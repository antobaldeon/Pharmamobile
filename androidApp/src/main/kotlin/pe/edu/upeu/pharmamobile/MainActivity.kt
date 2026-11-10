package pe.edu.upeu.pharmamobile

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import pe.edu.upeu.pharmamobil.App

class MainActivity : ComponentActivity() {
    private val permisos by lazy { org.koin.core.context.GlobalContext.get().get<pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosAndroid>() }
    private val solicitud = registerForActivityResult(androidx.activity.result.contract.ActivityResultContracts.RequestPermission()) { permisos.responder(it) }
    override fun onDestroy() { permisos.desconectar(); super.onDestroy() }
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        if ((applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0 &&
            intent.getBooleanExtra("s13_prueba_crashlytics", false)) {
            intent.removeExtra("s13_prueba_crashlytics")
            pe.edu.upeu.pharmamobile.data.firebase.PruebaCrashlytics.registrar()
        }
        permisos.explicar = { androidx.core.app.ActivityCompat.shouldShowRequestPermissionRationale(this, android.Manifest.permission.POST_NOTIFICATIONS) }
        permisos.lanzar = { solicitud.launch(android.Manifest.permission.POST_NOTIFICATIONS) }

        setContent {
            App()
        }
    }
}

@Preview
@Composable
fun AppAndroidPreview() {
    App()
}