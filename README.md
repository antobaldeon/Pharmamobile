This is a Kotlin Multiplatform project targeting Android, iOS.

* [/iosApp](./iosApp/iosApp) contains an iOS application. Even if youÃ¢â‚¬â„¢re sharing your UI with Compose Multiplatform,
  you need this entry point for your iOS app. This is also where you should add SwiftUI code for your project.

* [/shared](./shared/src) is for code that will be shared across your Compose Multiplatform applications.
  It contains several subfolders:
  - [commonMain](./shared/src/commonMain/kotlin) is for code thatÃ¢â‚¬â„¢s common for all targets.
  - Other folders are for Kotlin code that will be compiled for only the platform indicated in the folder name.
    For example, if you want to use AppleÃ¢â‚¬â„¢s CoreCrypto for the iOS part of your Kotlin app,
    the [iosMain](./shared/src/iosMain/kotlin) folder would be the right place for such calls.
    Similarly, if you want to edit the Desktop (JVM) specific part, the [jvmMain](./shared/src/jvmMain/kotlin)
    folder is the appropriate location.

### Running the apps

Use the run configurations provided by the run widget in your IDE's toolbar. You can also use these commands and options:

- Android app: `./gradlew :androidApp:assembleDebug`
- iOS app: open the [/iosApp](./iosApp) directory in Xcode and run it from there.

## Conectividad REST

El cliente compartido utiliza Ktor y `kotlinx.serialization`. La URL base actual
es `http://10.0.2.2:8080/` y corresponde al acceso al equipo anfitriÃƒÂ³n desde el
emulador Android. La direcciÃƒÂ³n para iOS requiere revisiÃƒÂ³n antes de ejecutar.

Se implementÃƒÂ³ `GET api/v1/productos` con los parÃƒÂ¡metros `pagina`, `tamanio=20`,
`ordenarPor=id` y `direccion=asc`. El repositorio acumula pÃƒÂ¡ginas desde cero
hasta que `ultima` sea `true`. Los DTO son `ProductoDto` y `PaginaProductosDto`;
el campo `estado` se convierte en `Producto.activo`.

El cliente configura `expectSuccess=true`, `ignoreUnknownKeys=true`, timeout de
peticiÃƒÂ³n de 15000 ms y conexiÃƒÂ³n de 10000 ms. El registro actual utiliza
`LogLevel.HEADERS`; para la evidencia de cuerpos completos se requiere ajustar
el registro durante la prueba. El ViewModel representa carga, resultados y error.

El registro remoto todavÃƒÂ­a lanza `UnsupportedOperationException`; las rutas de
consulta por ID, creaciÃƒÂ³n, actualizaciÃƒÂ³n y eliminaciÃƒÂ³n deben confirmarse con el
backend. No se han acreditado aquÃƒÂ­ los cinco escenarios de conexiÃƒÂ³n ni ejecuciÃƒÂ³n
en Android/iOS. El informe S07 indica explÃƒÂ­citamente las evidencias pendientes.

### Running tests

Use the run button in your IDE's editor gutter, or run tests using Gradle tasks:

- Android tests: `./gradlew :shared:testAndroidHostTest`
- iOS tests: `./gradlew :shared:iosSimulatorArm64Test`

---

Learn more about [Kotlin Multiplatform](https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html)Ã¢â‚¬Â¦


## Capacidades nativas (sesiÃƒÂ³n 09)

