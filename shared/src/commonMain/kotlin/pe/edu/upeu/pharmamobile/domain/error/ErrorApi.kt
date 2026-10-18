package pe.edu.upeu.pharmamobile.domain.error

sealed interface ErrorApi {
    // [Sesion 10 | HTTP] Mantiene separados los codigos 401 y 403.
    data object SesionExpirada : ErrorApi
    data object SinPermiso : ErrorApi
    data class Validacion(val porCampo: Map<String, String>) : ErrorApi
    data object NoEncontrado : ErrorApi
    data class Conflicto(val mensaje: String) : ErrorApi
    data object Servidor : ErrorApi
    data object SinConexion : ErrorApi
    data object TiempoAgotado : ErrorApi
}

class ErrorApiException(val error: ErrorApi) : Exception(when (error) {
    is ErrorApi.Validacion -> error.porCampo.values.firstOrNull() ?: "Revisa los datos del producto"
    ErrorApi.SesionExpirada -> "Tu sesiÛn expirÛ. Inicia sesiÛn nuevamente"
    ErrorApi.SinPermiso -> "No tienes permiso para esta operaciÛn"
    ErrorApi.NoEncontrado -> "Producto o categor√≠a no encontrados"
    is ErrorApi.Conflicto -> error.mensaje
    ErrorApi.Servidor -> "Error del servidor"
    ErrorApi.SinConexion -> "No se pudo conectar con el servidor"
    ErrorApi.TiempoAgotado -> "Se agot√≥ el tiempo de espera"
})
