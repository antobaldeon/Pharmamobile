package pe.edu.upeu.pharmamobile.data.local
// [Sesion 10 | Persistencia] Cada plataforma cifra el token con su almacen nativo.
interface AlmacenSeguro {
    fun guardarToken(token: String)
    fun leerToken(): String?
    fun borrarToken()
}
