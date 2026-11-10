@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)
package pe.edu.upeu.pharmamobile.data.permiso
import kotlin.coroutines.resume
import kotlinx.coroutines.suspendCancellableCoroutine
import platform.UserNotifications.*
import platform.Foundation.NSURL
import platform.UIKit.UIApplication
import platform.UIKit.UIApplicationOpenSettingsURLString
import pe.edu.upeu.pharmamobile.domain.permiso.*
class GestorPermisosIos : GestorPermisos {
    private val centro = UNUserNotificationCenter.currentNotificationCenter()
    override suspend fun estado(permiso: Permiso): EstadoPermiso = suspendCancellableCoroutine { c ->
        centro.getNotificationSettingsWithCompletionHandler { ajustes ->
            val estado = when (ajustes?.authorizationStatus) {
                UNAuthorizationStatusAuthorized, UNAuthorizationStatusProvisional -> EstadoPermiso.Concedido
                UNAuthorizationStatusDenied -> EstadoPermiso.DenegadoParaSiempre
                else -> EstadoPermiso.Denegado
            }
            if (c.isActive) c.resume(estado)
        }
    }
    override suspend fun solicitar(permiso: Permiso): EstadoPermiso {
        if (estado(permiso) != EstadoPermiso.Denegado) return estado(permiso)
        suspendCancellableCoroutine<Boolean> { c ->
            centro.requestAuthorizationWithOptions(UNAuthorizationOptionAlert or UNAuthorizationOptionSound or UNAuthorizationOptionBadge) { ok, _ -> if (c.isActive) c.resume(ok) }
        }
        return estado(permiso)
    }
    override fun abrirAjustes() { NSURL.URLWithString(UIApplicationOpenSettingsURLString)?.let { UIApplication.sharedApplication.openURL(it) } }
    override fun notificacionPrueba() {
        val contenido = UNMutableNotificationContent().apply { setTitle("PharmaMobil"); setBody("Los avisos están habilitados") }
        centro.addNotificationRequest(UNNotificationRequest.requestWithIdentifier("prueba", contenido, UNTimeIntervalNotificationTrigger.triggerWithTimeInterval(2.0, false)), null)
    }
}
