package pe.edu.upeu.pharmamobile.data.repository

import pe.edu.upeu.pharmamobile.Domain.model.Producto
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import pe.edu.upeu.pharmamobile.Domain.model.ResultadoProductos

class ProductoRepository {
    private val productosSimulados = listOf(
        Producto(1, "Paracetamol", 8.50, 100),
        Producto(2, "Ibuprofeno", 12.00, 50),
        Producto(3, "Amoxicilina", 18.50, 20)
    )

    suspend fun obtenerProductos(): List<Producto> {
        delay(1000) // Simula espera de red
        return productosSimulados
    }
    // Flow simple: lista vacía -> lista con datos
    fun observarProductos(): Flow<List<Producto>> = flow {
        emit(emptyList())
        delay(1000)
        emit(productosSimulados)
    }

    // Flow con sealed class: Cargando -> Exito
    fun cargarProductos(): Flow<ResultadoProductos> = flow {
        emit(ResultadoProductos.Cargando)
        delay(1000)
        emit(ResultadoProductos.Exito(productosSimulados))
    }
}