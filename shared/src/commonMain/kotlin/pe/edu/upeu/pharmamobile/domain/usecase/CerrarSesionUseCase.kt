package pe.edu.upeu.pharmamobile.domain.usecase
import pe.edu.upeu.pharmamobile.domain.repository.AuthRepository
import pe.edu.upeu.pharmamobile.domain.model.Credenciales
// [Sesion 10 | Caso de uso] Ejecuta cerrarSesion mediante el contrato de dominio.
class CerrarSesionUseCase(private val repository: AuthRepository) {
    suspend operator fun invoke() = repository.cerrarSesion()
}
