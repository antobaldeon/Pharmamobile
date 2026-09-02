package pe.edu.upeu.pharmamobile.Domain.model

data class Producto(
    val id: Long,
    val nombre : String,
    val precio: Double,
    val stock: Int,
    // AGREGADO (Reto 02): Permite clasificar el inventario entre Activos e Inactivos.
    val activo: Boolean = true
)

