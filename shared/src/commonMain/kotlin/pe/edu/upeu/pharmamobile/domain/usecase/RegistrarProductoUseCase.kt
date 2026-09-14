package pe.edu.upeu.pharmamobile.domain.usecase

import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository

class RegistrarProductoUseCase(
    private val productoRepository: ProductoRepository
) {
    suspend operator fun invoke(nombre: String, precioTexto: String, stockTexto: String): Result<Producto> {
        if (nombre.isBlank()) return fallo(nombre = "Nombre obligatorio")

        val precio = precioTexto.toDoubleOrNull()
            ?: return fallo(precio = "Precio inválido")
        if (precio <= 0) return fallo(precio = "El precio debe ser mayor a 0")

        val stock = stockTexto.toIntOrNull()
            ?: return fallo(stock = "Stock debe ser un número entero")
        if (stock < 0) return fallo(stock = "Stock no puede ser negativo")

        return runCatching {
            productoRepository.registrar(
                Producto(id = 0, nombre = nombre.trim(), precio = precio, stock = stock)
            )
        }
    }

    private fun fallo(
        nombre: String? = null,
        precio: String? = null,
        stock: String? = null
    ): Result<Producto> = Result.failure(ValidacionProductoException(nombre, precio, stock))
}

class ValidacionProductoException(
    val errorNombre: String?,
    val errorPrecio: String?,
    val errorStock: String?
) : IllegalArgumentException(listOfNotNull(errorNombre, errorPrecio, errorStock).first())
