package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.ListItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import org.koin.compose.viewmodel.koinViewModel
import pe.edu.upeu.pharmamobile.domain.model.Producto

@Composable
fun ProductoScreen(viewModel: ProductoViewModel = koinViewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Registro de Producto")
        OutlinedTextField(
            value = uiState.nombre,
            onValueChange = viewModel::actualizarNombre,
            label = { Text("Nombre") },
            isError = uiState.errorNombre != null,
            supportingText = { uiState.errorNombre?.let { Text(it) } },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = uiState.precio,
            onValueChange = viewModel::actualizarPrecio,
            label = { Text("Precio") },
            isError = uiState.errorPrecio != null,
            supportingText = { uiState.errorPrecio?.let { Text(it) } },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = uiState.stock,
            onValueChange = viewModel::actualizarStock,
            label = { Text("Stock") },
            isError = uiState.errorStock != null,
            supportingText = { uiState.errorStock?.let { Text(it) } },
            modifier = Modifier.fillMaxWidth()
        )
        Button(onClick = viewModel::registrarProducto, modifier = Modifier.fillMaxWidth()) {
            Text("Registrar")
        }
        uiState.mensajeExito?.let { Text(it) }

        TabRow(selectedTabIndex = uiState.filtroSeleccionado.ordinal) {
            FiltroProducto.entries.forEach { filtro ->
                Tab(
                    selected = uiState.filtroSeleccionado == filtro,
                    onClick = { viewModel.seleccionarFiltro(filtro) },
                    text = { Text(filtro.titulo) }
                )
            }
        }

        when (val fase = uiState.fase) {
            FaseProductos.Cargando -> Box(Modifier.fillMaxWidth().weight(1f), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            FaseProductos.SinProductos -> Text("No hay productos registrados")
            is FaseProductos.Error -> Text("Error: ${fase.mensaje}")
            is FaseProductos.ConProductos -> ListaProductos(
                productos = fase.productos,
                filtro = uiState.filtroSeleccionado
            )
        }
    }
}

@Composable
private fun ListaProductos(productos: List<Producto>, filtro: FiltroProducto) {
    val productosFiltrados = when (filtro) {
        FiltroProducto.Activos -> productos.filter { it.activo }
        FiltroProducto.Inactivos -> productos.filterNot { it.activo }
        FiltroProducto.BajoStock -> productos.filter { it.requiereReposicion }
    }

    if (productosFiltrados.isEmpty()) {
        Text("No hay productos en esta categoría")
        return
    }

    LazyColumn(modifier = Modifier.fillMaxWidth().weight(1f)) {
        items(productosFiltrados, key = Producto::id) { producto ->
            ListItem(
                headlineContent = { Text(producto.nombre) },
                supportingContent = {
                    val estado = if (producto.activo) "Activo" else "Inactivo"
                    val reposicion = if (producto.requiereReposicion) " · Bajo stock" else ""
                    Text("S/ ${producto.precio} · Stock: ${producto.stock} · $estado$reposicion")
                }
            )
            HorizontalDivider()
        }
    }
}
