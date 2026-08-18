package pe.edu.upeu.pharmamobile.domain.model

import pe.edu.upeu.pharmamobile.Domain.model.Cliente
import kotlin.test.Test
import kotlin.test.assertEquals

class ClienteTest {

    @Test
    fun probrarCliente(){
        val cliente = Cliente(
            id =   1L,
            nombre = "Farmacia Nueva Vida",
            correo = "ventas@central.pe",
            telefono = "987654321"
        )
        val resultado = cliente.obtenerTelefono()

        assertEquals(
            "987654321",
            resultado

        )
    }
}