package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import pe.edu.upeu.pharmamobile.data.local.ProductoLocal
import pe.edu.upeu.pharmamobile.domain.error.ErrorApiException
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class ProductoRepositorioOffline(
    private val local: ProductoLocal,
    private val remoto: ProductoRepository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.Default
) : ProductoRepository {
    private val mutex = Mutex()
    override fun observar() = local.observar()
    override suspend fun listar() = withContext(dispatcher) { local.listar() }
    override suspend fun obtener(id: Long) = withContext(dispatcher) { local.obtener(id) }

    override suspend fun registrar(producto: Producto): Producto = withContext(dispatcher) {
        mutex.withLock {
            val guardado = local.guardarPendiente(producto)
            try {
                sincronizarInterno()
            } catch (e: ErrorApiException) {
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
    private suspend fun sincronizarInterno() {
        local.pendientes().forEach { pendiente ->
            val servidor = remoto.registrar(pendiente.copy(id = 0, pendiente = false))
            local.confirmarEnvio(pendiente.id, servidor)
        }
        local.reemplazarSincronizados(remoto.listar())
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
