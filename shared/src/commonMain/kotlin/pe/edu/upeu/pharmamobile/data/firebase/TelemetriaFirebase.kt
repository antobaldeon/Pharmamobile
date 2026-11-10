package pe.edu.upeu.pharmamobile.data.firebase
import dev.gitlive.firebase.Firebase
import dev.gitlive.firebase.crashlytics.crashlytics
import pe.edu.upeu.pharmamobile.domain.port.Telemetria
/** Solo categorías técnicas permitidas; no se envían mensajes, tokens ni nombres. */
class TelemetriaFirebase : Telemetria {
    override fun registrarError(e: Throwable, contexto: Map<String, String>) {
        runCatching { Firebase.crashlytics.recordException(IllegalStateException("pharmamobil_error_tecnico")) }
    }
    override fun registrarEvento(nombre: String, datos: Map<String, String>) {
        if (nombre in setOf("sincronizacion_correcta", "sincronizacion_fallida")) runCatching { Firebase.crashlytics.log(nombre) }
    }
}
