package pe.edu.upeu.pharmamobile.domain.permiso
enum class Permiso { NOTIFICACIONES }
sealed interface EstadoPermiso {
    data object Concedido : EstadoPermiso
    data object Denegado : EstadoPermiso
    data object DenegadoParaSiempre : EstadoPermiso
}
interface GestorPermisos {
    suspend fun estado(permiso: Permiso): EstadoPermiso
    suspend fun solicitar(permiso: Permiso): EstadoPermiso
    fun abrirAjustes()
    fun notificacionPrueba()
}
fun resolverEstadoPermiso(concedido: Boolean, pedido: Boolean, explicar: Boolean): EstadoPermiso = when {
    concedido -> EstadoPermiso.Concedido
    !pedido || explicar -> EstadoPermiso.Denegado
    else -> EstadoPermiso.DenegadoParaSiempre
}
