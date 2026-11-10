package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.delay
import pe.edu.upeu.pharmamobile.domain.model.*
import kotlinx.coroutines.withContext
import pe.edu.upeu.pharmamobile.data.local.ProductoLocal
import pe.edu.upeu.pharmamobile.domain.error.ErrorApiException
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class ProductoRepositorioOffline(
    private val local: ProductoLocal,
    private val remoto: ProductoRepository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.Default,
    private val telemetria: pe.edu.upeu.pharmamobile.domain.port.Telemetria? = null,
    private val ahora: () -> Long = { kotlin.time.Clock.System.now().toEpochMilliseconds() }
) : ProductoRepository {
    private val mutex = Mutex()
    override fun observar() = local.observar()
    override fun observarUltimaSincronizacion() = local.observarUltimaSincronizacion()
    override suspend fun listar() = withContext(dispatcher) { local.listar() }
    override suspend fun obtener(id: Long) = withContext(dispatcher) { local.obtener(id) }

    override suspend fun registrar(producto: Producto): Producto = withContext(dispatcher) {
        mutex.withLock {
            val guardado = local.guardarPendiente(producto)
            try {
                sincronizarInterno(soloNuevos = true)
            } catch (e: ErrorApiException) {
                // Los errores por campo deben volver al formulario. La fila
                // rechazada ya quedó conservada y marcada como fallida.
                if (e.error is pe.edu.upeu.pharmamobile.domain.error.ErrorApi.Validacion) throw e
                // El alta local tuvo éxito. Un fallo remoto conserva el pendiente;
                // sincronizar explícitamente permite consultar y reintentar el error.
                return@withLock guardado
            }
            // La lista observada refleja el ID definitivo; devolver el alta local
            // mantiene estable el resultado incluso si la descarga posterior falló.
            guardado
        }
    }
    override suspend fun sincronizar() = withContext(dispatcher) {
        mutex.withLock { sincronizarInterno() }
    }
    override suspend fun reintentar(id: Long) = withContext(dispatcher) {
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
                telemetria?.registrarEvento("sincronizacion_fallida")
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
        telemetria?.registrarEvento("sincronizacion_correcta")
    }
    override suspend fun actualizar(producto: Producto): Producto = withContext(dispatcher) {
        mutex.withLock {
            if (producto.id < 0) local.actualizarPendiente(producto)
            else remoto.actualizar(producto).also(local::guardarSincronizado)
        }
    }
    override suspend fun eliminar(id: Long) = withContext(dispatcher) {
        mutex.withLock {
            if (id > 0) remoto.eliminar(id)
            local.eliminar(id)
            Unit
        }
    }
}
