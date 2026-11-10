// [Sesion 10 | Depuracion] Permite consultar si el binario nativo es de desarrollo.
@file:OptIn(kotlin.experimental.ExperimentalNativeApi::class)

package pe.edu.upeu.pharmamobile.di

import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.darwin.Darwin
import org.koin.core.module.Module
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import pe.edu.upeu.pharmamobile.platform.CompartidorIos
import org.koin.dsl.module
import platform.Foundation.NSBundle
import pe.edu.upeu.pharmamobile.domain.port.Telemetria
import pe.edu.upeu.pharmamobile.data.firebase.TelemetriaFirebase

actual val platformModule: Module = module {
    // La configuración Android no sustituye el archivo real de Firebase para iOS.
    single<Telemetria> {
        if (NSBundle.mainBundle.pathForResource("GoogleService-Info", "plist") != null) {
            TelemetriaFirebase()
        } else object : Telemetria {
            override fun registrarError(e: Throwable, contexto: Map<String, String>) = Unit
            override fun registrarEvento(nombre: String, datos: Map<String, String>) = Unit
        }
    }
    single<pe.edu.upeu.pharmamobile.domain.permiso.GestorPermisos> { pe.edu.upeu.pharmamobile.data.permiso.GestorPermisosIos() }
    single<pe.edu.upeu.pharmamobile.data.local.CreadorDeDriver> {
        pe.edu.upeu.pharmamobile.data.local.CreadorDeDriverIos()
    }
    // [Sesion 10 | Plataforma] Inyecta almacenamiento seguro y modo de depuracion.
    single<pe.edu.upeu.pharmamobile.data.local.AlmacenSeguro> {
        pe.edu.upeu.pharmamobile.data.local.AlmacenSeguroIos()
    }
    single { ConfiguracionDepuracion(kotlin.native.Platform.isDebugBinary) }
    single<Compartidor> { CompartidorIos() }
    single<HttpClientEngine> {
        Darwin.create()
    }
}

actual val backendBaseUrl: String
    get() = (NSBundle.mainBundle.objectForInfoDictionaryKey("PharmaBackendURL") as? String)
        ?.takeIf { it.isNotBlank() } ?: "http://localhost:8080/"
