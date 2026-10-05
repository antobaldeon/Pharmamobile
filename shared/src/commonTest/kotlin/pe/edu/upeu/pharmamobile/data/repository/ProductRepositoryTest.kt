package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.test.runTest
import pe.edu.upeu.pharmamobile.domain.model.Producto
import kotlin.test.Test
import kotlin.test.assertEquals

class ProductRepositoryTest {

    @Test
    fun listarRetornaListaSimulada() = runTest {
        val repository = ProductoRepositorioEnMemoria()
        val productos = repository.listar()

        assertEquals(5, productos.size)
        assertEquals("Paracetamol", productos[0].nombre)
    }

    @Test
    fun registrarAsignaIdEnRepositorio() = runTest {
        val repository = ProductoRepositorioEnMemoria()
        val producto = repository.registrar(Producto(0, "Azitromicina", 30.0, 10))

        assertEquals(6, producto.id)
        assertEquals(6, repository.listar().size)
    }
    @Test
    fun actualizarYEliminarReflejanLosCambios() = runTest {
        val repository = ProductoRepositorioEnMemoria()
        val original = repository.obtener(1)
        repository.actualizar(original.copy(nombre = "Producto actualizado"))
        assertEquals("Producto actualizado", repository.obtener(1).nombre)
        repository.eliminar(1)
        assertEquals(false, repository.listar().any { it.id == 1L })
    }
}
