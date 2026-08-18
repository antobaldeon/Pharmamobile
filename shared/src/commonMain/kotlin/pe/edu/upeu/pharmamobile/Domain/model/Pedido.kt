package pe.edu.upeu.pharmamobile.Domain.model

data class Pedido(
    val id: Long,
    val cliente: Cliente,
    val detalles: List<DetallePedido>,
    val estadoPedido: EstadoPedido
)
