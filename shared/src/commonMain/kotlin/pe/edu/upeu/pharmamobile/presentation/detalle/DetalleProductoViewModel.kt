package pe.edu.upeu.pharmamobile.presentation.detalle

import androidx.lifecycle.ViewModel
import pe.edu.upeu.pharmamobile.domain.model.Producto
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import pe.edu.upeu.pharmamobile.domain.usecase.comoTextoParaCompartir

class DetalleProductoViewModel(
    private val compartidor: Compartidor
) : ViewModel() {

    fun compartir(producto: Producto) {
        compartidor.compartir(
            producto.comoTextoParaCompartir()
        )
    }
}