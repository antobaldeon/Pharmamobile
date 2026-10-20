package pe.edu.upeu.pharmamobile.data.local
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.native.inMemoryDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
actual fun crearDriverPruebas(): SqlDriver = inMemoryDriver(PharmaDb.Schema)
