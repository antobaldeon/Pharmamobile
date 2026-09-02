# Reto 02 - Tabs, theming y navegación adaptativa

> AGREGADO (Reto 02): Este documento identifica qué se agregó y por qué.

## Navegación adaptativa

> AGREGADO (Reto 02): La selección se realiza en `App.kt` con `BoxWithConstraints`.

| Ancho disponible | Patrón aplicado | Motivo |
| --- | --- | --- |
| Menor de 600 dp | `ModalNavigationDrawer` | Conserva espacio para el contenido en teléfonos. |
| De 600 dp a menos de 840 dp | `NavigationRail` | Mantiene los destinos visibles en tablets. |
| 840 dp o más | `PermanentNavigationDrawer` | Aprovecha el espacio de escritorio y foldables. |

## Inventario y Tabs

> AGREGADO (Reto 02): El inventario inicia con cinco productos simulados y se comparte desde `App.kt`.

- **Activos**: productos con `activo = true`.
- **Inactivos**: productos con `activo = false`.
- **Bajo stock**: productos con `stock <= 5`; por lo tanto, stock `0` también aparece aquí.
- Un registro válido se agrega al inventario como producto activo y se muestra de inmediato en las Tabs.

## Verificación manual pendiente

> AGREGADO (Reto 02): Completar estas evidencias en emulador o dispositivo antes de la entrega.

- [ ] Inicio -> Productos -> Clientes -> Pedidos -> Inicio sin pérdida de estado.
- [ ] Tabs Activos, Inactivos y Bajo stock muestran el filtro correcto.
- [ ] Tema claro y oscuro conservan contraste legible en cada destino.
- [ ] Registrar `Paracetamol / 15.50 / 100` agrega el producto a Activos.
- [ ] Verificar que `Amoxicilina / 25.00 / 5` y `Loratadina / 12.50 / 0` aparecen en Bajo stock.
- [ ] Tomar capturas de Inicio, Drawer/Rail, Tabs, ambos temas y el logo compartido.
