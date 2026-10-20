package pe.edu.upeu.pharmamobile.data.local

import app.cash.sqldelight.coroutines.asFlow
import app.cash.sqldelight.coroutines.mapToList
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import pe.edu.upeu.pharmamobile.db.PharmaDb
import pe.edu.upeu.pharmamobile.domain.model.Producto

class ProductoLocal(private val base: PharmaDb, private val dispatcher: CoroutineDispatcher = Dispatchers.Default) {
    private val consultas = base.productoQueries
    private fun convertir(id: Long, nombre: String, precio: Double, stock: Long, activo: Long, categoriaId: Long, pendiente: Long) =
        Producto(id, nombre, precio, stock.toInt(), activo == 1L, categoriaId, pendiente == 1L)

    fun observar() = consultas.listarTodos(::convertir).asFlow().mapToList(dispatcher)
    fun listar() = consultas.listarTodos(::convertir).executeAsList()
    fun obtener(id: Long) = consultas.buscarPorId(id, ::convertir).executeAsOneOrNull() ?: error("Producto no encontrado en el dispositivo")
    fun pendientes() = consultas.listarPendientes(::convertir).executeAsList()
    private fun insertar(p: Producto) = consultas.insertar(p.id, p.nombre, p.precio, p.stock.toLong(), if (p.activo) 1L else 0L, p.categoriaId, if (p.pendiente) 1L else 0L)

    fun guardarPendiente(producto: Producto): Producto = base.transactionWithResult {
        val id = minOf(consultas.siguienteIdLocal().executeAsOne(), 0L) - 1L
        producto.copy(id = id, pendiente = true).also(::insertar)
    }
    fun actualizarPendiente(producto: Producto): Producto {
        require(producto.id < 0)
        obtener(producto.id)
        return producto.copy(pendiente = true).also(::insertar)
    }
    fun guardarSincronizado(producto: Producto) = insertar(producto.copy(pendiente = false))
    fun confirmarEnvio(idLocal: Long, servidor: Producto) = base.transaction {
        require(servidor.id > 0) { "El servidor no devolvió un ID válido" }
        consultas.borrarPorId(idLocal)
        guardarSincronizado(servidor)
    }
    fun reemplazarSincronizados(productos: List<Producto>) = base.transaction {
        consultas.borrarSincronizados()
        productos.forEach(::guardarSincronizado)
    }
    fun eliminar(id: Long) = consultas.borrarPorId(id)
}
