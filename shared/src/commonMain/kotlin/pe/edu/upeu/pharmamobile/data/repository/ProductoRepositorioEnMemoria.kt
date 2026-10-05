package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.delay
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class ProductoRepositorioEnMemoria : ProductoRepository {
    private val productos = mutableListOf(
        Producto(1, "Paracetamol", 15.50, 100),
        Producto(2, "Ibuprofeno", 18.90, 50),
        Producto(3, "Amoxicilina", 25.00, 5),
        Producto(4, "Loratadina", 12.50, 0, activo = false),
        Producto(5, "Diclofenaco", 20.00, 3)
    )

    override suspend fun registrar(producto: Producto): Producto {
        delay(500)
        val productoRegistrado = producto.copy(id = (productos.maxOfOrNull { it.id } ?: 0) + 1)
        productos += productoRegistrado
        return productoRegistrado
    }

    override suspend fun listar(): List<Producto> {
        delay(500)
        return productos.toList()
    }
    override suspend fun obtener(id: Long): Producto = productos.first { it.id == id }
    override suspend fun actualizar(producto: Producto): Producto {
        val index = productos.indexOfFirst { it.id == producto.id }
        require(index >= 0) { "Producto no encontrado" }
        productos[index] = producto
        return producto
    }
    override suspend fun eliminar(id: Long) {
        require(productos.removeAll { it.id == id }) { "Producto no encontrado" }
    }
}
