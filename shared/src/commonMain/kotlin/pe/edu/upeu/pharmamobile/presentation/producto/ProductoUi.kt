package pe.edu.upeu.pharmamobile.presentation.producto

import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.platform.formatearSoles

data class ProductoUi(
    val producto: Producto,
    val precioFormateado: String
)

fun Producto.toUi(): ProductoUi =
    ProductoUi(
        producto = this,
        precioFormateado = formatearSoles(precio)
    )