package pe.edu.upeu.pharmamobile.domain.model
sealed interface ResultadoEnvio {
    data class Transitorio(val motivo: String) : ResultadoEnvio
    data class Permanente(val motivo: String) : ResultadoEnvio
}
const val MAX_INTENTOS_ENVIO = 5L
fun esperaEnvio(intentos: Long): Long = 1000L shl (intentos - 1).coerceIn(0, 4).toInt()
