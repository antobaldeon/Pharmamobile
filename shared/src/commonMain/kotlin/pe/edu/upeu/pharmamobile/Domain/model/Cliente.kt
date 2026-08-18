package pe.edu.upeu.pharmamobile.Domain.model

data class Cliente(
    val id : Long,
    val nombre: String,
    val correo: String,
    val telefono: String?
){
    fun obtenerTelefono(): String{
        return telefono ?: "No registrado"
    }
}
