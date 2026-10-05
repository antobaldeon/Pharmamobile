package pe.edu.upeu.pharmamobile.domain.usecase

import kotlinx.coroutines.CancellationException
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

suspend fun <T> resultadoProducto(bloque: suspend () -> T): Result<T> = try {
    Result.success(bloque())
} catch (e: CancellationException) { throw e } catch (e: Exception) { Result.failure(e) }

class ListarProductosUseCase(private val repository: ProductoRepository) {
    suspend operator fun invoke() = resultadoProducto { repository.listar() }
}
class ActualizarProductoUseCase(private val repository: ProductoRepository) {
    suspend operator fun invoke(producto: Producto) = resultadoProducto { repository.actualizar(producto) }
}
class EliminarProductoUseCase(private val repository: ProductoRepository) {
    suspend operator fun invoke(id: Long) = resultadoProducto { repository.eliminar(id) }
}
