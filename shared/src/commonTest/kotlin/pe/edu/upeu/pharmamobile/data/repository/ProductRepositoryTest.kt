package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.test.runTest
import pe.edu.upeu.pharmamobile.Domain.model.ResultadoProductos
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertTrue

class ProductoRepositoryTest {

    @Test
    fun obtenerProductosRetornaListaSimulada() = runTest {
        val repository = ProductoRepository()
        val productos = repository.obtenerProductos()

        assertEquals(3, productos.size)
        assertEquals("Paracetamol", productos[0].nombre)
    }

    @Test
    fun observarProductosEmiteVacioLuegoListaCompleta() = runTest {
        val repository = ProductoRepository()
        val emisiones = repository.observarProductos().toList()

        assertEquals(2, emisiones.size)
        assertTrue(emisiones[0].isEmpty())
        assertEquals(3, emisiones[1].size)
    }

    @Test
    fun cargarProductosEmiteCargandoLuegoExito() = runTest {
        val repository = ProductoRepository()
        val emisiones = repository.cargarProductos().toList()

        assertEquals(2, emisiones.size)
        assertIs<ResultadoProductos.Cargando>(emisiones[0])
        assertIs<ResultadoProductos.Exito>(emisiones[1])

        val exito = emisiones[1] as ResultadoProductos.Exito
        assertEquals(3, exito.lista.size)
        assertEquals("Paracetamol", exito.lista[0].nombre)
    }
}