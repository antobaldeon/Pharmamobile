package pe.edu.upeu.pharmamobile.platform

import kotlinx.cinterop.ExperimentalForeignApi
import kotlinx.cinterop.useContents
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import platform.CoreGraphics.CGRectMake
import platform.UIKit.*

@OptIn(ExperimentalForeignApi::class)
class CompartidorIos : Compartidor {
    override fun compartir(texto: String) {
        val ventana = UIApplication.sharedApplication.connectedScenes
            .filterIsInstance<UIWindowScene>()
            .filter { it.activationState == UISceneActivationStateForegroundActive }
            .flatMap { it.windows.filterIsInstance<UIWindow>() }
            .firstOrNull { it.isKeyWindow() }
            ?: error("No hay una ventana activa para compartir")
        var presentador = ventana.rootViewController
            ?: error("No hay un controlador disponible para compartir")
        while (presentador.presentedViewController != null) {
            presentador = presentador.presentedViewController!!
        }
        val controlador = UIActivityViewController(listOf(texto), null)
        controlador.popoverPresentationController?.let { popover ->
            popover.sourceView = presentador.view
            presentador.view.bounds.useContents {
                popover.sourceRect = CGRectMake(size.width / 2, size.height / 2, 1.0, 1.0)
            }
        }
        presentador.presentViewController(controlador, true, null)
    }
}
