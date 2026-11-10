package pe.edu.upeu.pharmamobile.data.repository

import io.ktor.client.call.body
import io.ktor.client.engine.mock.*
import io.ktor.http.*
import io.ktor.utils.io.*
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.test.*
import kotlinx.io.IOException
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.data.remote.*
import pe.edu.upeu.pharmamobile.data.remote.dto.*
import pe.edu.upeu.pharmamobile.db.PharmaDb
import pe.edu.upeu.pharmamobile.domain.error.ErrorApiException
import pe.edu.upeu.pharmamobile.domain.model.Producto
import kotlin.test.*

/** Los seis casos exigidos usan SQL real en memoria y el adaptador HTTP real con MockEngine. */
class S11PruebasOfflineTest {
    private class Servidor {
        var conRed = true
        var rechazarDescarga = false
        val productos = mutableListOf<ProductoDto>()
        val peticiones = mutableListOf<String>()
        var altas = 0
        val engine = MockEngine { request ->
            if (!conRed) throw IOException("Sin conexión simulada")
            peticiones += request.method.value
            val headers = headersOf(HttpHeaders.ContentType, "application/json")
            when (request.method) {
                HttpMethod.Get -> {
                    if (rechazarDescarga) respond("{}", HttpStatusCode.InternalServerError, headers)
                    else {
                        // Una fila por página obliga al repositorio a descargar todas las páginas.
                        val pagina = request.url.parameters["pagina"]?.toInt() ?: 0
                        val contenido = productos.drop(pagina).take(1)
                        respond(Json.encodeToString(PaginaResponseDto(contenido, pagina, 1,
                            productos.size.toLong(), productos.size, pagina + 1 >= productos.size)), HttpStatusCode.OK, headers)
                    }
                }
                HttpMethod.Post -> {
                    val entrada = Json.decodeFromString<ProductoRequestDto>(request.body.toByteArray().decodeToString())
                    val creado = ProductoDto((productos.maxOfOrNull { it.id } ?: 0L) + 1,
                        entrada.nombre, entrada.precio, entrada.stock, entrada.estado, entrada.categoriaId)
                    productos += creado
                    altas++
                    respond(Json.encodeToString(creado), HttpStatusCode.Created, headers)
                }
                else -> error("Método inesperado: ${request.method}")
            }
        }
    }
    private suspend fun TestScope.conEntorno(bloque: suspend (ProductoLocal, Servidor, ProductoRepositorioOffline, ProductoRepositoryImpl, () -> Long, (Long) -> Unit) -> Unit) {
        val driver = crearDriverPruebas()
        val dispatcher = StandardTestDispatcher(testScheduler)
        val servidor = Servidor()
        val almacen = object : AlmacenSeguro {
            override fun guardarToken(token: String) = Unit
            override fun leerToken(): String? = null
            override fun borrarToken() = Unit
        }
        val cliente = crearHttpClient(servidor.engine, "https://pharmasoft.test/", almacen, GestorSesion(almacen))
        try {
            val local = ProductoLocal(PharmaDb(driver), dispatcher)
            val remoto = ProductoRepositoryImpl(ProductoApi(cliente))
            var tiempo = 1_800_000_000_000L
            val repo = ProductoRepositorioOffline(local, remoto, dispatcher) { tiempo }
            bloque(local, servidor, repo, remoto, { tiempo }, { tiempo = it })
        } finally { cliente.close(); driver.close() }
    }

    @Test fun prueba1SincronizacionConRedEmiteTodasLasPaginas() = runTest {
        conEntorno { local, servidor, repo, _, ahora, _ ->
            servidor.productos += ProductoDto(10, "A", 2.0, 3, true, 1)
            servidor.productos += ProductoDto(20, "B", 4.0, 8, false, 2)
            repo.sincronizar()
            assertEquals(listOf(10L, 20L), repo.observar().first().map { it.id })
            assertEquals(2, servidor.peticiones.count { it == "GET" })
            assertEquals(ahora(), local.ultimaSincronizacion())
        }
    }
    @Test fun prueba2RegistroSinRedQuedaPendienteYFlowLoEmite() = runTest {
        conEntorno { local, servidor, repo, _, _, _ ->
            servidor.conRed = false
            repo.registrar(Producto(0, "Sin red", 3.0, 7))
            val producto = repo.observar().first().single()
            assertTrue(producto.id < 0)
            assertTrue(producto.pendiente)
            assertEquals("Sin red", producto.nombre)
            assertEquals(1, local.pendientes().size)
            assertNull(local.ultimaSincronizacion())
        }
    }
    @Test fun prueba3ReconectarEnviaPendienteYConfirmaIdServidor() = runTest {
        conEntorno { local, servidor, repo, _, _, _ ->
            servidor.conRed = false
            repo.registrar(Producto(0, "Reconectar", 3.0, 7))
            servidor.conRed = true
            repo.sincronizar()
            assertEquals(listOf("POST", "GET"), servidor.peticiones)
            assertEquals(1, servidor.altas)
            val producto = repo.observar().first().single()
            assertTrue(producto.id > 0)
            assertFalse(producto.pendiente)
            assertTrue(local.pendientes().isEmpty())
        }
    }
    @Test fun prueba4BajadaNoBorraPendientes() = runTest {
        conEntorno { local, servidor, repo, remoto, _, _ ->
            servidor.conRed = false
            repo.registrar(Producto(0, "Local", 3.0, 7))
            servidor.conRed = true
            servidor.productos += ProductoDto(50, "Remoto", 5.0, 9, true, 1)
            // Se prueba específicamente la operación de bajada usada por el repositorio.
            local.reemplazarSincronizados(remoto.listar())
            val lista = repo.observar().first()
            assertEquals(2, lista.size)
            assertEquals("Local", lista.single { it.pendiente }.nombre)
            assertTrue(lista.any { it.id == 50L })
        }
    }
    @Test fun prueba5IdentificadoresLocalesYRemotosNoColisionan() = runTest {
        conEntorno { local, servidor, repo, remoto, _, _ ->
            servidor.conRed = false
            val a = repo.registrar(Producto(0, "Local A", 1.0, 1))
            val b = repo.registrar(Producto(0, "Local B", 2.0, 2))
            servidor.conRed = true
            servidor.productos += ProductoDto(1, "Servidor", 4.0, 4, true, 1)
            local.reemplazarSincronizados(remoto.listar())
            assertEquals(setOf(-1L, -2L, 1L), repo.observar().first().map { it.id }.toSet())
            assertNotEquals(a.id, b.id)
            assertEquals(3, local.listar().size)
        }
    }
    @Test fun prueba6SincronizarDosVecesNoDuplica() = runTest {
        conEntorno { _, servidor, repo, _, _, _ ->
            servidor.conRed = false
            repo.registrar(Producto(0, "Una sola alta", 3.0, 7))
            servidor.conRed = true
            repo.sincronizar()
            val primera = repo.observar().first()
            repo.sincronizar()
            assertEquals(primera, repo.observar().first())
            assertEquals(1, servidor.altas)
            assertEquals(1, servidor.productos.size)
        }
    }
    @Test fun falloDeSincronizacionNoModificaFechaCorrectaAnterior() = runTest {
        conEntorno { local, servidor, repo, _, ahora, cambiarHora ->
            repo.sincronizar()
            val anterior = ahora()
            cambiarHora(anterior + 172_800_000L)
            servidor.rechazarDescarga = true
            assertFailsWith<ErrorApiException> { repo.sincronizar() }
            assertEquals(anterior, repo.observarUltimaSincronizacion().first())
            assertEquals(anterior, local.ultimaSincronizacion())
        }
    }
}
