package pe.edu.upeu.pharmamobile.Domain.model

sealed class ResultadoProductos{
    data object Cargando : ResultadoProductos()
    data class Exito(val lista: List<Producto>) : ResultadoProductos()
    data class Error(val msg: String) : ResultadoProductos()
}
