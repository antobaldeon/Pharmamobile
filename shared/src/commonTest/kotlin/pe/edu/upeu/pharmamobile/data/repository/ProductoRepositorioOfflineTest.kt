package pe.edu.upeu.pharmamobile.data.repository

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.TestScope
import kotlinx.coroutines.test.runTest
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.db.PharmaDb
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.model.*
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository
import kotlin.test.*

class ProductoRepositorioOfflineTest {
    private suspend fun TestScope.conBase(bloque: suspend (ProductoLocal, RemotoFalso, ProductoRepositorioOffline) -> Unit) {
        val driver = crearDriverPruebas()
        try {
            val dispatcher = StandardTestDispatcher(testScheduler)
            val local = ProductoLocal(PharmaDb(driver), dispatcher)
            val remoto = RemotoFalso()
            bloque(local, remoto, ProductoRepositorioOffline(local, remoto, dispatcher))
        } finally { driver.close() }
    }

    @Test fun sinRedGuardaPendienteConIdNegativo() = runTest {
        conBase { local, remoto, repo ->
            remoto.conRed = false
            repo.registrar(Producto(0, "Ibuprofeno", 4.5, 20, categoriaId = 2))
            val p = repo.observar().first().single()
            assertTrue(p.id < 0)
            assertTrue(p.pendiente)
            assertEquals(2L, p.categoriaId)
            assertEquals(1, local.pendientes().size)
        }
    }
    @Test fun conRedDescargaEnLocal() = runTest {
        conBase { _, remoto, repo ->
            remoto.productos += Producto(1, "Paracetamol", 3.0, 10, activo = false)
            repo.sincronizar()
            assertEquals(remoto.productos, repo.observar().first())
        }
    }
    @Test fun reconectarSubeAntesDeBajarYNoDuplica() = runTest {
        conBase { local, remoto, repo ->
            remoto.conRed = false
            repo.registrar(Producto(0, "Amoxicilina", 8.0, 12))
            remoto.conRed = true
            remoto.eventos.clear()
            repo.sincronizar()
            assertEquals(listOf("subir", "bajar"), remoto.eventos)
            assertTrue(local.pendientes().isEmpty())
            val p = repo.observar().first().single()
            assertTrue(p.id > 0)
            assertFalse(p.pendiente)
            repo.sincronizar()
            assertEquals(1, remoto.creaciones)
            assertEquals(1, repo.observar().first().size)
        }
    }
    @Test fun falloEnSegundaSubidaConservaSoloElPendienteNoConfirmado() = runTest {
        conBase { local, remoto, repo ->
            remoto.conRed = false
            repo.registrar(Producto(0, "A", 1.0, 1))
            repo.registrar(Producto(0, "B", 2.0, 2))
            remoto.conRed = true
            remoto.fallarCreacion = 2
            assertFailsWith<ErrorApiException> { repo.sincronizar() }
            assertEquals(1, local.pendientes().size)
            assertEquals(2, local.listar().size)
            assertFalse("bajar" in remoto.eventos)
            remoto.fallarCreacion = null
            repo.sincronizar()
            assertEquals(2, remoto.productos.size)
            assertTrue(local.pendientes().isEmpty())
        }
    }
    @Test fun descargaNoBorraPendientesLocales() = runTest {
        conBase { local, _, _ ->
            local.guardarPendiente(Producto(0, "Local", 2.0, 1))
            local.reemplazarSincronizados(listOf(Producto(1, "Servidor", 5.0, 3)))
            assertEquals(2, local.listar().size)
            assertEquals(1, local.pendientes().size)
        }
    }
    @Test fun editaYEliminaUnPendienteSinRed() = runTest {
        conBase { _, remoto, repo ->
            remoto.conRed = false
            val creado = repo.registrar(Producto(0, "Local", 2.0, 1))
            repo.actualizar(creado.copy(nombre = "Editado"))
            assertEquals("Editado", repo.obtener(creado.id).nombre)
            repo.eliminar(creado.id)
            assertTrue(repo.observar().first().isEmpty())
        }
    }
    @Test fun perfilSeConservaParaReabrirSinRedYSeBorraAlSalir() = runTest {
        val driver = crearDriverPruebas()
        try {
            val base = PharmaDb(driver)
            val local = SesionLocal(base)
            val almacen = object : AlmacenSeguro {
                var valor: String? = "token"
                override fun guardarToken(token: String) { valor = token }
                override fun leerToken() = valor
                override fun borrarToken() { valor = null }
            }
            val sesion = Sesion("token", "admin", "Admin", setOf("CATALOGO_ESCRIBIR"))
            GestorSesion(almacen, local).activar(sesion)
            assertEquals(sesion, SesionLocal(base).leer("token"))
            GestorSesion(almacen, local).cerrar()
            assertNull(almacen.leerToken())
            assertNull(local.leer("token"))
        } finally { driver.close() }
    }

    private class RemotoFalso : ProductoRepository {
        var conRed = true
        var fallarCreacion: Int? = null
        var creaciones = 0
        private var intentos = 0
        val productos = mutableListOf<Producto>()
        val eventos = mutableListOf<String>()
        private fun red() { if (!conRed) throw ErrorApiException(ErrorApi.SinConexion) }
        override fun observar(): Flow<List<Producto>> = flowOf(productos.toList())
        override suspend fun sincronizar() = Unit
        override suspend fun listar(): List<Producto> { red(); eventos += "bajar"; return productos.toList() }
        override suspend fun registrar(producto: Producto): Producto {
            red()
            intentos++
            if (intentos == fallarCreacion) throw ErrorApiException(ErrorApi.SinConexion)
            eventos += "subir"
            creaciones++
            return producto.copy(id = (productos.maxOfOrNull { it.id } ?: 0L) + 1L, pendiente = false).also { productos += it }
        }
        override suspend fun obtener(id: Long): Producto { red(); return productos.first { it.id == id } }
        override suspend fun actualizar(producto: Producto): Producto { red(); productos[productos.indexOfFirst { it.id == producto.id }] = producto; return producto }
        override suspend fun eliminar(id: Long) { red(); productos.removeAll { it.id == id } }
    }
}
