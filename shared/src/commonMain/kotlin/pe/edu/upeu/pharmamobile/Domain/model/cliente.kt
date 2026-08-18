package pe.edu.upeu.pharmamobile.Domain.model

data class cliente(
    val id : Long,
    val nombre: String,
    val correo: String,
    val telefono: String?
)
