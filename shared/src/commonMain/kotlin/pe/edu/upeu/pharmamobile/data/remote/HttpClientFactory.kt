package pe.edu.upeu.pharmamobile.data.remote

import io.ktor.client.plugins.auth.Auth
import io.ktor.client.plugins.auth.authProvider
import io.ktor.client.plugins.auth.providers.*
import io.ktor.client.plugins.HttpResponseValidator
import io.ktor.client.plugins.ClientRequestException
import io.ktor.http.HttpHeaders
import io.ktor.http.Url
import io.ktor.http.encodedPath
import pe.edu.upeu.pharmamobile.data.local.AlmacenSeguro
import pe.edu.upeu.pharmamobile.data.local.GestorSesion
import io.ktor.client.HttpClient
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.logging.Logging
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

fun crearHttpClient(
    engine: HttpClientEngine,
    baseUrl: String,
    almacen: AlmacenSeguro,
    gestor: GestorSesion,
    esDepuracion: Boolean = false
): HttpClient {
    return HttpClient(engine) {
        expectSuccess = true

        install(ContentNegotiation) {
            json(
                Json {
                    ignoreUnknownKeys = true
                    isLenient = true
                    encodeDefaults = true
                }
            )
        }

        // [Sesion 10 | Auth] Envia JWT solo al backend configurado y nunca al login.
        val backend = Url(baseUrl)
        install(Auth) {
            bearer {
                loadTokens { almacen.leerToken()?.let { BearerTokens(it, "") } }
                sendWithoutRequest { request ->
                    request.url.host == backend.host && request.url.port == backend.port &&
                        request.url.protocol == backend.protocol &&
                        !request.url.encodedPath.endsWith("/auth/login")
                }
            }
        }
        // [Sesion 10 | Expiracion] Un 401 protegido borra almacenamiento y cache y avisa a la UI.
        HttpResponseValidator {
            handleResponseExceptionWithRequest { causa, request ->
                val response = (causa as? ClientRequestException)?.response
                if (response?.status?.value == 401 && !request.url.encodedPath.endsWith("/auth/login")) {
                    gestor.cerrar("Tu sesión expiró. Inicia sesión nuevamente")
                    response.call.client.authProvider<BearerAuthProvider>()?.clearToken()
                }
            }
        }
        // [Sesion 10 | Logging] Oculta Authorization y no registra cuerpos con contrasenas.
        install(Logging) {
            logger = object : Logger {
                override fun log(message: String) {
                    // [Sesion 10 Autonoma | Logcat] Conserva el filtro KTOR en cada linea ya saneada.
                    message.lineSequence().forEach { println("KTOR: $it") }
                }
            }
            level = if (esDepuracion) LogLevel.HEADERS else LogLevel.NONE
            sanitizeHeader { it.equals(HttpHeaders.Authorization, ignoreCase = true) }
        }

        install(HttpTimeout) {
            requestTimeoutMillis = 15_000
            connectTimeoutMillis = 10_000
        }

        defaultRequest {
            url(baseUrl)
            contentType(ContentType.Application.Json)
        }
    }
}