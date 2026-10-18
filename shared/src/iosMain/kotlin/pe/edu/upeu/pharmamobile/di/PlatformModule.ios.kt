// [Sesion 10 | Depuracion] Permite consultar si el binario nativo es de desarrollo.
@file:OptIn(kotlin.experimental.ExperimentalNativeApi::class)

package pe.edu.upeu.pharmamobile.di

import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.darwin.Darwin
import org.koin.core.module.Module
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import pe.edu.upeu.pharmamobile.platform.CompartidorIos
import org.koin.dsl.module

actual val platformModule: Module = module {
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

actual val backendBaseUrl: String = "http://localhost:8080/"
