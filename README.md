This is a Kotlin Multiplatform project targeting Android, iOS.

* [/iosApp](./iosApp/iosApp) contains an iOS application. Even if you’re sharing your UI with Compose Multiplatform,
  you need this entry point for your iOS app. This is also where you should add SwiftUI code for your project.

* [/shared](./shared/src) is for code that will be shared across your Compose Multiplatform applications.
  It contains several subfolders:
  - [commonMain](./shared/src/commonMain/kotlin) is for code that’s common for all targets.
  - Other folders are for Kotlin code that will be compiled for only the platform indicated in the folder name.
    For example, if you want to use Apple’s CoreCrypto for the iOS part of your Kotlin app,
    the [iosMain](./shared/src/iosMain/kotlin) folder would be the right place for such calls.
    Similarly, if you want to edit the Desktop (JVM) specific part, the [jvmMain](./shared/src/jvmMain/kotlin)
    folder is the appropriate location.

### Running the apps

Use the run configurations provided by the run widget in your IDE's toolbar. You can also use these commands and options:

- Android app: `./gradlew :androidApp:assembleDebug`
- iOS app: open the [/iosApp](./iosApp) directory in Xcode and run it from there.

## Conectividad REST

El cliente compartido utiliza Ktor y `kotlinx.serialization`. La URL base actual
es `http://10.0.2.2:8080/` y corresponde al acceso al equipo anfitrión desde el
emulador Android. La dirección para iOS requiere revisión antes de ejecutar.

Se implementó `GET api/v1/productos` con los parámetros `pagina`, `tamanio=20`,
`ordenarPor=id` y `direccion=asc`. El repositorio acumula páginas desde cero
hasta que `ultima` sea `true`. Los DTO son `ProductoDto` y `PaginaProductosDto`;
el campo `estado` se convierte en `Producto.activo`.

El cliente configura `expectSuccess=true`, `ignoreUnknownKeys=true`, timeout de
petición de 15000 ms y conexión de 10000 ms. El registro actual utiliza
`LogLevel.HEADERS`; para la evidencia de cuerpos completos se requiere ajustar
el registro durante la prueba. El ViewModel representa carga, resultados y error.

El registro remoto todavía lanza `UnsupportedOperationException`; las rutas de
consulta por ID, creación, actualización y eliminación deben confirmarse con el
backend. No se han acreditado aquí los cinco escenarios de conexión ni ejecución
en Android/iOS. El informe S07 indica explícitamente las evidencias pendientes.

### Running tests

Use the run button in your IDE's editor gutter, or run tests using Gradle tasks:

- Android tests: `./gradlew :shared:testAndroidHostTest`
- iOS tests: `./gradlew :shared:iosSimulatorArm64Test`

---

Learn more about [Kotlin Multiplatform](https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html)…
