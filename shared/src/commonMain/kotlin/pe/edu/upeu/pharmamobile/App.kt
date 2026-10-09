package pe.edu.upeu.pharmamobil

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import pe.edu.upeu.pharmamobile.presentation.acerca.AcercaScreen
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Medication
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.NavigationDrawerItemDefaults
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.NavigationRailItemDefaults
import androidx.compose.material3.PermanentDrawerSheet
import androidx.compose.material3.PermanentNavigationDrawer
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberDrawerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import org.koin.compose.KoinContext
import pe.edu.upeu.pharmamobil.navigation.Screen
import pe.edu.upeu.pharmamobil.presentation.inicio.InicioScreen
import pe.edu.upeu.pharmamobil.theme.PharmaMobilTheme
import pe.edu.upeu.pharmamobile.domain.presentation.Cliente.ClienteScreen
import pe.edu.upeu.pharmamobile.domain.presentation.Pedido.PedidoScreen
import pe.edu.upeu.pharmamobile.presentation.producto.ProductoScreen

// Define el patrÃ³n de navegaciÃ³n segÃºn el ancho disponible.
private enum class NavigationLayout { Compacto, Mediano, Amplio }

// Centraliza los destinos para reutilizarlos en Drawer y NavigationRail.
private data class NavigationDestination(
    val screen: Screen,
    val title: String,
    val icon: ImageVector
)

private val navigationDestinations = listOf(
    NavigationDestination(Screen.Inicio, "Inicio", Icons.Default.Home),
    NavigationDestination(Screen.Productos, "Productos", Icons.Default.Medication),
    NavigationDestination(Screen.Clientes, "Clientes", Icons.Default.Person),
    NavigationDestination(Screen.Pedidos, "Pedidos", Icons.Default.ShoppingCart),
    NavigationDestination(Screen.Acerca, "Acerca de", Icons.Default.Info)
)

@Composable
fun App() {
    KoinContext {
        PharmaMobilApp()
    }
}

@Composable
private fun PharmaMobilApp() {
    var pantallaActual by remember { mutableStateOf<Screen>(Screen.Inicio) }
    var darkTheme by remember { mutableStateOf(false) }

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    PharmaMobilTheme(darkTheme = darkTheme) {
        // Selecciona Drawer modal, Rail o Drawer permanente por breakpoint.
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
                        onOpenDrawer = { scope.launch { drawerState.open() } }
                    )
                }

                NavigationLayout.Mediano -> Row(Modifier.fillMaxSize()) {
                    NavigationRail(
                        modifier = Modifier.fillMaxHeight(),
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.onPrimary
                    ) {
                        Spacer(Modifier.height(12.dp))
                        navigationDestinations.forEach { destination ->
                            NavigationRailItem(
                                selected = pantallaActual == destination.screen,
                                onClick = { pantallaActual = destination.screen },
                                icon = { Icon(destination.icon, contentDescription = destination.title) },
                                label = { Text(destination.title) },
                                colors = NavigationRailItemDefaults.colors(
                                    selectedIconColor = MaterialTheme.colorScheme.onPrimaryContainer,
                                    selectedTextColor = MaterialTheme.colorScheme.onPrimary,
                                    indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                                    unselectedIconColor = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.7f),
                                    unselectedTextColor = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.7f)
                                )
                            )
                        }
                    }
                    PharmaScaffold(
                        modifier = Modifier.weight(1f),
                        pantallaActual = pantallaActual,
                    )
                }

                NavigationLayout.Amplio -> PermanentNavigationDrawer(
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
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun PharmaScaffold(
    modifier: Modifier,
    pantallaActual: Screen,
    onOpenDrawer: (() -> Unit)? = null
) {
    Scaffold(
        modifier = modifier,
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = { Text(tituloPantalla(pantallaActual), style = MaterialTheme.typography.titleLarge) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                ),
                navigationIcon = {
                    if (onOpenDrawer != null) {
                        IconButton(onClick = onOpenDrawer) {
                            Icon(Icons.Default.Menu, contentDescription = "Abrir menÃº")
                        }
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(modifier = Modifier.padding(paddingValues)) {
            when (pantallaActual) {
                Screen.Inicio -> InicioScreen()
                Screen.Productos -> ProductoScreen()
                Screen.Clientes -> ClienteScreen()
                Screen.Pedidos -> PedidoScreen()
                Screen.Acerca -> AcercaScreen()
            }
        }
    }
}

// El contenido se comparte entre Drawer modal y permanente.
@Composable
private fun DrawerNavigationContent(
    pantallaActual: Screen,
    darkTheme: Boolean,
    onDarkThemeChange: (Boolean) -> Unit,
    onScreenSelected: (Screen) -> Unit
) {
    // Scroll por si el menÃº no cabe en pantallas bajas / landscape
    Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
        DrawerHeader()
        Spacer(Modifier.height(12.dp))
        navigationDestinations.forEach { destination ->
            NavigationDrawerItem(
                label = { Text(destination.title) },
                selected = pantallaActual == destination.screen,
                onClick = { onScreenSelected(destination.screen) },
                icon = { Icon(destination.icon, contentDescription = destination.title) },
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp),
                colors = NavigationDrawerItemDefaults.colors(
                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                    selectedTextColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    selectedIconColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
        Spacer(Modifier.height(8.dp))
        HorizontalDivider(modifier = Modifier.padding(horizontal = 20.dp))
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Modo oscuro", style = MaterialTheme.typography.bodyMedium)
            Switch(
                checked = darkTheme,
                onCheckedChange = onDarkThemeChange,
                colors = SwitchDefaults.colors(
                    checkedTrackColor = MaterialTheme.colorScheme.primary,
                    checkedThumbColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    }
}

@Composable
private fun DrawerHeader() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.primary)
            .padding(horizontal = 24.dp, vertical = 32.dp)
    ) {
        Text(
            "PharmaMobil",
            style = MaterialTheme.typography.headlineSmall,
            color = MaterialTheme.colorScheme.onPrimary
        )
        Text(
            "GestiÃ³n farmacÃ©utica",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.75f)
        )
    }
}

private fun tituloPantalla(screen: Screen): String = when (screen) {
    Screen.Inicio -> "Inicio"
    Screen.Productos -> "Productos"
    Screen.Clientes -> "Clientes"
    Screen.Pedidos -> "Pedidos"
    Screen.Acerca -> "Acerca de"
}