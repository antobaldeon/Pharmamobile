package pe.edu.upeu.pharmamobile.presentation.sesion
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
// [Sesion 10 | Pantalla] Muestra validacion, carga y aviso de expiracion sin exponer el token.
@Composable fun LoginScreen(viewModel: SesionViewModel) {
    val estado by viewModel.uiState.collectAsState()
    val aviso by viewModel.aviso.collectAsState()
    val local: pe.edu.upeu.pharmamobile.data.local.ProductoLocal = org.koin.compose.koinInject()
    val productos by remember(local) { local.observar() }.collectAsState(initial = null)
    val ultima by remember(local) { local.observarUltimaSincronizacion() }.collectAsState(initial = null)
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(Modifier.widthIn(max = 420.dp).fillMaxWidth().verticalScroll(rememberScrollState()).padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Text("PharmaMobil", style = MaterialTheme.typography.headlineLarge)
            Text("Iniciar sesión", style = MaterialTheme.typography.titleLarge)
            if (productos?.isEmpty() == true && !estado.restaurando) {
                Text("No hay productos guardados en este dispositivo. Para la primera descarga, inicia sesión con conexión.")
                pe.edu.upeu.pharmamobile.presentation.producto.AntiguedadDatos(ultima)
            }
            if(estado.restaurando) {
                CircularProgressIndicator()
                Text("Comprobando sesión guardada…")
            } else {
                OutlinedTextField(estado.usuario, viewModel::usuario, label = { Text("Usuario") },
                    singleLine = true, enabled = !estado.cargando, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(estado.clave, viewModel::clave, label = { Text("Contraseña") },
                    visualTransformation = PasswordVisualTransformation(), singleLine = true,
                    enabled = !estado.cargando, modifier = Modifier.fillMaxWidth())
                (estado.error ?: aviso)?.let { Text(it, color = MaterialTheme.colorScheme.error) }
                Button(viewModel::ingresar, enabled = !estado.cargando, modifier = Modifier.fillMaxWidth()) {
                    Text(if(estado.cargando) "Ingresando…" else "Ingresar")
                }
                TextButton(viewModel::restaurar, enabled = !estado.cargando) { Text("Reintentar sesión guardada") }
            }
        }
    }
}
