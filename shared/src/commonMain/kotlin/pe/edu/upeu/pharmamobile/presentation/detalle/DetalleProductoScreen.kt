package pe.edu.upeu.pharmamobile.presentation.detalle

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.material3.Card
import pe.edu.upeu.pharmamobile.presentation.producto.ProductoUi

@Composable
fun DetalleProductoScreen(
    producto: ProductoUi,
    onCompartir: () -> Unit,
    onCerrar: () -> Unit
) {
    Dialog(onDismissRequest = onCerrar) {
        Card {
            Column(Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(producto.producto.nombre)
                Text(producto.precioFormateado)
                Text("Stock: ${producto.producto.stock}")
                Text(if (producto.producto.activo) "Activo" else "Inactivo")
                Button(onClick = onCompartir) { Text("Compartir") }
                OutlinedButton(onClick = onCerrar) { Text("Cerrar") }
            }
        }
    }
}
