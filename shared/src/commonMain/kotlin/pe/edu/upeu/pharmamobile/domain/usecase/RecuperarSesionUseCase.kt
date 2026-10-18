package pe.edu.upeu.pharmamobile.domain.usecase
import pe.edu.upeu.pharmamobile.domain.repository.AuthRepository
import pe.edu.upeu.pharmamobile.domain.model.Credenciales
// [Sesion 10 | Caso de uso] Ejecuta sesionGuardada mediante el contrato de dominio.
class RecuperarSesionUseCase(private val repository: AuthRepository) {
    suspend operator fun invoke() = repository.sesionGuardada()
}
