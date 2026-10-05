package pe.edu.upeu.pharmamobile.data.repository

import pe.edu.upeu.pharmamobile.data.mapper.*
import pe.edu.upeu.pharmamobile.data.remote.*
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class ProductoRepositoryImpl(private val api: ProductoApi) : ProductoRepository {
    override suspend fun listar(): List<Producto> = ejecutarLlamada {
        val productos = mutableListOf<Producto>()
        var pagina = 0
        do {
            val respuesta = api.obtenerPagina(pagina++)
            productos.addAll(respuesta.contenido.map { it.toDomain() })
        } while (!respuesta.ultima)
        productos.toList()
    }.getOrThrow()
    override suspend fun obtener(id: Long): Producto = ejecutarLlamada { api.obtener(id).toDomain() }.getOrThrow()
    override suspend fun registrar(producto: Producto): Producto = ejecutarLlamada { api.crear(producto.toRequest()).toDomain() }.getOrThrow()
    override suspend fun actualizar(producto: Producto): Producto = ejecutarLlamada { api.actualizar(producto.id, producto.toRequest()).toDomain() }.getOrThrow()
    override suspend fun eliminar(id: Long) = ejecutarLlamada { api.eliminar(id) }.getOrThrow()
}
