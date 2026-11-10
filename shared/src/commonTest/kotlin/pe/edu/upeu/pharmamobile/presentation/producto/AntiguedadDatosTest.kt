package pe.edu.upeu.pharmamobile.presentation.producto
import kotlin.test.*
class AntiguedadDatosTest {
    private val ahora = 1_800_000_000_000L
    @Test fun nuncaSincronizadoEsExplicito() { assertEquals("Nunca sincronizado", textoAntiguedad(null, ahora)) }
    @Test fun recienteMinutosYHoras() {
        assertEquals("Actualizado hace un momento", textoAntiguedad(ahora, ahora))
        assertEquals("Actualizado hace 1 minuto", textoAntiguedad(ahora - 60_000, ahora))
        assertEquals("Actualizado hace 2 horas", textoAntiguedad(ahora - 7_200_000, ahora))
    }
    @Test fun masDeUnDiaYPlural() {
        assertEquals("Actualizado hace 1 día", textoAntiguedad(ahora - 90_000_000, ahora))
        assertEquals("Actualizado hace 2 días", textoAntiguedad(ahora - 172_800_000, ahora))
    }
    @Test fun cambioDeRelojNoProduceTiempoNegativo() { assertEquals("Actualizado hace un momento", textoAntiguedad(ahora + 100_000, ahora)) }
}
