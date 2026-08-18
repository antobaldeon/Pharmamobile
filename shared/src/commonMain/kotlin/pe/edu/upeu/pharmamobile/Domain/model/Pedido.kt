package pe.edu.upeu.pharmamobile.Domain.model

data class Pedido(
    val id: Long,
    val cliente: cliente,
    val detalles: List<DetallePedido>,
    val estadoPedido: EstadoPedido
)
