package pe.edu.upeu.pharmamobile.data.remote
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.*
import io.ktor.client.plugins.auth.AuthCircuitBreaker
import pe.edu.upeu.pharmamobile.data.remote.dto.*
// [Sesion 10 | REST] Marca login como peticion de autenticacion para que nunca adjunte un token anterior.
class AuthApi(private val cliente: HttpClient) {
    suspend fun login(dto: LoginRequestDto): LoginResponseDto = cliente.post("api/v1/auth/login") {
        attributes.put(AuthCircuitBreaker, Unit)
        setBody(dto)
    }.body()
    suspend fun usuarioActual(): UsuarioActualDto = cliente.get("api/v1/auth/me").body()
}
