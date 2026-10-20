package pe.edu.upeu.pharmamobile.data.local
import androidx.test.platform.app.InstrumentationRegistry
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.android.AndroidSqliteDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
actual fun crearDriverPruebas(): SqlDriver = AndroidSqliteDriver(PharmaDb.Schema, InstrumentationRegistry.getInstrumentation().targetContext, null)
