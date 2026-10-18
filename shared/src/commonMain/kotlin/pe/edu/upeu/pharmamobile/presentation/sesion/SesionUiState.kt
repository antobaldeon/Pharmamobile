package pe.edu.upeu.pharmamobile.presentation.sesion
// [Sesion 10 | UI] La clave solo vive en memoria y se elimina despues de autenticar.
data class SesionUiState(val usuario: String = "", val clave: String = "", val cargando: Boolean = false,
    val restaurando: Boolean = true, val error: String? = null)
