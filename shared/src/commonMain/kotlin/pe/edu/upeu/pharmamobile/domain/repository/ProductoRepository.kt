package pe.edu.upeu.pharmamobile.domain.repository

import pe.edu.upeu.pharmamobile.domain.model.Producto

interface ProductoRepository {
    suspend fun registrar(producto: Producto): Producto
    suspend fun obtener(id: Long): Producto
    suspend fun actualizar(producto: Producto): Producto
    suspend fun eliminar(id: Long)
    suspend fun listar(): List<Producto>
}
