package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.compose.material3.Text
import androidx.compose.runtime.*
import kotlinx.coroutines.delay
import kotlin.time.Clock

fun textoAntiguedad(ultima: Long?, ahora: Long): String {
    if (ultima == null) return "Nunca sincronizado"
    val segundos = if (ahora <= ultima) 0L else (ahora - ultima) / 1000
    return when {
        segundos < 60 -> "Actualizado hace un momento"
        segundos < 3600 -> {
            val n = segundos / 60
            "Actualizado hace $n ${if (n == 1L) "minuto" else "minutos"}"
        }
        segundos < 86400 -> {
            val n = segundos / 3600
            "Actualizado hace $n ${if (n == 1L) "hora" else "horas"}"
        }
        else -> {
            val n = segundos / 86400
            "Actualizado hace $n ${if (n == 1L) "día" else "días"}"
        }
    }
}

@Composable
fun AntiguedadDatos(ultima: Long?) {
    var ahora by remember { mutableStateOf(Clock.System.now().toEpochMilliseconds()) }
    LaunchedEffect(ultima) {
        while (true) {
            ahora = Clock.System.now().toEpochMilliseconds()
            delay(60_000)
        }
    }
    Text(textoAntiguedad(ultima, ahora))
}
