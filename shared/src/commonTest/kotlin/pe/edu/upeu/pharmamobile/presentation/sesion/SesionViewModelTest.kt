package pe.edu.upeu.pharmamobile.presentation.sesion
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import pe.edu.upeu.pharmamobile.data.local.*
import pe.edu.upeu.pharmamobile.domain.model.*
import pe.edu.upeu.pharmamobile.domain.repository.AuthRepository
import pe.edu.upeu.pharmamobile.domain.usecase.*
import kotlin.test.*
// [Sesion 10 Autonoma | Regresion UI] La invalidacion remota tambien limpia el formulario anterior.
@OptIn(ExperimentalCoroutinesApi::class)
class SesionViewModelTest {
    private val dispatcher = StandardTestDispatcher()
    @BeforeTest fun preparar() { Dispatchers.setMain(dispatcher) }
    @AfterTest fun terminar() { Dispatchers.resetMain() }
    @Test fun un401LimpiaUsuarioYClaveYConservaAviso() = runTest {
        val almacen = object : AlmacenSeguro {
            override fun guardarToken(token: String) {}
            override fun leerToken(): String? = null
            override fun borrarToken() {}
        }
        val gestor = GestorSesion(almacen)
        val repo = object : AuthRepository {
            override suspend fun iniciarSesion(credenciales: Credenciales): Sesion {
                val sesion = Sesion("token", credenciales.usuario, "Usuario", emptySet())
                gestor.activar(sesion); return sesion
            }
            override suspend fun sesionGuardada(): Sesion? = null
            override suspend fun cerrarSesion() { gestor.cerrar() }
        }
        val vm = SesionViewModel(IniciarSesionUseCase(repo), RecuperarSesionUseCase(repo), CerrarSesionUseCase(repo), gestor)
        advanceUntilIdle()
        vm.usuario("admin"); vm.clave("clave"); vm.ingresar()
        advanceUntilIdle()
        assertNotNull(vm.sesion.value)
        gestor.cerrar("Sesion expirada")
        advanceUntilIdle()
        assertEquals("", vm.uiState.value.usuario)
        assertEquals("", vm.uiState.value.clave)
        assertEquals("Sesion expirada", vm.aviso.value)
        assertNull(vm.sesion.value)
    }
}
