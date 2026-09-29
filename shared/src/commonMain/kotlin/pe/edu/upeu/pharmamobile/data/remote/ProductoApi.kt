package pe.edu.upeu.pharmamobile.data.remote

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.parameter
import pe.edu.upeu.pharmamobile.data.remote.dto.PaginaProductosDto

class ProductoApi(
    private val client: HttpClient
) {
    suspend fun obtenerPagina(pagina: Int): PaginaProductosDto {
        return client.get("api/v1/productos") {
            parameter("pagina", pagina)
            parameter("tamanio", 20)
            parameter("ordenarPor", "id")
            parameter("direccion", "asc")
        }.body()
    }
}