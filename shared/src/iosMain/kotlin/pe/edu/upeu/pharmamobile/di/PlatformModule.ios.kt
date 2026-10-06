package pe.edu.upeu.pharmamobile.di

import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.darwin.Darwin
import org.koin.core.module.Module
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import pe.edu.upeu.pharmamobile.platform.CompartidorIos
import org.koin.dsl.module

actual val platformModule: Module = module {
    single<Compartidor> { CompartidorIos() }
    single<HttpClientEngine> {
        Darwin.create()
    }
}

actual val backendBaseUrl: String = "http://localhost:8080/"
