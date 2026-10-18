package pe.edu.upeu.pharmamobile.data.remote.dto
import kotlinx.serialization.Serializable
// [Sesion 10 | DTO] /auth/me devuelve empleadoNombre, no nombreCompleto.
@Serializable data class UsuarioActualDto(val username: String, val empleadoNombre: String, val permisos: List<String>, val roles: List<String> = emptyList())
