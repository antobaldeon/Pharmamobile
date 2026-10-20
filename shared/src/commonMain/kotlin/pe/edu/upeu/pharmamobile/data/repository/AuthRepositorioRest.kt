package pe.edu.upeu.pharmamobile.data.repository
import io.ktor.client.plugins.HttpRequestTimeoutException
import io.ktor.utils.io.errors.IOException
import io.ktor.client.HttpClient
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.plugins.auth.authProvider
import io.ktor.client.plugins.auth.providers.BearerAuthProvider
import kotlinx.coroutines.CancellationException
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.data.mapper.aSesion
import pe.edu.upeu.pharmamobile.data.remote.AuthApi
import pe.edu.upeu.pharmamobile.data.remote.dto.LoginRequestDto
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.model.*
import pe.edu.upeu.pharmamobile.domain.repository.AuthRepository
// [Sesion 10 | Repositorio] Guarda el JWT, limpia la cache Bearer y restaura identidad mediante /auth/me.
class AuthRepositorioRest(private val api: AuthApi, private val cliente: HttpClient,
    private val almacen: AlmacenSeguro, private val gestor: GestorSesion, private val local: SesionLocal? = null) : AuthRepository {
    override suspend fun iniciarSesion(credenciales: Credenciales): Sesion = traducir(true) {
        val dto = api.login(LoginRequestDto(credenciales.usuario.trim(), credenciales.clave))
        require(dto.token.isNotBlank())
        almacen.guardarToken(dto.token)
        limpiarCache()
        dto.aSesion().also(gestor::activar)
    }
    override suspend fun sesionGuardada(): Sesion? {
        val token = almacen.leerToken() ?: return null
        return try {
            traducir(false) { api.usuarioActual().aSesion(token).also(gestor::activar) }
        } catch (e: ErrorSesionException) {
            if (e.error != ErrorSesion.SinConexion) throw e
            local?.leer(token)?.also(gestor::activar) ?: throw e
        }
    }
    override suspend fun cerrarSesion() { gestor.cerrar(); limpiarCache() }
    private fun limpiarCache() { cliente.authProvider<BearerAuthProvider>()?.clearToken() }
    private suspend fun <T> traducir(login: Boolean, bloque: suspend () -> T): T = try { bloque() }
    catch (e: CancellationException) { throw e }
    catch (e: ClientRequestException) {
        throw ErrorSesionException(when(e.response.status.value) {
            401 -> if(login) ErrorSesion.CredencialesInvalidas else ErrorSesion.SesionExpirada
            403 -> ErrorSesion.SinPermiso
            else -> throw e
        })
    } catch (e: ErrorSesionException) { throw e }
    catch (_: IOException) { throw ErrorSesionException(ErrorSesion.SinConexion) }
    catch (_: HttpRequestTimeoutException) { throw ErrorSesionException(ErrorSesion.SinConexion) }
}
