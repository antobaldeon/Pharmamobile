package pe.edu.upeu.pharmamobile.data.permiso
import android.Manifest
import android.app.*
import android.content.*
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import pe.edu.upeu.pharmamobile.domain.permiso.*

class GestorPermisosAndroid(private val contexto: Context) : GestorPermisos {
    private val preferencias = contexto.getSharedPreferences("permisos", Context.MODE_PRIVATE)
    private val mutex = Mutex()
    var explicar: (() -> Boolean)? = null
    var lanzar: (() -> Unit)? = null
    private var pendiente: CompletableDeferred<Boolean>? = null
    fun responder(concedido: Boolean) { pendiente?.complete(concedido) }
    fun desconectar() { pendiente?.cancel(); pendiente = null; explicar = null; lanzar = null }
    override suspend fun estado(permiso: Permiso): EstadoPermiso {
        val permitido = if (Build.VERSION.SDK_INT >= 33) ContextCompat.checkSelfPermission(contexto, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED
            else NotificationManagerCompat.from(contexto).areNotificationsEnabled()
        if (Build.VERSION.SDK_INT < 33 && !permitido) return EstadoPermiso.DenegadoParaSiempre
        return resolverEstadoPermiso(permitido, preferencias.getBoolean("notificaciones_pedido", false), explicar?.invoke() ?: true)
    }
    override suspend fun solicitar(permiso: Permiso): EstadoPermiso = mutex.withLock {
        if (estado(permiso) != EstadoPermiso.Denegado) return@withLock estado(permiso)
        val accion = lanzar ?: return@withLock EstadoPermiso.Denegado
        val espera = CompletableDeferred<Boolean>(); pendiente = espera
        preferencias.edit().putBoolean("notificaciones_pedido", true).apply()
        try { accion(); espera.await(); estado(permiso) } finally { pendiente = null }
    }
    override fun abrirAjustes() {
        contexto.startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:${contexto.packageName}")).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    }
    override fun notificacionPrueba() {
        if (!NotificationManagerCompat.from(contexto).areNotificationsEnabled()) return
        if (Build.VERSION.SDK_INT >= 26) contexto.getSystemService(NotificationManager::class.java).createNotificationChannel(NotificationChannel("sincronizacion", "Sincronización", NotificationManager.IMPORTANCE_DEFAULT))
        if (Build.VERSION.SDK_INT >= 33 && ContextCompat.checkSelfPermission(contexto, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) return
        NotificationManagerCompat.from(contexto).notify(13, NotificationCompat.Builder(contexto, "sincronizacion")
            .setSmallIcon(android.R.drawable.ic_popup_sync).setContentTitle("PharmaMobil")
            .setContentText("Los avisos de PharmaMobil están habilitados").setAutoCancel(true).build())
    }
}
