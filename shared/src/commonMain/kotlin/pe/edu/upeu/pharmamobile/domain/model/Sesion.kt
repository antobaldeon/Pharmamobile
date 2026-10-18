package pe.edu.upeu.pharmamobile.domain.model
// [Sesion 10 | Dominio] Describe credenciales y permisos sin depender de HTTP.
data class Credenciales(val usuario: String, val clave: String)
data class Sesion(val token: String, val usuario: String, val nombreCompleto: String, val permisos: Set<String>, val roles: List<String> = emptyList()) {
    fun puede(permiso: String) = permiso in permisos
}
