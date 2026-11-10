package pe.edu.upeu.pharmamobile.data.firebase

import android.util.Log
import com.google.firebase.FirebaseApp
import com.google.firebase.crashlytics.FirebaseCrashlytics

/** Invocada únicamente por la Activity debug con una acción explícita de prueba. */
object PruebaCrashlytics {
    fun registrar() {
        try {
            FirebaseApp.getInstance()
            val crashlytics = FirebaseCrashlytics.getInstance()
            crashlytics.log("s13_prueba_controlada")
            crashlytics.recordException(IllegalStateException("S13_ERROR_CONTROLADO_NO_FATAL"))
            Log.i("S13_CRASHLYTICS", "Error de prueba no fatal registrado en el SDK")
            crashlytics.sendUnsentReports()
        } catch (error: Exception) {
            Log.e("S13_CRASHLYTICS", "No se pudo registrar la prueba: ${error.javaClass.simpleName}")
        }
    }
}
