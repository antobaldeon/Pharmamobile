package pe.edu.upeu.pharmamobile.data.local

import app.cash.sqldelight.db.SqlDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
import app.cash.sqldelight.driver.native.NativeSqliteDriver

class CreadorDeDriverIos : CreadorDeDriver {
    override fun crear(): SqlDriver = NativeSqliteDriver(PharmaDb.Schema, "pharma.db")
}
