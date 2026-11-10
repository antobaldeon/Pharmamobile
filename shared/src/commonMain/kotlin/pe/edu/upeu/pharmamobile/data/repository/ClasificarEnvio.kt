package pe.edu.upeu.pharmamobile.data.repository
import pe.edu.upeu.pharmamobile.domain.error.*
import pe.edu.upeu.pharmamobile.domain.model.ResultadoEnvio
fun ErrorApiException.resultadoEnvio(): ResultadoEnvio = when (error) {
    ErrorApi.SinConexion, ErrorApi.TiempoAgotado, ErrorApi.Servidor -> ResultadoEnvio.Transitorio(message ?: "Error de conexión")
    else -> ResultadoEnvio.Permanente(message ?: "Revisar el producto")
}
