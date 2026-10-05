package pe.edu.upeu.pharmamobile.data.remote

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.*
import pe.edu.upeu.pharmamobile.data.remote.dto.*

class ProductoApi(private val client: HttpClient) {
    suspend fun obtenerPagina(pagina: Int): PaginaProductosDto = client.get("api/v1/productos") {
        parameter("pagina", pagina)
        parameter("tamanio", 20)
        parameter("ordenarPor", "id")
        parameter("direccion", "asc")
    }.body()
    suspend fun obtener(id: Long): ProductoDto = client.get("api/v1/productos/$id").body()
    suspend fun crear(request: ProductoRequestDto): ProductoDto = client.post("api/v1/productos") { setBody(request) }.body()
    suspend fun actualizar(id: Long, request: ProductoRequestDto): ProductoDto = client.put("api/v1/productos/$id") { setBody(request) }.body()
    suspend fun eliminar(id: Long) { client.delete("api/v1/productos/$id") }
}
