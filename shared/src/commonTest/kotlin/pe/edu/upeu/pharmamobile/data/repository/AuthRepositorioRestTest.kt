package pe.edu.upeu.pharmamobile.data.repository

import io.ktor.client.engine.mock.*
import io.ktor.client.request.*
import io.ktor.http.*
import kotlinx.coroutines.test.runTest
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.data.remote.*
import pe.edu.upeu.pharmamobile.domain.model.*
import pe.edu.upeu.pharmamobile.domain.error.*
import kotlin.test.*

// [Sesion 10 | Pruebas] Verifica el contrato JWT real sin depender de Oracle ni del emulador.
class AuthRepositorioRestTest {
    private class AlmacenPrueba(var token: String? = null) : AlmacenSeguro {
        override fun guardarToken(token: String) { this.token = token }
        override fun leerToken() = token
        override fun borrarToken() { token = null }
    }
    private val loginJson = """{"token":"nuevo-jwt","tipo":"Bearer","expiraEnSegundos":3600,"username":"admin","nombreCompleto":"Admin","roles":["ADMIN"],"permisos":["CATALOGO_ESCRIBIR"]}"""
    private val meJson = """{"username":"admin","empleadoNombre":"Admin","permisos":["CATALOGO_ESCRIBIR"]}"""
    private val headers = headersOf(HttpHeaders.ContentType, "application/json")

    @Test fun loginNoEnviaTokenAnteriorYRenuevaCache() = runTest {
        val almacen = AlmacenPrueba("anterior")
        val gestor = GestorSesion(almacen)
        val motor = MockEngine { request ->
            when(request.url.encodedPath) {
                "/api/v1/auth/login" -> {
                    assertNull(request.headers[HttpHeaders.Authorization])
                    respond(loginJson, HttpStatusCode.OK, headers)
                }
                else -> respond(meJson, HttpStatusCode.OK, headers)
            }
        }
        val cliente = crearHttpClient(motor, "https://backend.test/", almacen, gestor)
        try {
            val repository = AuthRepositorioRest(AuthApi(cliente), cliente, almacen, gestor)
            cliente.get("api/v1/auth/me")
            assertEquals("Bearer anterior", motor.requestHistory.last().headers[HttpHeaders.Authorization])
            val sesion = repository.iniciarSesion(Credenciales("admin", "Admin123"))
            assertTrue(sesion.puede("CATALOGO_ESCRIBIR"))
            cliente.get("api/v1/auth/me")
            assertEquals("Bearer nuevo-jwt", motor.requestHistory.last().headers[HttpHeaders.Authorization])
            repository.cerrarSesion()
            assertNull(almacen.token)
            assertNull(gestor.sesion.value)
            cliente.get("api/v1/auth/me")
            assertNull(motor.requestHistory.last().headers[HttpHeaders.Authorization])
        } finally { cliente.close() }
    }
    @Test fun restauraIdentidadDesdeMeConTokenGuardado() = runTest {
        val almacen = AlmacenPrueba("guardado")
        val gestor = GestorSesion(almacen)
        val motor = MockEngine { request ->
            assertEquals("Bearer guardado", request.headers[HttpHeaders.Authorization])
            respond(meJson, HttpStatusCode.OK, headers)
        }
        val cliente = crearHttpClient(motor, "https://backend.test/", almacen, gestor)
        try {
            val repository = AuthRepositorioRest(AuthApi(cliente), cliente, almacen, gestor)
            assertEquals("Admin", repository.sesionGuardada()?.nombreCompleto)
            assertEquals("admin", gestor.sesion.value?.usuario)
            assertEquals(1, motor.requestHistory.size)
        } finally { cliente.close() }
    }
    @Test fun sinPermisoConservaSesionPero401LaBorra() = runTest {
        val almacen = AlmacenPrueba("guardado")
        val gestor = GestorSesion(almacen)
        gestor.activar(Sesion("guardado", "almacen", "Almacen", setOf("CATALOGO_LEER")))
        var status = HttpStatusCode.Forbidden
        val motor = MockEngine { respond("{}", status, headers) }
        val cliente = crearHttpClient(motor, "https://backend.test/", almacen, gestor)
        try {
            val forbidden = ejecutarLlamada { cliente.get("api/v1/clientes") }.exceptionOrNull() as ErrorApiException
            assertEquals(ErrorApi.SinPermiso, forbidden.error)
            assertNotNull(gestor.sesion.value)
            assertEquals("guardado", almacen.token)
            status = HttpStatusCode.Unauthorized
            val unauthorized = ejecutarLlamada { cliente.get("api/v1/productos") }.exceptionOrNull() as ErrorApiException
            assertEquals(ErrorApi.SesionExpirada, unauthorized.error)
            assertNull(gestor.sesion.value)
            assertNull(almacen.token)
            assertNotNull(gestor.aviso.value)
        } finally { cliente.close() }
    }
    @Test fun loginInvalidoNoConfundeCredencialesConExpiracion() = runTest {
        val almacen = AlmacenPrueba()
        val gestor = GestorSesion(almacen)
        val motor = MockEngine { respond("{}", HttpStatusCode.Unauthorized, headers) }
        val cliente = crearHttpClient(motor, "https://backend.test/", almacen, gestor)
        try {
            val repository = AuthRepositorioRest(AuthApi(cliente), cliente, almacen, gestor)
            val error = assertFailsWith<ErrorSesionException> { repository.iniciarSesion(Credenciales("admin", "incorrecta")) }
            assertEquals(ErrorSesion.CredencialesInvalidas, error.error)
            assertNull(almacen.token)
            assertNull(gestor.aviso.value)
        } finally { cliente.close() }
    }
}
