package pe.edu.upeu.pharmamobile.domain.error
// [Sesion 10 | Errores] Distingue autenticacion, autorizacion y conectividad.
sealed interface ErrorSesion {
    data object CredencialesInvalidas : ErrorSesion
    data object SesionExpirada : ErrorSesion
    data object SinPermiso : ErrorSesion
    data object SinConexion : ErrorSesion
}
class ErrorSesionException(val error: ErrorSesion) : Exception(when(error) {
    ErrorSesion.CredencialesInvalidas -> "Usuario o contraseña incorrectos"
    ErrorSesion.SesionExpirada -> "Tu sesión expiró. Inicia sesión nuevamente"
    ErrorSesion.SinPermiso -> "No tienes permiso para esta operación"
    ErrorSesion.SinConexion -> "No se pudo conectar con el servidor"
})
