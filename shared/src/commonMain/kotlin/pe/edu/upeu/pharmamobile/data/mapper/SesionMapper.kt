package pe.edu.upeu.pharmamobile.data.mapper
import pe.edu.upeu.pharmamobile.data.remote.dto.*
import pe.edu.upeu.pharmamobile.domain.model.Sesion
// [Sesion 10 | Mapeo y roles] Conserva los roles del servidor para el saludo al ingresar y reabrir la app.
// [Sesion 10 | Mapeo] Convierte respuestas REST al modelo independiente de dominio.
fun LoginResponseDto.aSesion() = Sesion(token, username, nombreCompleto, permisos.toSet(), roles)
fun UsuarioActualDto.aSesion(token: String) = Sesion(token, username, empleadoNombre, permisos.toSet(), roles)
