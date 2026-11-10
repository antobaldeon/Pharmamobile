package pe.edu.upeu.pharmamobile.domain.repository

import pe.edu.upeu.pharmamobile.domain.model.Producto

interface ProductoRepository {
    fun observar(): kotlinx.coroutines.flow.Flow<List<Producto>>
    fun observarUltimaSincronizacion(): kotlinx.coroutines.flow.Flow<Long?> = kotlinx.coroutines.flow.flowOf(null)
    suspend fun reintentar(id: Long) { sincronizar() }
    suspend fun sincronizar()
    suspend fun registrar(producto: Producto): Producto
    suspend fun obtener(id: Long): Producto
    suspend fun actualizar(producto: Producto): Producto
    suspend fun eliminar(id: Long)
    suspend fun listar(): List<Producto>
}
