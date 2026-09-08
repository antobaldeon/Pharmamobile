package pe.edu.upeu.pharmamobile.presentation.producto

import pe.edu.upeu.pharmamobile.domain.model.Producto

enum class FiltroProducto(val titulo: String) {
    Activos("Activos"),
    Inactivos("Inactivos"),
    BajoStock("Bajo stock")
}

sealed interface FaseProductos {
    data object Cargando : FaseProductos
    data object SinProductos : FaseProductos
    data class ConProductos(val productos: List<Producto>) : FaseProductos
    data class Error(val mensaje: String) : FaseProductos
}

data class ProductoUiState(
    val fase: FaseProductos = FaseProductos.Cargando,
    val nombre: String = "",
    val precio: String = "",
    val stock: String = "",
    val errorNombre: String? = null,
    val errorPrecio: String? = null,
    val errorStock: String? = null,
    val filtroSeleccionado: FiltroProducto = FiltroProducto.Activos,
    val mensajeExito: String? = null
)
