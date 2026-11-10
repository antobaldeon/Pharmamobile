package pe.edu.upeu.pharmamobile.data.repository
import io.ktor.client.engine.mock.*
import io.ktor.http.*
import kotlinx.coroutines.test.*
import kotlinx.coroutines.flow.first
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.data.remote.*
import pe.edu.upeu.pharmamobile.db.PharmaDb
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.model.*
import pe.edu.upeu.pharmamobile.domain.permiso.*
import kotlin.test.*

class S13IntegradorTest {
    @Test fun permisosDistinguenPrimeraSolicitudDenegacionYConcesion() {
        assertEquals(EstadoPermiso.Denegado, resolverEstadoPermiso(false, false, false))
        assertEquals(EstadoPermiso.Denegado, resolverEstadoPermiso(false, true, true))
        assertEquals(EstadoPermiso.DenegadoParaSiempre, resolverEstadoPermiso(false, true, false))
        assertEquals(EstadoPermiso.Concedido, resolverEstadoPermiso(true, true, false))
    }
    @Test fun gestorFalsoPermiteProbarLosTresEstadosSinDispositivo() = runTest {
        val falso = object : GestorPermisos {
            var actual: EstadoPermiso = EstadoPermiso.Denegado
            var ajustes = false
            override suspend fun estado(permiso: Permiso) = actual
            override suspend fun solicitar(permiso: Permiso): EstadoPermiso { actual = EstadoPermiso.Concedido; return actual }
            override fun abrirAjustes() { ajustes = true }
            override fun notificacionPrueba() = Unit
        }
        assertEquals(EstadoPermiso.Denegado, falso.estado(Permiso.NOTIFICACIONES))
        assertEquals(EstadoPermiso.Concedido, falso.solicitar(Permiso.NOTIFICACIONES))
        falso.actual = EstadoPermiso.DenegadoParaSiempre
        falso.abrirAjustes()
        assertTrue(falso.ajustes)
        assertEquals(EstadoPermiso.DenegadoParaSiempre, falso.estado(Permiso.NOTIFICACIONES))
    }
    @Test fun esperaCreceConLimite() {
        assertEquals(listOf(1000L, 2000L, 4000L, 8000L, 16000L), (1L..5L).map(::esperaEnvio))
        assertEquals(16000L, esperaEnvio(100))
    }
    @Test fun erroresSeClasifican() {
        assertIs<ResultadoEnvio.Transitorio>(ErrorApiException(ErrorApi.SinConexion).resultadoEnvio())
        assertIs<ResultadoEnvio.Transitorio>(ErrorApiException(ErrorApi.TiempoAgotado).resultadoEnvio())
        assertIs<ResultadoEnvio.Permanente>(ErrorApiException(ErrorApi.Conflicto("Conflicto")).resultadoEnvio())
        assertIs<ResultadoEnvio.Permanente>(ErrorApiException(ErrorApi.SesionExpirada).resultadoEnvio())
    }
    private suspend fun TestScope.caso(status: HttpStatusCode, bloque: suspend (ProductoLocal, ProductoRepositorioOffline, () -> Int) -> Unit) {
        val driver = crearDriverPruebas()
        val dispatcher = StandardTestDispatcher(testScheduler)
        var posts = 0
        val motor = MockEngine { request ->
            if (request.method == HttpMethod.Post) { posts++; respond("{}", status, headersOf(HttpHeaders.ContentType,"application/json")) }
            else respond("{\"contenido\":[],\"ultima\":true}", HttpStatusCode.OK, headersOf(HttpHeaders.ContentType,"application/json"))
        }
        val almacen = object : AlmacenSeguro {
            override fun guardarToken(token: String) = Unit
            override fun leerToken(): String? = null
            override fun borrarToken() = Unit
        }
        val cliente = crearHttpClient(motor, "https://test.local/", almacen, GestorSesion(almacen))
        try {
            val local = ProductoLocal(PharmaDb(driver),dispatcher)
            val repo = ProductoRepositorioOffline(local, ProductoRepositoryImpl(ProductoApi(cliente)),dispatcher)
            bloque(local, repo) { posts }
        } finally { cliente.close(); driver.close() }
    }
    @Test fun falloTransitorioSumaIntentoSinBucleAutomatico() = runTest {
        caso(HttpStatusCode.ServiceUnavailable) { local, repo, posts ->
            repo.registrar(Producto(0,"Prueba",1.0,1))
            assertEquals(1L, local.pendientes().single().intentos)
            assertEquals(1, posts())
            assertTrue(local.pendientes().single().ultimoError != null)
        }
    }
    @Test fun validacionRemotaLlegaAlFormularioYConservaLaFilaFallida() = runTest {
        caso(HttpStatusCode.BadRequest) { local, repo, posts ->
            val error = assertFailsWith<ErrorApiException> {
                repo.registrar(Producto(0,"Prueba",1.0,1))
            }
            assertIs<ErrorApi.Validacion>(error.error)
            assertEquals(5L, local.pendientes().single().intentos)
            assertEquals("Prueba", local.pendientes().single().nombre)
            repo.sincronizar()
            assertEquals(1, posts())
        }
    }
    @Test fun permanenteQuedaFallidoYNoSeReenviaAlSincronizar() = runTest {
        caso(HttpStatusCode.Conflict) { local, repo, posts ->
            repo.registrar(Producto(0,"Prueba",1.0,1))
            repo.sincronizar()
            assertEquals(5L, local.pendientes().single().intentos)
            assertEquals(1, posts())
            assertTrue(repo.observar().first().single().pendiente)
        }
    }
    @Test fun cincoIntentosExplicitosAgotanLaFila() = runTest {
        caso(HttpStatusCode.ServiceUnavailable) { local, repo, posts ->
            repo.registrar(Producto(0,"Prueba",1.0,1))
            repeat(4) { assertFailsWith<ErrorApiException> { repo.sincronizar() } }
            repo.sincronizar()
            assertEquals(5L, local.pendientes().single().intentos)
            assertEquals(5, posts())
            assertEquals(15_000L, testScheduler.currentTime)
        }
    }
}
