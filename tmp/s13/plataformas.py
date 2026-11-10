from pathlib import Path
def w(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def e(p,a,c):
 s=p.read_text(encoding='utf-8');assert a in s,(p,a);w(p,s.replace(a,c))
b=Path('shared/src/commonMain/kotlin/pe/edu/upeu/pharmamobile')
a=Path('shared/src/androidMain/kotlin/pe/edu/upeu/pharmamobile')
w(a/'data/permiso/GestorPermisosAndroid.kt','''package pe.edu.upeu.pharmamobile.data.permiso
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
''')
p=Path('androidApp/src/main/kotlin/pe/edu/upeu/pharmamobile/MainActivity.kt')
e(p,'class MainActivity : ComponentActivity() {','''class MainActivity : ComponentActivity() {
    private val permisos by lazy { org.koin.core.context.GlobalContext.get().get<pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosAndroid>() }
    private val solicitud = registerForActivityResult(androidx.activity.result.contract.ActivityResultContracts.RequestPermission()) { permisos.responder(it) }
    override fun onDestroy() { permisos.desconectar(); super.onDestroy() }''')
e(p,'        super.onCreate(savedInstanceState)','''        super.onCreate(savedInstanceState)
        permisos.explicar = { androidx.core.app.ActivityCompat.shouldShowRequestPermissionRationale(this, android.Manifest.permission.POST_NOTIFICATIONS) }
        permisos.lanzar = { solicitud.launch(android.Manifest.permission.POST_NOTIFICATIONS) }''')
p=Path('androidApp/src/main/AndroidManifest.xml');e(p,'    <uses-permission android:name="android.permission.INTERNET" />','    <uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />')
p=a/'di/PlatformModule.android.kt';e(p,'actual val platformModule: Module = module {','''actual val platformModule: Module = module {
    single { pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosAndroid(androidContext()) }
    single<pe.edu.upeu.pharmamobile.domain.permiso.GestorPermisos> { get<pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosAndroid>() }''')
# Native permission implementation.
i=Path('shared/src/iosMain/kotlin/pe/edu/upeu/pharmamobile')
w(i/'data/permiso/GestorPermisosIos.kt','''@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)
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
''')
p=i/'di/PlatformModule.ios.kt';e(p,'actual val platformModule: Module = module {','''actual val platformModule: Module = module {
    single<pe.edu.upeu.pharmamobile.domain.permiso.GestorPermisos> { pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosIos() }''')
w(b/'domain/port/Telemetria.kt','''package pe.edu.upeu.pharmamobile.domain.port
interface Telemetria {
    fun registrarError(e: Throwable, contexto: Map<String, String> = emptyMap())
    fun registrarEvento(nombre: String, datos: Map<String, String> = emptyMap())
}
''')
w(b/'data/firebase/TelemetriaFirebase.kt','''package pe.edu.upeu.pharmamobile.data.firebase
import dev.gitlive.firebase.Firebase
import dev.gitlive.firebase.crashlytics.crashlytics
import pe.edu.upeu.pharmamobile.domain.port.Telemetria
/** Solo categorías técnicas permitidas; no se envían mensajes, tokens ni nombres. */
class TelemetriaFirebase : Telemetria {
    override fun registrarError(e: Throwable, contexto: Map<String, String>) {
        runCatching { Firebase.crashlytics.recordException(IllegalStateException("pharmamobil_error_tecnico")) }
    }
    override fun registrarEvento(nombre: String, datos: Map<String, String>) {
        if (nombre in setOf("sincronizacion_correcta", "sincronizacion_fallida")) runCatching { Firebase.crashlytics.log(nombre) }
    }
}
''')
p=b/'di/AppModule.kt';e(p,'val dataModule = module {','''val dataModule = module {
    single<pe.edu.upeu.pharmamobile.domain.port.Telemetria> { pe.edu.upeu.pharmamobile.data.firebase.TelemetriaFirebase() }''')
e(p,'ProductoRepositorioOffline(get(), get<ProductoRepositoryImpl>())','ProductoRepositorioOffline(get(), get<ProductoRepositoryImpl>(), telemetria = get())')
p=b/'data/repository/ProductoRepositorioOffline.kt'
# append optional before clock to preserve trailing lambda call sites
s=p.read_text(encoding='utf-8').replace('    private val ahora: () -> Long', '    private val telemetria: pe.edu.upeu.pharmamobile.domain.port.Telemetria? = null,\n    private val ahora: () -> Long')
s=s.replace('                val resultado = error.resultadoEnvio()','                telemetria?.registrarEvento("sincronizacion_fallida")\n                val resultado = error.resultadoEnvio()')
s=s.replace('        local.reemplazarSincronizados(productos, ahora())','        local.reemplazarSincronizados(productos, ahora())\n        telemetria?.registrarEvento("sincronizacion_correcta")');w(p,s)
p=Path('shared/build.gradle.kts');e(p,'        commonMain.dependencies {','        commonMain.dependencies {\n            implementation("dev.gitlive:firebase-crashlytics:2.7.0")')
p=Path('gradle/libs.versions.toml');e(p,'[plugins]','[plugins]\ngoogleServices = { id = "com.google.gms.google-services", version = "4.4.4" }\nfirebaseCrashlytics = { id = "com.google.firebase.crashlytics", version = "3.0.6" }')
p=Path('build.gradle.kts');e(p,'plugins {','plugins {\n    alias(libs.plugins.googleServices) apply false\n    alias(libs.plugins.firebaseCrashlytics) apply false')
p=Path('androidApp/build.gradle.kts');e(p,'    alias(libs.plugins.androidApplication)','    alias(libs.plugins.googleServices) apply false\n    alias(libs.plugins.firebaseCrashlytics) apply false\n    alias(libs.plugins.androidApplication)')
e(p,'kotlin {','''// La app sigue compilando sin inventar credenciales de Firebase.
if (file("google-services.json").exists()) {
    apply(plugin = "com.google.gms.google-services")
    apply(plugin = "com.google.firebase.crashlytics")
}

kotlin {''')
