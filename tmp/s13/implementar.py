from pathlib import Path
b=Path('shared/src/commonMain/kotlin/pe/edu/upeu/pharmamobile')
def w(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def e(p,a,c):
 s=p.read_text(encoding='utf-8');assert a in s,(p,a);w(p,s.replace(a,c))
e(b/'domain/model/Producto.kt','val pendiente: Boolean = false','val pendiente: Boolean = false,\n    val intentos: Long = 0,\n    val ultimoError: String? = null')
p=Path('shared/src/commonMain/sqldelight/db/Producto.sq')
e(p,'pendiente INTEGER NOT NULL DEFAULT 0','pendiente INTEGER NOT NULL DEFAULT 0,\n    intentos INTEGER NOT NULL DEFAULT 0,\n    ultimoError TEXT')
# Keep insert compatible: new rows default metadata; failed edits intentionally reset retry state.
w(Path('shared/src/commonMain/sqldelight/db/2.sqm'),'ALTER TABLE producto ADD COLUMN intentos INTEGER NOT NULL DEFAULT 0;\nALTER TABLE producto ADD COLUMN ultimoError TEXT;\n')
s=p.read_text(encoding='utf-8');s+='''
registrarFallo:
UPDATE producto SET intentos = ?, ultimoError = ? WHERE id = ? AND pendiente = 1;

restablecerEnvio:
UPDATE producto SET intentos = 0, ultimoError = NULL WHERE id = ? AND pendiente = 1;
''';w(p,s)
p=b/'data/local/ProductoLocal.kt'
e(p,'pendiente: Long) =','pendiente: Long, intentos: Long, ultimoError: String?) =')
e(p,'categoriaId, pendiente == 1L)','categoriaId, pendiente == 1L, intentos, ultimoError)')
e(p,'    fun eliminar(id: Long)', '''    fun registrarFallo(id: Long, intentos: Long, error: String) { consultas.registrarFallo(intentos, error, id) }
    fun restablecerEnvio(id: Long) { consultas.restablecerEnvio(id) }
    fun eliminar(id: Long)''')
w(b/'domain/model/ResultadoEnvio.kt','''package pe.edu.upeu.pharmamobile.domain.model
sealed interface ResultadoEnvio {
    data class Transitorio(val motivo: String) : ResultadoEnvio
    data class Permanente(val motivo: String) : ResultadoEnvio
}
const val MAX_INTENTOS_ENVIO = 5L
fun esperaEnvio(intentos: Long): Long = 1000L shl (intentos - 1).coerceIn(0, 4).toInt()
''')
w(b/'data/repository/ClasificarEnvio.kt','''package pe.edu.upeu.pharmamobile.data.repository
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.model.ResultadoEnvio
fun ErrorApiException.resultadoEnvio(): ResultadoEnvio = when (error) {
    ErrorApi.SinConexion, ErrorApi.TiempoAgotado, ErrorApi.Servidor -> ResultadoEnvio.Transitorio(message ?: "Error de conexión")
    else -> ResultadoEnvio.Permanente(message ?: "Revisar el producto")
}
''')
p=b/'domain/repository/ProductoRepository.kt'
e(p,'    suspend fun sincronizar()','    suspend fun reintentar(id: Long) { sincronizar() }\n    suspend fun sincronizar()')
p=b/'data/repository/ProductoRepositorioOffline.kt'
e(p,'import kotlinx.coroutines.withContext','import kotlinx.coroutines.delay\nimport pe.edu.upeu.pharmamobile.domain.model.*\nimport kotlinx.coroutines.withContext')
e(p,'sincronizarInterno()\n            } catch','sincronizarInterno(soloNuevos = true)\n            } catch')
a=p.read_text(encoding='utf-8');start=a.index('    private suspend fun sincronizarInterno()');end=a.index('    override suspend fun actualizar',start)
a=a[:start]+'''    override suspend fun reintentar(id: Long) = withContext(dispatcher) {
        mutex.withLock {
            local.restablecerEnvio(id)
            sincronizarInterno()
        }
    }
    private suspend fun sincronizarInterno(soloNuevos: Boolean = false) {
        var primerFallo: ErrorApiException? = null
        local.pendientes().filter { it.intentos < MAX_INTENTOS_ENVIO && (!soloNuevos || it.intentos == 0L) }.forEach { pendiente ->
            // Los POST no son idempotentes: no hay bucle automático. Una nueva
            // pulsación de Sincronizar autoriza el reenvío de resultados inciertos.
            if (pendiente.intentos > 0) delay(esperaEnvio(pendiente.intentos))
            try {
                val servidor = remoto.registrar(pendiente.copy(id = 0, pendiente = false))
                local.confirmarEnvio(pendiente.id, servidor)
            } catch (error: ErrorApiException) {
                val resultado = error.resultadoEnvio()
                val intentos = if (resultado is ResultadoEnvio.Permanente) MAX_INTENTOS_ENVIO else pendiente.intentos + 1
                local.registrarFallo(pendiente.id, intentos, error.message ?: "Error de envío")
                if (primerFallo == null) primerFallo = error
            }
        }
        // No se oculta un fallo ni se registra una sincronización completa falsa.
        primerFallo?.let { throw it }
        val productos = remoto.listar()
        local.reemplazarSincronizados(productos, ahora())
    }
'''+a[end:];w(p,a)
p=b/'presentation/producto/ProductoUiState.kt'
e(p,'val ultimaSincronizacionMillis: Long? = null','val ultimaSincronizacionMillis: Long? = null,\n    val pendientes: Int = 0,\n    val fallidas: Int = 0')
p=b/'presentation/producto/ProductoViewModel.kt'
e(p,'it.copy(fase = faseDe(productos))','it.copy(fase = faseDe(productos), pendientes = productos.count { p -> p.pendiente && p.intentos < 5 }, fallidas = productos.count { p -> p.pendiente && p.intentos >= 5 })')
e(p,'    fun recargarProductos()', '''    fun reintentar(id: Long) {
        if (_uiState.value.sincronizando) return
        _uiState.update { it.copy(sincronizando = true) }
        viewModelScope.launch {
            try {
                resultadoProducto { productoRepository.reintentar(id) }.onFailure(::manejarFallo)
            } finally { _uiState.update { it.copy(sincronizando = false) } }
        }
    }
    fun recargarProductos()''')
p=b/'presentation/producto/ProductoScreen.kt'
e(p,'        item { AntiguedadDatos(uiState.ultimaSincronizacionMillis) }','''        item { AntiguedadDatos(uiState.ultimaSincronizacionMillis) }
        item { Text("${uiState.pendientes} cambios por enviar · ${uiState.fallidas} fallidos") }
        item { pe.edu.upeu.pharmamobile.presentation.permiso.PermisoNotificaciones() }
        if (uiState.pendientes > 0 || uiState.fallidas > 0) item {
            Text("Antes de reenviar, verifica en el servidor que el producto no exista. Un envío sin respuesta puede haberse registrado.")
        }
        (uiState.fase as? FaseProductos.ConProductos)?.productos?.filter { it.producto.pendiente && it.producto.ultimoError != null }?.forEach { fila ->
            item {
                Column {
                    Text("${fila.producto.nombre}: ${fila.producto.ultimoError} · Intentos ${fila.producto.intentos}/5")
                    OutlinedButton(onClick = { viewModel.reintentar(fila.producto.id) }, enabled = !uiState.sincronizando) {
                        Text("Confirmar reenvío de este producto")
                    }
                }
            }
        }''')
w(b/'domain/permiso/GestorPermisos.kt','''package pe.edu.upeu.pharmamobile.domain.permiso
enum class Permiso { NOTIFICACIONES }
sealed interface EstadoPermiso {
    data object Concedido : EstadoPermiso
    data object Denegado : EstadoPermiso
    data object DenegadoParaSiempre : EstadoPermiso
}
interface GestorPermisos {
    suspend fun estado(permiso: Permiso): EstadoPermiso
    suspend fun solicitar(permiso: Permiso): EstadoPermiso
    fun abrirAjustes()
    fun notificacionPrueba()
}
fun resolverEstadoPermiso(concedido: Boolean, pedido: Boolean, explicar: Boolean): EstadoPermiso = when {
    concedido -> EstadoPermiso.Concedido
    !pedido || explicar -> EstadoPermiso.Denegado
    else -> EstadoPermiso.DenegadoParaSiempre
}
''')
w(b/'presentation/permiso/PermisoNotificaciones.kt','''package pe.edu.upeu.pharmamobile.presentation.permiso
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.*
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import kotlinx.coroutines.launch
import org.koin.compose.koinInject
import pe.edu.upeu.pharmamobile.domain.permiso.*
@Composable fun PermisoNotificaciones() {
    val gestor: GestorPermisos = koinInject()
    val scope = rememberCoroutineScope()
    var estado by remember { mutableStateOf<EstadoPermiso>(EstadoPermiso.Denegado) }
    var ocupado by remember { mutableStateOf(false) }
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) { scope.launch { estado = gestor.estado(Permiso.NOTIFICACIONES) } }
    Column {
        Text("Notificaciones: " + when (estado) {
            EstadoPermiso.Concedido -> "Concedido"
            EstadoPermiso.Denegado -> "Denegado"
            EstadoPermiso.DenegadoParaSiempre -> "Denegado para siempre"
        })
        Text("Permite mostrar avisos de PharmaMobil. Puedes continuar usando el catálogo sin este permiso.")
        Button(enabled = !ocupado, onClick = {
            if (estado == EstadoPermiso.DenegadoParaSiempre) gestor.abrirAjustes()
            else if (estado == EstadoPermiso.Concedido) gestor.notificacionPrueba()
            else scope.launch {
                ocupado = true
                try { estado = gestor.solicitar(Permiso.NOTIFICACIONES) } finally { ocupado = false }
            }
        }) { Text(when (estado) {
            EstadoPermiso.Concedido -> "Probar notificación"
            EstadoPermiso.DenegadoParaSiempre -> "Abrir Ajustes"
            else -> "Permitir notificaciones"
        }) }
    }
}
''')
