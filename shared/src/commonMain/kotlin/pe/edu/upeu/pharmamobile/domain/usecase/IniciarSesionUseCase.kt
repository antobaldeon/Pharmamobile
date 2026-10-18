package pe.edu.upeu.pharmamobile.domain.usecase
import pe.edu.upeu.pharmamobile.domain.repository.AuthRepository
import pe.edu.upeu.pharmamobile.domain.model.Credenciales
// [Sesion 10 | Caso de uso] Ejecuta iniciarSesion mediante el contrato de dominio.
class IniciarSesionUseCase(private val repository: AuthRepository) {
    suspend operator fun invoke(credenciales: Credenciales) = repository.iniciarSesion(credenciales)
}
