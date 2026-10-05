package pe.edu.upeu.pharmamobile.di

import org.koin.core.KoinApplication
import org.koin.core.context.startKoin
import org.koin.core.module.Module
import org.koin.core.module.dsl.viewModelOf
import org.koin.dsl.module
import pe.edu.upeu.pharmamobile.domain.repository.ProductoRepository
import pe.edu.upeu.pharmamobile.domain.usecase.*
import pe.edu.upeu.pharmamobile.presentation.producto.ProductoViewModel
import io.ktor.client.HttpClient
import pe.edu.upeu.pharmamobile.data.remote.crearHttpClient
import pe.edu.upeu.pharmamobile.data.remote.ProductoApi
import pe.edu.upeu.pharmamobile.data.repository.ProductoRepositoryImpl

val dataModule = module {
    single<HttpClient> {
        crearHttpClient(
            engine = get(),
            baseUrl = backendBaseUrl
        )
    }

    single {
        ProductoApi(get())
    }

    single<ProductoRepository> {
        ProductoRepositoryImpl(get())
    }
}

val domainModule = module {
    factory { RegistrarProductoUseCase(get()) }
    factory { ListarProductosUseCase(get()) }
    factory { ActualizarProductoUseCase(get()) }
    factory { EliminarProductoUseCase(get()) }
}

val presentationModule = module {
    viewModelOf(::ProductoViewModel)
}

expect val backendBaseUrl: String
expect val platformModule: Module

fun initKoin(config: KoinApplication.() -> Unit = {}) = startKoin {
    config()
    modules(dataModule, domainModule, presentationModule, platformModule)
}
