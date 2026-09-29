package pe.edu.upeu.pharmamobile.data.remote.dto

import kotlinx.serialization.Serializable

@Serializable
data class ProductoDto(
    val id: Long,
    val nombre: String,
    val precio: Double,
    val stock: Int,
    val estado: Boolean
)

@Serializable
data class PaginaProductosDto(
    val contenido: List<ProductoDto>,
    val ultima: Boolean
)