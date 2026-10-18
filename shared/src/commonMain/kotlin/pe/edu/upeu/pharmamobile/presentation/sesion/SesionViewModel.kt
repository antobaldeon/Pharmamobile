package pe.edu.upeu.pharmamobile.presentation.sesion
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import pe.edu.upeu.pharmamobile.data.local.GestorSesion
import pe.edu.upeu.pharmamobile.domain.model.Credenciales
import pe.edu.upeu.pharmamobile.domain.usecase.*
// [Sesion 10 | MVVM] Recupera sesion al arrancar y valida el formulario antes del login.
class SesionViewModel(private val iniciar: IniciarSesionUseCase, private val recuperar: RecuperarSesionUseCase,
    private val cerrar: CerrarSesionUseCase, gestor: GestorSesion) : ViewModel() {
    private val estado = MutableStateFlow(SesionUiState())
    val uiState = estado.asStateFlow()
    val sesion = gestor.sesion
    val aviso = gestor.aviso
    // [Sesion 10 Autonoma | Limpieza] Un 401 tambien elimina usuario, clave y errores de la sesion anterior.
    init {
        viewModelScope.launch {
            var habiaSesion = false
            sesion.collect { actual ->
                if (actual == null && habiaSesion) estado.value = SesionUiState(restaurando = false)
                habiaSesion = actual != null
            }
        }
        restaurar()
    }
    fun usuario(valor: String) { estado.update { it.copy(usuario = valor, error = null) } }
    fun clave(valor: String) { estado.update { it.copy(clave = valor, error = null) } }
    fun restaurar() { viewModelScope.launch {
        estado.update { it.copy(restaurando = true, error = null) }
        try { recuperar() } catch(e: CancellationException) { throw e }
        catch(e: Exception) { estado.update { it.copy(error = e.message) } }
        finally { estado.update { it.copy(restaurando = false) } }
    } }
    fun ingresar() {
        val actual = estado.value
        if(actual.cargando || actual.restaurando) return
        if(actual.usuario.isBlank() || actual.clave.isBlank()) {
            estado.update { it.copy(error = "Ingresa usuario y contraseña") }; return
        }
        viewModelScope.launch {
            estado.update { it.copy(cargando = true, error = null) }
            try { iniciar(Credenciales(actual.usuario, actual.clave)); estado.update { it.copy(clave = "") } }
            catch(e: CancellationException) { throw e }
            catch(e: Exception) { estado.update { it.copy(error = e.message) } }
            finally { estado.update { it.copy(cargando = false) } }
        }
    }
    fun salir() { viewModelScope.launch { cerrar(); estado.value = SesionUiState(restaurando = false) } }
}
