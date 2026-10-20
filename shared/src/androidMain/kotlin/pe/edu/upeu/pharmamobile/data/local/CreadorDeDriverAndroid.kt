package pe.edu.upeu.pharmamobile.data.local

import app.cash.sqldelight.db.SqlDriver
import pe.edu.upeu.pharmamobile.db.PharmaDb
import android.content.Context
import app.cash.sqldelight.driver.android.AndroidSqliteDriver

class CreadorDeDriverAndroid(private val contexto: Context) : CreadorDeDriver {
    override fun crear(): SqlDriver = AndroidSqliteDriver(PharmaDb.Schema, contexto, "pharma.db")
}
