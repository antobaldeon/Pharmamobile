package pe.edu.upeu.pharmamobile.data.local

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import pe.edu.upeu.pharmamobile.db.PharmaDb
import pe.edu.upeu.pharmamobile.domain.model.Sesion

/** Perfil sin JWT. El token permanece en el almacén seguro de la plataforma. */
class SesionLocal(base: PharmaDb) {
    private val consultas = base.sesionLocalQueries
    fun guardar(sesion: Sesion) {
        consultas.guardarPerfil(sesion.usuario, sesion.nombreCompleto,
            Json.encodeToString(sesion.permisos.toList()), Json.encodeToString(sesion.roles))
    }
    fun leer(token: String): Sesion? = consultas.leerPerfil().executeAsOneOrNull()?.let {
        Sesion(token, it.usuario, it.nombre, Json.decodeFromString<List<String>>(it.permisos).toSet(), Json.decodeFromString<List<String>>(it.roles))
    }
    fun borrar() = consultas.borrarPerfil()
}
