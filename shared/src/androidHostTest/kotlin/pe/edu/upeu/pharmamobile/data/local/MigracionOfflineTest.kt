package pe.edu.upeu.pharmamobile.data.local

import app.cash.sqldelight.driver.jdbc.sqlite.JdbcSqliteDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
import kotlin.test.*

class MigracionOfflineTest {
    @Test fun migrarDeVersionUnoConservaProductosYPendientes() {
        val driver = JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)
        try {
            driver.execute(null, "CREATE TABLE producto (id INTEGER NOT NULL PRIMARY KEY, nombre TEXT NOT NULL, precio REAL NOT NULL, stock INTEGER NOT NULL, activo INTEGER NOT NULL, categoriaId INTEGER NOT NULL, pendiente INTEGER NOT NULL DEFAULT 0)", 0)
            driver.execute(null, "INSERT INTO producto VALUES (-1, 'Pendiente anterior', 5.0, 2, 1, 1, 1)", 0)
            PharmaDb.Schema.migrate(driver, 1, PharmaDb.Schema.version)
            val local = ProductoLocal(PharmaDb(driver))
            assertEquals("Pendiente anterior", local.listar().single().nombre)
            assertTrue(local.listar().single().pendiente)
            assertNull(local.ultimaSincronizacion())
            local.reemplazarSincronizados(emptyList(), 123456L)
            assertEquals(123456L, ProductoLocal(PharmaDb(driver)).ultimaSincronizacion())
            assertEquals(1, local.pendientes().size)
        } finally { driver.close() }
    }
}
