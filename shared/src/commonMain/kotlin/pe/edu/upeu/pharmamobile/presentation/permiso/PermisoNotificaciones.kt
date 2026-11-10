package pe.edu.upeu.pharmamobile.presentation.permiso
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.*
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import kotlinx.coroutines.launch
import org.koin.compose.koinInject
import pe.edu.upeu.pharmamobile.domain.permiso.*
@Composable fun PermisoNotificaciones() {
    val gestor: GestorPermisos = koinInject()
    val scope = rememberCoroutineScope()
    var estado by remember { mutableStateOf<EstadoPermiso>(EstadoPermiso.Denegado) }
    var ocupado by remember { mutableStateOf(false) }
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) { scope.launch { estado = gestor.estado(Permiso.NOTIFICACIONES) } }
    Column {
        Text("Notificaciones: " + when (estado) {
            EstadoPermiso.Concedido -> "Concedido"
            EstadoPermiso.Denegado -> "Denegado"
            EstadoPermiso.DenegadoParaSiempre -> "Denegado para siempre"
        })
        Text("Permite mostrar avisos de PharmaMobil. Puedes continuar usando el catálogo sin este permiso.")
        Button(enabled = !ocupado, onClick = {
            if (estado == EstadoPermiso.DenegadoParaSiempre) gestor.abrirAjustes()
            else if (estado == EstadoPermiso.Concedido) gestor.notificacionPrueba()
            else scope.launch {
                ocupado = true
                try { estado = gestor.solicitar(Permiso.NOTIFICACIONES) } finally { ocupado = false }
            }
        }) { Text(when (estado) {
            EstadoPermiso.Concedido -> "Probar notificación"
            EstadoPermiso.DenegadoParaSiempre -> "Abrir Ajustes"
            else -> "Permitir notificaciones"
        }) }
    }
}
