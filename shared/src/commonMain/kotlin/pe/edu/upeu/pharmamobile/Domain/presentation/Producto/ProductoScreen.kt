package pe.edu.upeu.pharmamobile.Domain.presentation.Producto

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import pe.edu.upeu.pharmamobile.Domain.model.Producto

@Composable
fun ProductoScreen() {
    // Paso 2: estados de texto (inicialmente String)
    var nombre by remember { mutableStateOf("") }
    var precio by remember { mutableStateOf("") }
    var stock by remember { mutableStateOf("") }

    // Paso 3 y 4: control de intento y mensaje de retroalimentación
    var mensaje by remember { mutableStateOf("") }
    var intentoRegistrar by remember { mutableStateOf(false) }

    // Banderas de error por campo, usadas solo para pintar isError en la UI
    var errorNombre by remember { mutableStateOf(false) }
    var errorPrecio by remember { mutableStateOf(false) }
    var errorStock by remember { mutableStateOf(false) }

    fun registrar() {
        intentoRegistrar = true
        errorNombre = false
        errorPrecio = false
        errorStock = false

        // Pasos 5 y 6: conversión segura (*OrNull) antes de evaluar reglas
        val precioDouble = precio.toDoubleOrNull()
        val stockInt = stock.toIntOrNull()

        // Paso 7: secuencia estricta de validación
        when {
            nombre.isBlank() -> {
                errorNombre = true
                mensaje = "El nombre es obligatorio."
            }
            precioDouble == null -> {
                errorPrecio = true
                mensaje = "Ingrese un precio numérico."
            }
            precioDouble <= 0.0 -> {
                errorPrecio = true
                mensaje = "El precio debe ser mayor que cero."
            }
            stockInt == null -> {
                errorStock = true
                mensaje = "Ingrese un stock entero."
            }
            stockInt < 0 -> {
                errorStock = true
                mensaje = "El stock no puede ser negativo."
            }
            else -> {
                // Producto solo se construye si todas las reglas pasaron
                val producto = Producto(
                    id = 0L,
                    nombre = nombre,
                    precio = precioDouble,
                    stock = stockInt
                )
                println("Producto registrado: $producto")
                mensaje = "Producto registrado correctamente"

                // Paso 8: limpieza automática del formulario
                nombre = ""
                precio = ""
                stock = ""
                intentoRegistrar = false
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("PharmaMobil")
        Text("Registro de Producto")

        // Paso 9: isError solo se activa después de un intento de registro
        OutlinedTextField(
            value = nombre,
            onValueChange = { nombre = it },
            label = { Text("Nombre") },
            isError = intentoRegistrar && errorNombre,
            supportingText = {
                if (intentoRegistrar && errorNombre) Text(mensaje)
            },
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = precio,
            onValueChange = { precio = it },
            label = { Text("Precio") },
            isError = intentoRegistrar && errorPrecio,
            supportingText = {
                if (intentoRegistrar && errorPrecio) Text(mensaje)
            },
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = stock,
            onValueChange = { stock = it },
            label = { Text("Stock") },
            isError = intentoRegistrar && errorStock,
            supportingText = {
                if (intentoRegistrar && errorStock) Text(mensaje)
            },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { registrar() },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Registrar")
        }

        if (mensaje.isNotBlank() && !errorNombre && !errorPrecio && !errorStock) {
            Text(mensaje)
        }
    }
}