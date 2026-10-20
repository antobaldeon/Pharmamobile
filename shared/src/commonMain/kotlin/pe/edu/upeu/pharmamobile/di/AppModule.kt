package pe.edu.upeu.pharmamobile.di

import pe.edu.upeu.pharmamobile.presentation.sesion.SesionViewModel
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
import pe.edu.upeu.pharmamobile.presentation.detalle.DetalleProductoViewModel

// [Sesion 10 | Koin] Comparte el estado de sesion entre HTTP y navegacion.
val dataModule = module {
    single { pe.edu.upeu.pharmamobile.data.local.GestorSesion(get(), get()) }
    single { pe.edu.upeu.pharmamobile.data.remote.AuthApi(get()) }
    single<pe.edu.upeu.pharmamobile.domain.repository.AuthRepository> {
        pe.edu.upeu.pharmamobile.data.repository.AuthRepositorioRest(get(), get(), get(), get(), get())
    }
    single<HttpClient> {
        crearHttpClient(
            engine = get(),
            baseUrl = backendBaseUrl,
            almacen = get(),
            gestor = get(),
            esDepuracion = get<ConfiguracionDepuracion>().activa
        )
    }

    single {
        ProductoApi(get())
    }

    single { pe.edu.upeu.pharmamobile.db.PharmaDb(get<pe.edu.upeu.pharmamobile.data.local.CreadorDeDriver>().crear()) }
    single { pe.edu.upeu.pharmamobile.data.local.ProductoLocal(get()) }
    single { pe.edu.upeu.pharmamobile.data.local.SesionLocal(get()) }
    single { ProductoRepositoryImpl(get()) }
    single<ProductoRepository> {
        pe.edu.upeu.pharmamobile.data.repository.ProductoRepositorioOffline(get(), get<ProductoRepositoryImpl>())
    }
}

val domainModule = module {
    // [Sesion 10 | Koin] Inyecta las tres operaciones de autenticacion.
    factory { IniciarSesionUseCase(get()) }
    factory { RecuperarSesionUseCase(get()) }
    factory { CerrarSesionUseCase(get()) }
    factory { RegistrarProductoUseCase(get()) }
    factory { ListarProductosUseCase(get()) }
    factory { ActualizarProductoUseCase(get()) }
    factory { EliminarProductoUseCase(get()) }
}

val presentationModule = module {
    // [Sesion 10 | Koin] La puerta de entrada mantiene un ViewModel de sesion.
    viewModelOf(::SesionViewModel)
    viewModelOf(::ProductoViewModel)
    viewModelOf(::DetalleProductoViewModel)
}

expect val backendBaseUrl: String
expect val platformModule: Module

fun initKoin(config: KoinApplication.() -> Unit = {}) = startKoin {
    config()
    modules(dataModule, domainModule, presentationModule, platformModule)
}

fun initKoinIos() = initKoin()

// [Sesion 10 | Configuracion] Cada plataforma decide si habilita el registro de depuracion.
data class ConfiguracionDepuracion(val activa: Boolean)
