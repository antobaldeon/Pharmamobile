from pathlib import Path
b=Path('shared/src/commonMain/kotlin/pe/edu/upeu/pharmamobile')
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def edit(p,a,c):
 s=p.read_text(encoding='utf-8');assert a in s,(p,a);write(p,s.replace(a,c))
sql='''CREATE TABLE estado_sincronizacion (
    id INTEGER NOT NULL PRIMARY KEY CHECK (id = 1),
    ultima_correcta INTEGER NOT NULL
);
'''
write(Path('shared/src/commonMain/sqldelight/db/EstadoSincronizacion.sq'),sql+'''
leerUltima:
SELECT ultima_correcta FROM estado_sincronizacion WHERE id = 1;

guardarUltima:
INSERT OR REPLACE INTO estado_sincronizacion VALUES (1, ?);
''')
write(Path('shared/src/commonMain/sqldelight/db/1.sqm'),sql)
p=b/'data/local/ProductoLocal.kt'
edit(p,'import app.cash.sqldelight.coroutines.asFlow','import app.cash.sqldelight.coroutines.mapToOneOrNull\nimport app.cash.sqldelight.coroutines.asFlow')
edit(p,'    fun observar() =','    fun observarUltimaSincronizacion() = base.estadoSincronizacionQueries.leerUltima().asFlow().mapToOneOrNull(dispatcher)\n    fun ultimaSincronizacion() = base.estadoSincronizacionQueries.leerUltima().executeAsOneOrNull()\n\n    fun observar() =')
edit(p,'fun reemplazarSincronizados(productos: List<Producto>) = base.transaction {','fun reemplazarSincronizados(productos: List<Producto>, instanteCorrecto: Long? = null) = base.transaction {')
edit(p,'        productos.forEach(::guardarSincronizado)','        productos.forEach(::guardarSincronizado)\n        instanteCorrecto?.let { base.estadoSincronizacionQueries.guardarUltima(it) }')
p=b/'domain/repository/ProductoRepository.kt'
edit(p,'    suspend fun sincronizar()','    fun observarUltimaSincronizacion(): kotlinx.coroutines.flow.Flow<Long?> = kotlinx.coroutines.flow.flowOf(null)\n    suspend fun sincronizar()')
p=b/'data/repository/ProductoRepositorioOffline.kt'
edit(p,'private val dispatcher: CoroutineDispatcher = Dispatchers.Default','private val dispatcher: CoroutineDispatcher = Dispatchers.Default,\n    private val ahora: () -> Long = { kotlin.time.Clock.System.now().toEpochMilliseconds() }')
edit(p,'    override fun observar() = local.observar()','    override fun observar() = local.observar()\n    override fun observarUltimaSincronizacion() = local.observarUltimaSincronizacion()')
edit(p,'        local.reemplazarSincronizados(remoto.listar())','        val productos = remoto.listar()\n        local.reemplazarSincronizados(productos, ahora())')
p=b/'presentation/producto/ProductoUiState.kt'
edit(p,'val avisoRed: String? = null','val avisoRed: String? = null,\n    val ultimaSincronizacionMillis: Long? = null')
p=b/'presentation/producto/ProductoViewModel.kt'
edit(p,'        sincronizar()\n    }','''        viewModelScope.launch {
            productoRepository.observarUltimaSincronizacion().collect { instante ->
                _uiState.update { it.copy(ultimaSincronizacionMillis = instante) }
            }
        }
        sincronizar()
    }''')
write(b/'presentation/producto/AntiguedadDatos.kt','''package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.compose.material3.Text
import androidx.compose.runtime.*
import kotlinx.coroutines.delay
import kotlin.time.Clock

fun textoAntiguedad(ultima: Long?, ahora: Long): String {
    if (ultima == null) return "Nunca sincronizado"
    val segundos = if (ahora <= ultima) 0L else (ahora - ultima) / 1000
    return when {
        segundos < 60 -> "Actualizado hace un momento"
        segundos < 3600 -> {
            val n = segundos / 60
            "Actualizado hace $n ${if (n == 1L) "minuto" else "minutos"}"
        }
        segundos < 86400 -> {
            val n = segundos / 3600
            "Actualizado hace $n ${if (n == 1L) "hora" else "horas"}"
        }
        else -> {
            val n = segundos / 86400
            "Actualizado hace $n ${if (n == 1L) "día" else "días"}"
        }
    }
}

@Composable
fun AntiguedadDatos(ultima: Long?) {
    var ahora by remember { mutableStateOf(Clock.System.now().toEpochMilliseconds()) }
    LaunchedEffect(ultima) {
        while (true) {
            ahora = Clock.System.now().toEpochMilliseconds()
            delay(60_000)
        }
    }
    Text(textoAntiguedad(ultima, ahora))
}
''')
p=b/'presentation/producto/ProductoScreen.kt'
edit(p,'        // [Sesion 10 | Permisos] Oculta el formulario','        item { AntiguedadDatos(uiState.ultimaSincronizacionMillis) }\n        // [Sesion 10 | Permisos] Oculta el formulario')
edit(p,'MensajeVacio("No hay productos registrados")','MensajeVacio("No hay productos guardados. Conéctate y pulsa Sincronizar para descargar el catálogo.")')
p=b/'presentation/sesion/LoginScreen.kt'
edit(p,'    val aviso by viewModel.aviso.collectAsState()','''    val aviso by viewModel.aviso.collectAsState()
    val local: pe.edu.upeu.pharmamobile.data.local.ProductoLocal = org.koin.compose.koinInject()
    val productos by remember(local) { local.observar() }.collectAsState(initial = null)
    val ultima by remember(local) { local.observarUltimaSincronizacion() }.collectAsState(initial = null)''')
edit(p,'            Text("Iniciar sesión", style = MaterialTheme.typography.titleLarge)','''            Text("Iniciar sesión", style = MaterialTheme.typography.titleLarge)
            if (productos?.isEmpty() == true && !estado.restaurando) {
                Text("No hay productos guardados en este dispositivo. Para la primera descarga, inicia sesión con conexión.")
                pe.edu.upeu.pharmamobile.presentation.producto.AntiguedadDatos(ultima)
            }''')
