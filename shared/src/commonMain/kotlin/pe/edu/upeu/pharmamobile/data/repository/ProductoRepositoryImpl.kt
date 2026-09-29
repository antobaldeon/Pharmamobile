package pe.edu.upeu.pharmamobile.data.repository

import pe.edu.upeu.pharmamobile.data.mapper.toDomain
import pe.edu.upeu.pharmamobile.data.remote.ProductoApi
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class ProductoRepositoryImpl(
    private val api: ProductoApi
) : ProductoRepository {

    override suspend fun listar(): List<Producto> {
        val productos = mutableListOf<Producto>()
        var pagina = 0

        do {
            val respuesta = api.obtenerPagina(pagina)
            productos.addAll(
                respuesta.contenido.map { it.toDomain() }
            )
            pagina++
        } while (!respuesta.ultima)

        return productos
    }

    override suspend fun registrar(producto: Producto): Producto {
        throw UnsupportedOperationException(
            "Por ahora registra los productos desde Swagger."
        )
    }
}