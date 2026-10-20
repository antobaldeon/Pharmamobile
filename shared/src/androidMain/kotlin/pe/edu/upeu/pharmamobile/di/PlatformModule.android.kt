package pe.edu.upeu.pharmamobile.di

import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.okhttp.OkHttp
import org.koin.android.ext.koin.androidContext
import org.koin.core.module.Module
import org.koin.dsl.module
import pe.edu.upeu.pharmamobile.domain.platform.Compartidor
import pe.edu.upeu.pharmamobile.platform.CompartidorAndroid

actual val platformModule: Module = module {
    single<pe.edu.upeu.pharmamobile.data.local.CreadorDeDriver> {
        pe.edu.upeu.pharmamobile.data.local.CreadorDeDriverAndroid(androidContext())
    }
    // [Sesion 10 | Plataforma] Inyecta almacenamiento seguro y modo de depuracion.
    single<pe.edu.upeu.pharmamobile.data.local.AlmacenSeguro> {
        pe.edu.upeu.pharmamobile.data.local.AlmacenSeguroAndroid(androidContext())
    }
    single { ConfiguracionDepuracion((androidContext().applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0) }
    single<HttpClientEngine> {
        OkHttp.create()
    }

    single<Compartidor> {
        CompartidorAndroid(androidContext())
    }
}

actual val backendBaseUrl: String =
    "http://10.0.2.2:8080/"
