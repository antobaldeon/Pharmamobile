package pe.edu.upeu.pharmamobile.data.local
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.jdbc.sqlite.JdbcSqliteDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
actual fun crearDriverPruebas(): SqlDriver = JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY).also { PharmaDb.Schema.create(it) }
