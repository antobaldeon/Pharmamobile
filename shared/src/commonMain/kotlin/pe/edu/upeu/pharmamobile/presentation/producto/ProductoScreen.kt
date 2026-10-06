package pe.edu.upeu.pharmamobile.presentation.producto

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import pe.edu.upeu.pharmamobile.presentation.detalle.DetalleProductoScreen
import pe.edu.upeu.pharmamobile.presentation.detalle.DetalleProductoViewModel
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import org.koin.compose.viewmodel.koinViewModel
import pe.edu.upeu.pharmamobile.domain.model.Producto

@Composable
fun ProductoScreen(viewModel: ProductoViewModel = koinViewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    var seleccionado by remember { mutableStateOf<ProductoUi?>(null) }
    val detalleViewModel: DetalleProductoViewModel = koinViewModel()
    seleccionado?.let { producto ->
        DetalleProductoScreen(
            producto = producto,
            onCompartir = {
                detalleViewModel.compartir(producto.producto)
            },
            onCerrar = { seleccionado = null }
        )
    }
    val enCurso = uiState.operacion is OperacionProducto.EnCurso

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // ---------- Formulario ----------
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = MaterialTheme.shapes.medium,
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.cardElevation(defaultElevation = 3.dp)
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = if (uiState.productoEditando == null) "Registro de Producto" else "Editar producto",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.primary
                    )
                    OutlinedTextField(
                        value = uiState.nombre,
                        onValueChange = viewModel::actualizarNombre,
                        label = { Text("Nombre") },
                        isError = uiState.errorNombre != null,
                        supportingText = { uiState.errorNombre?.let { Text(it) } },
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = uiState.precio,
                        onValueChange = viewModel::actualizarPrecio,
                        label = { Text("Precio") },
                        isError = uiState.errorPrecio != null,
                        supportingText = { uiState.errorPrecio?.let { Text(it) } },
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = uiState.stock,
                        onValueChange = viewModel::actualizarStock,
                        label = { Text("Stock") },
                        isError = uiState.errorStock != null,
                        supportingText = { uiState.errorStock?.let { Text(it) } },
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = uiState.categoriaId,
                        onValueChange = viewModel::actualizarCategoria,
                        label = { Text("ID de categorÃ­a") },
                        isError = uiState.errorCategoria != null,
                        supportingText = { uiState.errorCategoria?.let { Text(it) } },
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.fillMaxWidth()
                    )
                    Button(
                        onClick = viewModel::registrarProducto,
                        enabled = !enCurso,
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.fillMaxWidth().height(50.dp)
                    ) {
                        Text(
                            if (enCurso) "Procesando..."
                            else if (uiState.productoEditando == null) "Registrar"
                            else "Guardar cambios"
                        )
                    }
                    if (uiState.productoEditando != null) {
                        OutlinedButton(
                            onClick = viewModel::cancelarEdicion,
                            enabled = !enCurso,
                            shape = MaterialTheme.shapes.small,
                            modifier = Modifier.fillMaxWidth()
                        ) { Text("Cancelar ediciÃ³n") }
                    }
                    (uiState.operacion as? OperacionProducto.Fallida)?.let {
                        Text(it.mensaje, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium)
                    }
                    uiState.mensajeExito?.let {
                        Text(it, color = MaterialTheme.colorScheme.secondary, style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
        }

        // ---------- Recargar ----------
        item {
            FilledTonalButton(
                onClick = viewModel::recargarProductos,
                enabled = uiState.fase != FaseProductos.Cargando && !enCurso,
                shape = MaterialTheme.shapes.small,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Recargar")
            }
        }

        // ---------- Filtros ----------
        item {
            Surface(
                shape = MaterialTheme.shapes.small,
                color = MaterialTheme.colorScheme.surfaceVariant
            ) {
                TabRow(
                    selectedTabIndex = uiState.filtroSeleccionado.ordinal,
                    containerColor = Color.Transparent,
                    contentColor = MaterialTheme.colorScheme.primary
                ) {
                    FiltroProducto.entries.forEach { filtro ->
                        Tab(
                            selected = uiState.filtroSeleccionado == filtro,
                            onClick = { viewModel.seleccionarFiltro(filtro) },
                            text = { Text(filtro.titulo) }
                        )
                    }
                }
            }
        }

        // ---------- Contenido segÃºn fase ----------
        when (val fase = uiState.fase) {
            FaseProductos.Cargando -> item {
                Box(
                    modifier = Modifier.fillMaxWidth().height(160.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                }
            }
            FaseProductos.SinProductos -> item {
                MensajeVacio("No hay productos registrados")
            }
            is FaseProductos.Error -> item {
                Text("Error: ${fase.mensaje}", color = MaterialTheme.colorScheme.error)
            }
            is FaseProductos.ConProductos -> listaProductos(
                productos = fase.productos,
                filtro = uiState.filtroSeleccionado,
                habilitado = !enCurso,
                editar = viewModel::editar,
                eliminar = viewModel::eliminar,
                verDetalle = { seleccionado = it }
            )
        }
    }
}

@Composable
private fun MensajeVacio(texto: String) {
    Text(
        text = texto,
        style = MaterialTheme.typography.bodyMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.fillMaxWidth().padding(vertical = 24.dp)
    )
}

@Composable
private fun EtiquetaEstado(texto: String, fondo: Color, contenido: Color) {
    Surface(shape = MaterialTheme.shapes.extraSmall, color = fondo) {
        Text(
            text = texto,
            style = MaterialTheme.typography.labelMedium,
            color = contenido,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
        )
    }
}

private fun LazyListScope.listaProductos(
    productos: List<ProductoUi>,
    filtro: FiltroProducto,
    habilitado: Boolean,
    editar: (Producto) -> Unit,
    eliminar: (Long) -> Unit,
    verDetalle: (ProductoUi) -> Unit
){
    val productosFiltrados = when (filtro) {
        FiltroProducto.Activos ->
            productos.filter { it.producto.activo }

        FiltroProducto.Inactivos ->
            productos.filterNot { it.producto.activo }

        FiltroProducto.BajoStock ->
            productos.filter { it.producto.requiereReposicion }
    }

    if (productosFiltrados.isEmpty()) {
        item { MensajeVacio("No hay productos en esta categorÃ­a") }
        return
    }

    items(
        productosFiltrados,
        key = { it.producto.id }
    ) { item ->
        val producto = item.producto

        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = MaterialTheme.shapes.medium,
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = producto.nombre,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = "${item.precioFormateado} Â· Stock: ${producto.stock}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (producto.activo) {
                        EtiquetaEstado("Activo", MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.onPrimaryContainer)
                    } else {
                        EtiquetaEstado("Inactivo", MaterialTheme.colorScheme.surfaceVariant, MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (producto.requiereReposicion) {
                        EtiquetaEstado("Bajo stock", MaterialTheme.colorScheme.errorContainer, MaterialTheme.colorScheme.onErrorContainer)
                    }
                }
                OutlinedButton(onClick = { verDetalle(item) }, enabled = habilitado) {
                    Text("Ver detalle")
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    FilledTonalButton(
                        onClick = { editar(producto) },
                        enabled = habilitado,
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.weight(1f)
                    ) { Text("Editar") }
                    OutlinedButton(
                        onClick = { eliminar(producto.id) },
                        enabled = habilitado,
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.weight(1f)
                    ) { Text("Eliminar", color = MaterialTheme.colorScheme.error) }
                }
            }
        }
    }
}