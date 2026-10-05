package pe.edu.upeu.pharmamobile.domain.error

sealed interface ErrorApi {
    data class Validacion(val porCampo: Map<String, String>) : ErrorApi
    data object NoEncontrado : ErrorApi
    data class Conflicto(val mensaje: String) : ErrorApi
    data object Servidor : ErrorApi
    data object SinConexion : ErrorApi
    data object TiempoAgotado : ErrorApi
}

class ErrorApiException(val error: ErrorApi) : Exception(when (error) {
    is ErrorApi.Validacion -> error.porCampo.values.firstOrNull() ?: "Revisa los datos del producto"
    ErrorApi.NoEncontrado -> "Producto o categoría no encontrados"
    is ErrorApi.Conflicto -> error.mensaje
    ErrorApi.Servidor -> "Error del servidor"
    ErrorApi.SinConexion -> "No se pudo conectar con el servidor"
    ErrorApi.TiempoAgotado -> "Se agotó el tiempo de espera"
})
