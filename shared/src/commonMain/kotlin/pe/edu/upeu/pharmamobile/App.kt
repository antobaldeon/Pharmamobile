package pe.edu.upeu.pharmamobil

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Medication
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.PermanentDrawerSheet
import androidx.compose.material3.PermanentNavigationDrawer
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import pe.edu.upeu.pharmamobil.navigation.Screen
import pe.edu.upeu.pharmamobil.presentation.inicio.InicioScreen
import pe.edu.upeu.pharmamobil.theme.PharmaMobilTheme
import pe.edu.upeu.pharmamobile.Domain.model.Producto
import pe.edu.upeu.pharmamobile.Domain.presentation.Cliente.ClienteScreen
import pe.edu.upeu.pharmamobile.Domain.presentation.Pedido.PedidoScreen
import pe.edu.upeu.pharmamobile.Domain.presentation.Producto.ProductoScreen

// AGREGADO (Reto 02): Define el patrón de navegación según el ancho disponible.
private enum class NavigationLayout { Compacto, Mediano, Amplio }

// AGREGADO (Reto 02): Centraliza los cuatro destinos para reutilizarlos en Drawer y NavigationRail.
private data class NavigationDestination(
    val screen: Screen,
    val title: String,
    val icon: ImageVector
)

// AGREGADO (Reto 02): Evita repetir los datos de cada destino en los distintos tipos de navegación.
private val navigationDestinations = listOf(
    NavigationDestination(Screen.Inicio, "Inicio", Icons.Default.Home),
    NavigationDestination(Screen.Productos, "Productos", Icons.Default.Medication),
    NavigationDestination(Screen.Clientes, "Clientes", Icons.Default.Person),
    NavigationDestination(Screen.Pedidos, "Pedidos", Icons.Default.ShoppingCart)
)

@Composable
fun App() {
    var pantallaActual by remember { mutableStateOf<Screen>(Screen.Inicio) }
    var darkTheme by remember { mutableStateOf(false) }

    // AGREGADO (Reto 02): Mantiene el inventario simulado aunque se cambie de destino.
    val inventario = remember {
        mutableStateListOf(
            Producto(1L, "Paracetamol", 15.50, 100, activo = true),
            Producto(2L, "Ibuprofeno", 18.90, 50, activo = true),
            Producto(3L, "Amoxicilina", 25.00, 5, activo = true),
            Producto(4L, "Loratadina", 12.50, 0, activo = false),
            Producto(5L, "Diclofenaco", 20.00, 3, activo = true)
        )
    }

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    PharmaMobilTheme(darkTheme = darkTheme) {
        // AGREGADO (Reto 02): Selecciona Drawer modal, Rail o Drawer permanente por breakpoint.
        BoxWithConstraints {
            val navigationLayout = when {
                maxWidth < 600.dp -> NavigationLayout.Compacto
                maxWidth < 840.dp -> NavigationLayout.Mediano
                else -> NavigationLayout.Amplio
            }

            when (navigationLayout) {
                NavigationLayout.Compacto -> ModalNavigationDrawer(
                    drawerState = drawerState,
                    drawerContent = {
                        ModalDrawerSheet {
                            DrawerNavigationContent(
                                pantallaActual = pantallaActual,
                                darkTheme = darkTheme,
                                onDarkThemeChange = { darkTheme = it },
                                onScreenSelected = { screen ->
                                    pantallaActual = screen
                                    scope.launch { drawerState.close() }
                                }
                            )
                        }
                    }
                ) {
                    PharmaScaffold(
                        modifier = Modifier.fillMaxSize(),
                        pantallaActual = pantallaActual,
                        inventario = inventario,
                        onOpenDrawer = { scope.launch { drawerState.open() } }
                    )
                }

                NavigationLayout.Mediano -> Row(Modifier.fillMaxSize()) {
                    // AGREGADO (Reto 02): NavigationRail mejora el acceso a destinos en tablets.
                    NavigationRail(modifier = Modifier.fillMaxHeight()) {
                        navigationDestinations.forEach { destination ->
                            NavigationRailItem(
                                selected = pantallaActual == destination.screen,
                                onClick = { pantallaActual = destination.screen },
                                icon = { Icon(destination.icon, contentDescription = destination.title) },
                                label = { Text(destination.title) }
                            )
                        }
                    }
                    PharmaScaffold(
                        modifier = Modifier.weight(1f),
                        pantallaActual = pantallaActual,
                        inventario = inventario
                    )
                }

                NavigationLayout.Amplio -> PermanentNavigationDrawer(
                    // AGREGADO (Reto 02): El Drawer permanente aprovecha el espacio de escritorio/foldables.
                    drawerContent = {
                        PermanentDrawerSheet {
                            DrawerNavigationContent(
                                pantallaActual = pantallaActual,
                                darkTheme = darkTheme,
                                onDarkThemeChange = { darkTheme = it },
                                onScreenSelected = { pantallaActual = it }
                            )
                        }
                    }
                ) {
                    PharmaScaffold(
                        modifier = Modifier.fillMaxSize(),
                        pantallaActual = pantallaActual,
                        inventario = inventario
                    )
                }
            }
        }
    }
}

// MODIFICADO (Reto 02): Reutiliza la misma estructura visual en los tres patrones adaptativos.
@Composable
private fun PharmaScaffold(
    modifier: Modifier,
    pantallaActual: Screen,
    inventario: SnapshotStateList<Producto>,
    onOpenDrawer: (() -> Unit)? = null
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text(tituloPantalla(pantallaActual)) },
                navigationIcon = {
                    if (onOpenDrawer != null) {
                        IconButton(onClick = onOpenDrawer) {
                            Icon(Icons.Default.Menu, contentDescription = "Abrir menú")
                        }
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(modifier = Modifier.padding(paddingValues)) {
            when (pantallaActual) {
                Screen.Inicio -> InicioScreen()
                // MODIFICADO (Reto 02): Entrega el inventario a Productos para Tabs y registros nuevos.
                Screen.Productos -> ProductoScreen(
                    inventario = inventario,
                    onProductoRegistrado = { inventario.add(it) }
                )
                Screen.Clientes -> ClienteScreen()
                Screen.Pedidos -> PedidoScreen()
            }
        }
    }
}

// MODIFICADO (Reto 02): El contenido se comparte entre Drawer modal y permanente.
@Composable
private fun DrawerNavigationContent(
    pantallaActual: Screen,
    darkTheme: Boolean,
    onDarkThemeChange: (Boolean) -> Unit,
    onScreenSelected: (Screen) -> Unit
) {
    DrawerHeader()
    navigationDestinations.forEach { destination ->
        NavigationDrawerItem(
            label = { Text(destination.title) },
            selected = pantallaActual == destination.screen,
            onClick = { onScreenSelected(destination.screen) },
            icon = { Icon(destination.icon, contentDescription = destination.title) }
        )
    }
    Spacer(modifier = Modifier.padding(8.dp))
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text("Modo oscuro")
        Switch(checked = darkTheme, onCheckedChange = onDarkThemeChange)
    }
}

@Composable
private fun DrawerHeader() {
    Column(modifier = Modifier.fillMaxWidth().padding(24.dp)) {
        Text("PharmaMobil", style = MaterialTheme.typography.headlineSmall)
        Text("Gestión farmacéutica", style = MaterialTheme.typography.bodyMedium)
    }
}

private fun tituloPantalla(screen: Screen): String = when (screen) {
    Screen.Inicio -> "Inicio"
    Screen.Productos -> "Productos"
    Screen.Clientes -> "Clientes"
    Screen.Pedidos -> "Pedidos"
}
