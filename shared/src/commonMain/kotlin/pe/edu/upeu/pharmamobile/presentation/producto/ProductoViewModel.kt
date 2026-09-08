package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository
import pe.edu.upeu.pharmamobile.domain.usecase.RegistrarProductoUseCase
import pe.edu.upeu.pharmamobile.domain.usecase.ValidacionProductoException

class ProductoViewModel(
    private val registrarProducto: RegistrarProductoUseCase,
    private val productoRepository: ProductoRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(ProductoUiState())
    val uiState = _uiState.asStateFlow()

    init {
        listarProductos()
    }

    fun actualizarNombre(valor: String) = _uiState.update { it.copy(nombre = valor, errorNombre = null) }
    fun actualizarPrecio(valor: String) = _uiState.update { it.copy(precio = valor, errorPrecio = null) }
    fun actualizarStock(valor: String) = _uiState.update { it.copy(stock = valor, errorStock = null) }
    fun seleccionarFiltro(filtro: FiltroProducto) = _uiState.update { it.copy(filtroSeleccionado = filtro) }

    fun registrarProducto() {
        viewModelScope.launch {
            registrarProducto(_uiState.value.nombre, _uiState.value.precio, _uiState.value.stock)
                .onSuccess {
                    _uiState.update {
                        it.copy(
                            nombre = "", precio = "", stock = "",
                            errorNombre = null, errorPrecio = null, errorStock = null,
                            mensajeExito = "Producto registrado correctamente"
                        )
                    }
                    listarProductos()
                }
                .onFailure { error ->
                    val validacion = error as? ValidacionProductoException
                    _uiState.update {
                        it.copy(
                            errorNombre = validacion?.errorNombre,
                            errorPrecio = validacion?.errorPrecio,
                            errorStock = validacion?.errorStock,
                            mensajeExito = null,
                            fase = if (validacion == null) FaseProductos.Error(error.message ?: "No se pudo registrar el producto") else it.fase
                        )
                    }
                }
        }
    }

    private fun listarProductos() {
        viewModelScope.launch {
            _uiState.update { it.copy(fase = FaseProductos.Cargando) }
            runCatching { productoRepository.listar() }
                .onSuccess { productos ->
                    _uiState.update {
                        it.copy(fase = if (productos.isEmpty()) FaseProductos.SinProductos else FaseProductos.ConProductos(productos))
                    }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(fase = FaseProductos.Error(error.message ?: "No se pudieron cargar los productos")) }
                }
        }
    }
}