- `commonMain/platform/Formato.kt` declara `expect fun formatearSoles`.
- Android implementa el formato con `NumberFormat` en `androidMain/platform/Formato.android.kt`; iOS utiliza `NSNumberFormatter` en `iosMain/platform/Formato.ios.kt`, con la regiÃƒÂ³n PerÃƒÂº.
- `presentation/producto/ProductoUi.kt` prepara los precios antes de mostrarlos; el precio del dominio sigue siendo numÃƒÂ©rico.
- `domain/platform/Compartidor.kt` define el contrato. `domain/usecase/TextoParaCompartir.kt` prepara nombre, precio y stock.
- `CompartidorAndroid` utiliza `ACTION_SEND` y `FLAG_ACTIVITY_NEW_TASK`; `CompartidorIos` presenta `UIActivityViewController` desde la ventana activa y configura el popover de iPad.
- Cada `PlatformModule` registra su implementaciÃƒÂ³n en Koin, conservando el motor HTTP.
- En Productos, pulsa **Ver detalle** y luego **Compartir**. La pantalla comÃƒÂºn delega la acciÃƒÂ³n a `DetalleProductoViewModel`.

### VerificaciÃƒÂ³n y evidencias pendientes

Ejecutar Android con `gradlew.bat :androidApp:assembleDebug` y probar el selector en un emulador o telÃƒÂ©fono. Para iOS, compilar y ejecutar `iosApp` en macOS con Xcode. Las aplicaciones ofrecidas dependen de las instaladas en el dispositivo.

Guardar capturas del listado con moneda y de compartir en ambas plataformas. La captura del error por falta de `actual` debe obtenerse en el punto de control inicial de la prÃƒÂ¡ctica; no se incluye una evidencia ficticia. Documentar diferencias de formato y opciones de compartir.

Swift importa el framework `Shared`; `MainViewControllerKt.MainViewController()` abre la interfaz Compose y la inicializaciÃƒÂ³n de Koin estÃƒÂ¡ definida en `PlatformModule.ios.kt`.


## CÃ³digo especÃ­fico de plataforma

Las rutas Kotlin siguientes son relativas a `shared/src/<source set>/kotlin/pe/edu/upeu/pharmamobile/`.

| Capacidad o contrato | commonMain | androidMain | iosMain |
| --- | --- | --- | --- |
| Moneda `expect fun formatearSoles(valor: Double): String` | `platform/Formato.kt` | `platform/Formato.android.kt`, NumberFormat y Locale | `platform/Formato.ios.kt`, NSNumberFormatter y NSLocale |
| Compartir `interface Compartidor` (contrato con inyecciÃ³n) | `domain/platform/Compartidor.kt` | `platform/CompartidorAndroid.kt`, Intent.ACTION_SEND | `platform/CompartidorIos.kt`, UIActivityViewController |
| Dispositivo `expect class InfoDispositivo()` con sistema y version | `platform/InfoDispositivo.kt` | `platform/InfoDispositivo.kt`, Build.VERSION.RELEASE | `platform/InfoDispositivo.kt`, UIDevice.systemName y systemVersion |
| InyecciÃ³n `expect val platformModule: Module` | `di/AppModule.kt` | `di/PlatformModule.android.kt`, OkHttp y androidContext para Compartidor | `di/PlatformModule.ios.kt`, Darwin y CompartidorIos |
| URL `expect val backendBaseUrl: String` | `di/AppModule.kt` | `di/PlatformModule.android.kt`, direcciÃ³n 10.0.2.2 del emulador | `di/PlatformModule.ios.kt`, localhost del simulador |
| Plataforma `expect fun getPlatform(): Platform` heredada | `Platform.kt` | `Platform.android.kt`, Build.VERSION.SDK_INT | `Platform.ios.kt`, UIDevice.systemName y systemVersion |

### Tercera capacidad de la actividad autÃ³noma

Abrir **Acerca de** desde el menÃº lateral o la barra de navegaciÃ³n. La pantalla muestra el sistema operativo y su versiÃ³n real mediante `InfoDispositivo`. Android obtiene la versiÃ³n de Build; iOS la obtiene de UIDevice. La pantalla comÃºn no importa Android ni UIKit.

Para la evidencia, capturar esta pantalla en Android e iOS. La compilaciÃ³n de iOS requiere macOS y Xcode. Comparar tambiÃ©n el precio literal del mismo producto y la interfaz de compartir.
