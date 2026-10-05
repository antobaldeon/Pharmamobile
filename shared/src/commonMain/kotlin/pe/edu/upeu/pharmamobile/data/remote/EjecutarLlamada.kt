package pe.edu.upeu.pharmamobile.data.remote

import io.ktor.client.call.body
import io.ktor.client.plugins.*
import io.ktor.utils.io.errors.IOException
import kotlinx.coroutines.CancellationException
import pe.edu.upeu.pharmamobile.data.remote.dto.ErrorResponseDto
import pe.edu.upeu.pharmamobile.domain.error.*

suspend fun <T> ejecutarLlamada(bloque: suspend () -> T): Result<T> = try {
    Result.success(bloque())
} catch (e: CancellationException) {
    throw e
} catch (e: ClientRequestException) {
    val cuerpo = try { e.response.body<ErrorResponseDto>() } catch (c: CancellationException) { throw c } catch (_: Exception) { null }
    Result.failure(ErrorApiException(when (e.response.status.value) {
        400 -> ErrorApi.Validacion(cuerpo?.validationErrors.orEmpty())
        404 -> ErrorApi.NoEncontrado
        409 -> ErrorApi.Conflicto(cuerpo?.message ?: "Operación no permitida")
        else -> ErrorApi.Servidor
    }))
} catch (e: ServerResponseException) {
    Result.failure(ErrorApiException(ErrorApi.Servidor))
} catch (e: HttpRequestTimeoutException) {
    Result.failure(ErrorApiException(ErrorApi.TiempoAgotado))
} catch (e: IOException) {
    Result.failure(ErrorApiException(ErrorApi.SinConexion))
} catch (e: Exception) {
    Result.failure(ErrorApiException(ErrorApi.Servidor))
}
