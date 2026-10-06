This is a Kotlin Multiplatform project targeting Android, iOS.

* [/iosApp](./iosApp/iosApp) contains an iOS application. Even if youâ€™re sharing your UI with Compose Multiplatform,
  you need this entry point for your iOS app. This is also where you should add SwiftUI code for your project.

* [/shared](./shared/src) is for code that will be shared across your Compose Multiplatform applications.
  It contains several subfolders:
  - [commonMain](./shared/src/commonMain/kotlin) is for code thatâ€™s common for all targets.
  - Other folders are for Kotlin code that will be compiled for only the platform indicated in the folder name.
    For example, if you want to use Appleâ€™s CoreCrypto for the iOS part of your Kotlin app,
    the [iosMain](./shared/src/iosMain/kotlin) folder would be the right place for such calls.
    Similarly, if you want to edit the Desktop (JVM) specific part, the [jvmMain](./shared/src/jvmMain/kotlin)
    folder is the appropriate location.

### Running the apps

Use the run configurations provided by the run widget in your IDE's toolbar. You can also use these commands and options:

- Android app: `./gradlew :androidApp:assembleDebug`
- iOS app: open the [/iosApp](./iosApp) directory in Xcode and run it from there.

## Conectividad REST

El cliente compartido utiliza Ktor y `kotlinx.serialization`. La URL base actual
es `http://10.0.2.2:8080/` y corresponde al acceso al equipo anfitriÃ³n desde el
emulador Android. La direcciÃ³n para iOS requiere revisiÃ³n antes de ejecutar.

Se implementÃ³ `GET api/v1/productos` con los parÃ¡metros `pagina`, `tamanio=20`,
`ordenarPor=id` y `direccion=asc`. El repositorio acumula pÃ¡ginas desde cero
hasta que `ultima` sea `true`. Los DTO son `ProductoDto` y `PaginaProductosDto`;
el campo `estado` se convierte en `Producto.activo`.

El cliente configura `expectSuccess=true`, `ignoreUnknownKeys=true`, timeout de
peticiÃ³n de 15000 ms y conexiÃ³n de 10000 ms. El registro actual utiliza
`LogLevel.HEADERS`; para la evidencia de cuerpos completos se requiere ajustar
el registro durante la prueba. El ViewModel representa carga, resultados y error.

El registro remoto todavÃ­a lanza `UnsupportedOperationException`; las rutas de
consulta por ID, creaciÃ³n, actualizaciÃ³n y eliminaciÃ³n deben confirmarse con el
backend. No se han acreditado aquÃ­ los cinco escenarios de conexiÃ³n ni ejecuciÃ³n
en Android/iOS. El informe S07 indica explÃ­citamente las evidencias pendientes.

### Running tests

Use the run button in your IDE's editor gutter, or run tests using Gradle tasks:

- Android tests: `./gradlew :shared:testAndroidHostTest`
- iOS tests: `./gradlew :shared:iosSimulatorArm64Test`

---

Learn more about [Kotlin Multiplatform](https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html)â€¦


## Capacidades nativas (sesiÃ³n 09)

- `commonMain/platform/Formato.kt` declara `expect fun formatearSoles`.
- Android implementa el formato con `NumberFormat` en `androidMain/platform/Formato.android.kt`; iOS utiliza `NSNumberFormatter` en `iosMain/platform/Formato.ios.kt`, con la regiÃ³n PerÃº.
- `presentation/producto/ProductoUi.kt` prepara los precios antes de mostrarlos; el precio del dominio sigue siendo numÃ©rico.
- `domain/platform/Compartidor.kt` define el contrato. `domain/usecase/TextoParaCompartir.kt` prepara nombre, precio y stock.
- `CompartidorAndroid` utiliza `ACTION_SEND` y `FLAG_ACTIVITY_NEW_TASK`; `CompartidorIos` presenta `UIActivityViewController` desde la ventana activa y configura el popover de iPad.
- Cada `PlatformModule` registra su implementaciÃ³n en Koin, conservando el motor HTTP.
- En Productos, pulsa **Ver detalle** y luego **Compartir**. La pantalla comÃºn delega la acciÃ³n a `DetalleProductoViewModel`.

### VerificaciÃ³n y evidencias pendientes

Ejecutar Android con `gradlew.bat :androidApp:assembleDebug` y probar el selector en un emulador o telÃ©fono. Para iOS, compilar y ejecutar `iosApp` en macOS con Xcode. Las aplicaciones ofrecidas dependen de las instaladas en el dispositivo.

Guardar capturas del listado con moneda y de compartir en ambas plataformas. La captura del error por falta de `actual` debe obtenerse en el punto de control inicial de la prÃ¡ctica; no se incluye una evidencia ficticia. Documentar diferencias de formato y opciones de compartir.

Swift importa el framework `Shared`; `MainViewControllerKt.MainViewController()` abre la interfaz Compose y la inicializaciÃ³n de Koin estÃ¡ definida en `PlatformModule.ios.kt`.
