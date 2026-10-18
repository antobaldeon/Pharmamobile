package pe.edu.upeu.pharmamobile.data.remote.dto
import kotlinx.serialization.Serializable
// [Sesion 10 | DTO] Respeta los nombres JSON reales de PharmaSoft.
@Serializable data class LoginRequestDto(val username: String, val password: String)
@Serializable data class LoginResponseDto(val token: String, val tipo: String, val expiraEnSegundos: Long,
    val username: String, val nombreCompleto: String, val roles: List<String>, val permisos: List<String>)
