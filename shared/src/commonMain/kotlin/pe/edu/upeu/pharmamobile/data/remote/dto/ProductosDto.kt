package pe.edu.upeu.pharmamobile.data.remote.dto

import kotlinx.serialization.Serializable

@Serializable
data class ProductoDto(val id: Long, val nombre: String, val precio: Double, val stock: Int, val estado: Boolean, val categoriaId: Long? = null)

@Serializable
data class ProductoRequestDto(val nombre: String, val precio: Double, val stock: Int, val estado: Boolean, val categoriaId: Long)

@Serializable
data class PaginaResponseDto<T>(val contenido: List<T>, val pagina: Int = 0, val tamanio: Int = 20, val totalElementos: Long = 0, val totalPaginas: Int = 0, val ultima: Boolean)

typealias PaginaProductosDto = PaginaResponseDto<ProductoDto>

@Serializable
data class ErrorResponseDto(val message: String = "Operación no permitida", val validationErrors: Map<String, String> = emptyMap())
