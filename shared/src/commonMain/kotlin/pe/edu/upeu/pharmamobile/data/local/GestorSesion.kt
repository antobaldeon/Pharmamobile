package pe.edu.upeu.pharmamobile.data.local
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import pe.edu.upeu.pharmamobile.domain.model.Sesion
// [Sesion 10 | Estado global] Propaga un 401 de cualquier pantalla hasta la puerta de login.
class GestorSesion(private val almacen: AlmacenSeguro) {
    private val estado = MutableStateFlow<Sesion?>(null)
    val sesion = estado.asStateFlow()
    private val mensaje = MutableStateFlow<String?>(null)
    val aviso = mensaje.asStateFlow()
    // [Sesion 10 | Cambio de usuario] Identifica cada ingreso sin usar el token como clave de UI.
    var ingreso: Long = 0
        private set
    fun activar(sesion: Sesion) { ingreso++; mensaje.value = null; estado.value = sesion }
    fun cerrar(aviso: String? = null) { almacen.borrarToken(); estado.value = null; mensaje.value = aviso }
}
