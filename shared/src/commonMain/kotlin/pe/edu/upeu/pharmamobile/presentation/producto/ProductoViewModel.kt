package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.usecase.*

class ProductoViewModel(
    private val registrarProducto: RegistrarProductoUseCase,
    private val productoRepository: ProductoRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(ProductoUiState())
    val uiState = _uiState.asStateFlow()
    init { listarProductos() }
    fun actualizarNombre(valor: String) = _uiState.update { it.copy(nombre = valor, errorNombre = null) }
    fun actualizarPrecio(valor: String) = _uiState.update { it.copy(precio = valor, errorPrecio = null) }
    fun actualizarStock(valor: String) = _uiState.update { it.copy(stock = valor, errorStock = null) }
    fun actualizarCategoria(valor: String) = _uiState.update { it.copy(categoriaId = valor, errorCategoria = null) }
    fun seleccionarFiltro(filtro: FiltroProducto) = _uiState.update { it.copy(filtroSeleccionado = filtro) }
    fun cancelarEdicion() = _uiState.update { it.copy(productoEditando = null, nombre = "", precio = "", stock = "", categoriaId = "1", errorNombre = null, errorPrecio = null, errorStock = null, errorCategoria = null) }
    fun editar(producto: Producto) {
        if (_uiState.value.operacion is OperacionProducto.EnCurso) return
        viewModelScope.launch {
            resultadoProducto { productoRepository.obtener(producto.id) }.onSuccess { actual ->
                _uiState.update { it.copy(productoEditando = actual, nombre = actual.nombre, precio = actual.precio.toString(), stock = actual.stock.toString(), categoriaId = actual.categoriaId.toString(), errorNombre = null, errorPrecio = null, errorStock = null, errorCategoria = null, mensajeExito = null) }
            }.onFailure(::manejarFallo)
        }
    }
    fun registrarProducto() {
        val estado = _uiState.value
        if (estado.operacion is OperacionProducto.EnCurso) return
        val categoria = estado.categoriaId.toLongOrNull()
        if (categoria == null || categoria <= 0) {
            _uiState.update { it.copy(errorCategoria = "Ingresa una categoría válida") }
            return
        }
        viewModelScope.launch {
            val editando = estado.productoEditando
            _uiState.update { it.copy(operacion = OperacionProducto.EnCurso(if (editando == null) OperacionProducto.Tipo.Crear else OperacionProducto.Tipo.Actualizar), mensajeExito = null) }
            val resultado = if (editando == null) {
                registrarProducto(estado.nombre, estado.precio, estado.stock, categoria)
            } else {
                val precio = estado.precio.toDoubleOrNull()
                val stock = estado.stock.toIntOrNull()
                if (precio == null || stock == null) {
                    manejarFallo(ValidacionProductoException(null, if (precio == null) "Precio inválido" else null, if (stock == null) "Stock debe ser un número entero" else null))
                    return@launch
                }
                ActualizarProductoUseCase(productoRepository)(editando.copy(nombre = estado.nombre.trim(), precio = precio, stock = stock, categoriaId = categoria))
            }
            resultado.onSuccess {
                cancelarEdicion()
                refrescarTrasOperacion(if (editando == null) "Producto registrado correctamente" else "Producto actualizado")
            }.onFailure(::manejarFallo)
        }
    }
    fun eliminar(id: Long) {
        if (_uiState.value.operacion is OperacionProducto.EnCurso) return
        viewModelScope.launch {
            _uiState.update { it.copy(operacion = OperacionProducto.EnCurso(OperacionProducto.Tipo.Eliminar), mensajeExito = null) }
            EliminarProductoUseCase(productoRepository)(id).onSuccess {
                if (_uiState.value.productoEditando?.id == id) cancelarEdicion()
                refrescarTrasOperacion("Producto eliminado")
            }.onFailure(::manejarFallo)
        }
    }
    private suspend fun refrescarTrasOperacion(mensaje: String) {
        ListarProductosUseCase(productoRepository)().onSuccess { productos ->
            _uiState.update { it.copy(fase = faseDe(productos), operacion = OperacionProducto.Inactiva, mensajeExito = mensaje) }
        }.onFailure { fallo ->
            _uiState.update { it.copy(mensajeExito = mensaje) }
            manejarFallo(fallo)
        }
    }
    private fun manejarFallo(fallo: Throwable) {
        val validacion = fallo as? ValidacionProductoException
        val campos = ((fallo as? ErrorApiException)?.error as? ErrorApi.Validacion)?.porCampo
        _uiState.update {
            if (validacion != null || !campos.isNullOrEmpty()) it.copy(
                operacion = OperacionProducto.Inactiva, mensajeExito = null,
                errorNombre = validacion?.errorNombre ?: campos?.get("nombre"),
                errorPrecio = validacion?.errorPrecio ?: campos?.get("precio"),
                errorStock = validacion?.errorStock ?: campos?.get("stock"),
                errorCategoria = campos?.get("categoriaId")
            ) else it.copy(operacion = OperacionProducto.Fallida(fallo.message ?: "No se pudo completar la operación"))
        }
    }
    fun recargarProductos() {
        if (_uiState.value.fase != FaseProductos.Cargando && _uiState.value.operacion !is OperacionProducto.EnCurso) listarProductos()
    }
    private fun faseDe(productos: List<Producto>): FaseProductos =
        if (productos.isEmpty()) {
            FaseProductos.SinProductos
        } else {
            FaseProductos.ConProductos(
                productos.map { it.toUi() }
            )
        }
       private fun listarProductos() {
        viewModelScope.launch {
            _uiState.update { it.copy(fase = FaseProductos.Cargando) }
            ListarProductosUseCase(productoRepository)().onSuccess { productos ->
                _uiState.update { it.copy(fase = faseDe(productos)) }
            }.onFailure { error ->
                _uiState.update { it.copy(fase = FaseProductos.Error(error.message ?: "No se pudieron cargar los productos")) }
            }
        }
    }
}
