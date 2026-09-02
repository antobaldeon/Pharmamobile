package pe.edu.upeu.pharmamobile.Domain.presentation.Producto

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.ListItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import pe.edu.upeu.pharmamobile.Domain.model.Producto

// AGREGADO (Reto 02): Clasifica el inventario en las tres vistas solicitadas por la guía.
private enum class InventarioTab(val titulo: String) {
    Activos("Activos"),
    Inactivos("Inactivos"),
    BajoStock("Bajo stock")
}

// MODIFICADO (Reto 02): Recibe el inventario compartido y registra los nuevos productos en la lista.
@Composable
fun ProductoScreen(
    inventario: List<Producto>,
    onProductoRegistrado: (Producto) -> Unit
) {
    var nombre by remember { mutableStateOf("") }
    var precio by remember { mutableStateOf("") }
    var stock by remember { mutableStateOf("") }
    var mensaje by remember { mutableStateOf("") }
    var intentoRegistrar by remember { mutableStateOf(false) }
    var errorNombre by remember { mutableStateOf(false) }
    var errorPrecio by remember { mutableStateOf(false) }
    var errorStock by remember { mutableStateOf(false) }

    // AGREGADO (Reto 02): Conserva qué clasificación del inventario está viendo el usuario.
    var tabSeleccionada by remember { mutableStateOf(InventarioTab.Activos) }

    // AGREGADO (Reto 02): Stock 0 también se considera Bajo stock, como pide la guía.
    val productosFiltrados = when (tabSeleccionada) {
        InventarioTab.Activos -> inventario.filter { it.activo }
        InventarioTab.Inactivos -> inventario.filter { !it.activo }
        InventarioTab.BajoStock -> inventario.filter { it.stock <= 5 }
    }

    fun registrar() {
        intentoRegistrar = true
        errorNombre = false
        errorPrecio = false
        errorStock = false

        val precioDouble = precio.toDoubleOrNull()
        val stockInt = stock.toIntOrNull()

        when {
            nombre.isBlank() -> {
                errorNombre = true
                mensaje = "Nombre obligatorio"
            }
            precioDouble == null -> {
                errorPrecio = true
                mensaje = "Precio inválido"
            }
            precioDouble <= 0.0 -> {
                errorPrecio = true
                mensaje = "El precio debe ser mayor a 0"
            }
            stockInt == null -> {
                errorStock = true
                mensaje = "Stock debe ser un número entero"
            }
            stockInt < 0 -> {
                errorStock = true
                mensaje = "Stock no puede ser negativo"
            }
            else -> {
                // MODIFICADO (Reto 02): El registro actualiza las Tabs además de mostrar confirmación.
                onProductoRegistrado(
                    Producto(
                        id = (inventario.maxOfOrNull { it.id } ?: 0L) + 1L,
                        nombre = nombre,
                        precio = precioDouble,
                        stock = stockInt,
                        activo = true
                    )
                )
                mensaje = "Producto registrado correctamente"
                nombre = ""
                precio = ""
                stock = ""
                intentoRegistrar = false
            }
        }
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Registro de Producto")

        OutlinedTextField(
            value = nombre,
            onValueChange = { nombre = it },
            label = { Text("Nombre") },
            isError = intentoRegistrar && errorNombre,
            supportingText = { if (intentoRegistrar && errorNombre) Text(mensaje) },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = precio,
            onValueChange = { precio = it },
            label = { Text("Precio") },
            isError = intentoRegistrar && errorPrecio,
            supportingText = { if (intentoRegistrar && errorPrecio) Text(mensaje) },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = stock,
            onValueChange = { stock = it },
            label = { Text("Stock") },
            isError = intentoRegistrar && errorStock,
            supportingText = { if (intentoRegistrar && errorStock) Text(mensaje) },
            modifier = Modifier.fillMaxWidth()
        )
        Button(onClick = ::registrar, modifier = Modifier.fillMaxWidth()) {
            Text("Registrar")
        }
        if (mensaje.isNotBlank() && !errorNombre && !errorPrecio && !errorStock) {
            Text(mensaje)
        }

        // AGREGADO (Reto 02): Tabs para alternar contenido relacionado sin salir de Productos.
        TabRow(selectedTabIndex = tabSeleccionada.ordinal) {
            InventarioTab.entries.forEach { tab ->
                Tab(
                    selected = tabSeleccionada == tab,
                    onClick = { tabSeleccionada = tab },
                    text = { Text(tab.titulo) }
                )
            }
        }

        LazyColumn(modifier = Modifier.fillMaxWidth().weight(1f)) {
            items(productosFiltrados, key = { it.id }) { producto ->
                ListItem(
                    headlineContent = { Text(producto.nombre) },
                    supportingContent = {
                        val estado = if (producto.activo) "Activo" else "Inactivo"
                        val bajoStock = if (producto.stock <= 5) " · Bajo stock" else ""
                        Text("S/ ${producto.precio} · Stock: ${producto.stock} · $estado$bajoStock")
                    }
                )
                HorizontalDivider()
            }
        }
    }
}
