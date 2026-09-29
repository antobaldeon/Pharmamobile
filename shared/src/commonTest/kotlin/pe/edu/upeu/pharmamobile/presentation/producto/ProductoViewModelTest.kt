package pe.edu.upeu.pharmamobile.presentation.producto

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository
import pe.edu.upeu.pharmamobile.domain.usecase.RegistrarProductoUseCase
import kotlin.test.AfterTest
import kotlin.test.BeforeTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs

@OptIn(ExperimentalCoroutinesApi::class)
class ProductoViewModelTest {
    private val dispatcher = StandardTestDispatcher()

    @BeforeTest
    fun configurarDispatcherPrincipal() {
        Dispatchers.setMain(dispatcher)
    }

    @AfterTest
    fun restaurarDispatcherPrincipal() {
        Dispatchers.resetMain()
    }

    @Test
    fun repositorioVacioMuestraFaseSinProductos() = runTest {
        val viewModel = crearViewModel(RepositorioFalso())

        advanceUntilIdle()

        assertIs<FaseProductos.SinProductos>(viewModel.uiState.value.fase)
    }

    @Test
    fun repositorioConProductosMuestraFaseConProductos() = runTest {
        val productos = listOf(
            Producto(1, "Paracetamol", 15.5, 100),
            Producto(2, "Ibuprofeno", 18.9, 50),
            Producto(3, "Amoxicilina", 25.0, 5)
        )
        val viewModel = crearViewModel(RepositorioFalso(productos = productos))

        advanceUntilIdle()

        val fase = assertIs<FaseProductos.ConProductos>(viewModel.uiState.value.fase)
        assertEquals(productos, fase.productos)
    }

    @Test
    fun repositorioQueFallaMuestraFaseError() = runTest {
        val viewModel = crearViewModel(RepositorioFalso(errorAlListar = IllegalStateException("Fallo de prueba")))

        advanceUntilIdle()

        val fase = assertIs<FaseProductos.Error>(viewModel.uiState.value.fase)
        assertEquals("Fallo de prueba", fase.mensaje)
    }

    @Test
    fun precioCeroMuestraErrorYNoRegistraProducto() = runTest {
        val repositorio = RepositorioFalso()
        val viewModel = crearViewModel(repositorio)
        advanceUntilIdle()

        viewModel.actualizarNombre("Paracetamol")
        viewModel.actualizarPrecio("0")
        viewModel.actualizarStock("10")
        viewModel.registrarProducto()
        advanceUntilIdle()

        assertEquals("El precio debe ser mayor a 0", viewModel.uiState.value.errorPrecio)
        assertEquals(0, repositorio.registrosRealizados)
    }

    private fun crearViewModel(repositorio: ProductoRepository): ProductoViewModel = ProductoViewModel(
        registrarProducto = RegistrarProductoUseCase(repositorio),
        productoRepository = repositorio
    )

    private class RepositorioFalso(
        private val productos: List<Producto> = emptyList(),
        private val errorAlListar: Throwable? = null
    ) : ProductoRepository {
        var registrosRealizados = 0
            private set

        override suspend fun registrar(producto: Producto): Producto {
            registrosRealizados++
            return producto.copy(id = 1)
        }

        override suspend fun listar(): List<Producto> {
            errorAlListar?.let { throw it }
            return productos
        }
    }
}
