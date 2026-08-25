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

@Composable

fun ProductoScreen() {
    var nombre by remember { mutableStateOf("") }
    var precio by remember { mutableStateOf("") }
    var stock by remember { mutableStateOf("") }

    var errorNombre by remember { mutableStateOf(false) }
    var errorPrecio by remember { mutableStateOf(false) }
    var errorStock by remember { mutableStateOf(false) }

    var mensaje by remember { mutableStateOf("") }

    fun validar(): Boolean {
        errorNombre = nombre.isBlank()
        errorPrecio = precio.toDoubleOrNull() == null || precio.toDouble() <= 0.0
        errorStock = stock.toIntOrNull() == null || stock.toInt() < 0

        return !errorNombre && !errorPrecio && !errorStock
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("PharmaMobil")
        Text("Registro de Producto")

        OutlinedTextField(
            value = nombre,
            onValueChange = { nombre = it },
            label = { Text("Nombre") },
            isError = errorNombre,
            supportingText = {
                if (errorNombre) Text("El nombre es obligatorio")
            },
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = precio,
            onValueChange = { precio = it },
            label = { Text("Precio") },
            isError = errorPrecio,
            supportingText = {
                if (errorPrecio) Text("Precio inválido")
            },
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = stock,
            onValueChange = { stock = it },
            label = { Text("Stock") },
            isError = errorStock,
            supportingText = {
                if (errorStock) Text("El stock no puede ser negativo")
            },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = {
                if (validar()) {
                    println("Nombre=$nombre, Precio=$precio, Stock=$stock")
                    mensaje = "Producto registrado correctamente"
                } else {
                    mensaje = ""
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Registrar")
        }

        if (mensaje.isNotBlank()) {
            Text(mensaje)
        }
    }
}