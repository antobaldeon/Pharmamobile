This is a Kotlin Multiplatform project targeting Android, iOS.

* [/iosApp](./iosApp/iosApp) contains an iOS application. Even if youÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢re sharing your UI with Compose Multiplatform,
  you need this entry point for your iOS app. This is also where you should add SwiftUI code for your project.

* [/shared](./shared/src) is for code that will be shared across your Compose Multiplatform applications.
  It contains several subfolders:
  - [commonMain](./shared/src/commonMain/kotlin) is for code thatÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s common for all targets.
  - Other folders are for Kotlin code that will be compiled for only the platform indicated in the folder name.
    For example, if you want to use AppleÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s CoreCrypto for the iOS part of your Kotlin app,
    the [iosMain](./shared/src/iosMain/kotlin) folder would be the right place for such calls.
    Similarly, if you want to edit the Desktop (JVM) specific part, the [jvmMain](./shared/src/jvmMain/kotlin)
    folder is the appropriate location.

### Running the apps

Use the run configurations provided by the run widget in your IDE's toolbar. You can also use these commands and options:

- Android app: `./gradlew :androidApp:assembleDebug`
- iOS app: open the [/iosApp](./iosApp) directory in Xcode and run it from there.

## Conectividad REST

El cliente compartido utiliza Ktor y `kotlinx.serialization`. La URL base actual
es `http://10.0.2.2:8080/` y corresponde al acceso al equipo anfitriÃƒÆ’Ã‚Â³n desde el
emulador Android. La direcciÃƒÆ’Ã‚Â³n para iOS requiere revisiÃƒÆ’Ã‚Â³n antes de ejecutar.

Se implementÃƒÆ’Ã‚Â³ `GET api/v1/productos` con los parÃƒÆ’Ã‚Â¡metros `pagina`, `tamanio=20`,
`ordenarPor=id` y `direccion=asc`. El repositorio acumula pÃƒÆ’Ã‚Â¡ginas desde cero
hasta que `ultima` sea `true`. Los DTO son `ProductoDto` y `PaginaProductosDto`;
el campo `estado` se convierte en `Producto.activo`.

El cliente configura `expectSuccess=true`, `ignoreUnknownKeys=true`, timeout de
peticiÃƒÆ’Ã‚Â³n de 15000 ms y conexiÃƒÆ’Ã‚Â³n de 10000 ms. El registro actual utiliza
`LogLevel.HEADERS`; para la evidencia de cuerpos completos se requiere ajustar
el registro durante la prueba. El ViewModel representa carga, resultados y error.

El registro remoto todavÃƒÆ’Ã‚Â­a lanza `UnsupportedOperationException`; las rutas de
consulta por ID, creaciÃƒÆ’Ã‚Â³n, actualizaciÃƒÆ’Ã‚Â³n y eliminaciÃƒÆ’Ã‚Â³n deben confirmarse con el
backend. No se han acreditado aquÃƒÆ’Ã‚Â­ los cinco escenarios de conexiÃƒÆ’Ã‚Â³n ni ejecuciÃƒÆ’Ã‚Â³n
en Android/iOS. El informe S07 indica explÃƒÆ’Ã‚Â­citamente las evidencias pendientes.

### Running tests

Use the run button in your IDE's editor gutter, or run tests using Gradle tasks:

- Android tests: `./gradlew :shared:testAndroidHostTest`
- iOS tests: `./gradlew :shared:iosSimulatorArm64Test`

---

Learn more about [Kotlin Multiplatform](https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html)ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦


## Capacidades nativas (sesiÃƒÆ’Ã‚Â³n 09)

- `commonMain/platform/Formato.kt` declara `expect fun formatearSoles`.
- Android implementa el formato con `NumberFormat` en `androidMain/platform/Formato.android.kt`; iOS utiliza `NSNumberFormatter` en `iosMain/platform/Formato.ios.kt`, con la regiÃƒÆ’Ã‚Â³n PerÃƒÆ’Ã‚Âº.
- `presentation/producto/ProductoUi.kt` prepara los precios antes de mostrarlos; el precio del dominio sigue siendo numÃƒÆ’Ã‚Â©rico.
- `domain/platform/Compartidor.kt` define el contrato. `domain/usecase/TextoParaCompartir.kt` prepara nombre, precio y stock.
- `CompartidorAndroid` utiliza `ACTION_SEND` y `FLAG_ACTIVITY_NEW_TASK`; `CompartidorIos` presenta `UIActivityViewController` desde la ventana activa y configura el popover de iPad.
- Cada `PlatformModule` registra su implementaciÃƒÆ’Ã‚Â³n en Koin, conservando el motor HTTP.
- En Productos, pulsa **Ver detalle** y luego **Compartir**. La pantalla comÃƒÆ’Ã‚Âºn delega la acciÃƒÆ’Ã‚Â³n a `DetalleProductoViewModel`.

### VerificaciÃƒÆ’Ã‚Â³n y evidencias pendientes

Ejecutar Android con `gradlew.bat :androidApp:assembleDebug` y probar el selector en un emulador o telÃƒÆ’Ã‚Â©fono. Para iOS, compilar y ejecutar `iosApp` en macOS con Xcode. Las aplicaciones ofrecidas dependen de las instaladas en el dispositivo.

Guardar capturas del listado con moneda y de compartir en ambas plataformas. La captura del error por falta de `actual` debe obtenerse en el punto de control inicial de la prÃƒÆ’Ã‚Â¡ctica; no se incluye una evidencia ficticia. Documentar diferencias de formato y opciones de compartir.

Swift importa el framework `Shared`; `MainViewControllerKt.MainViewController()` abre la interfaz Compose y la inicializaciÃƒÆ’Ã‚Â³n de Koin estÃƒÆ’Ã‚Â¡ definida en `PlatformModule.ios.kt`.


## CÃƒÂ³digo especÃƒÂ­fico de plataforma

Las rutas Kotlin siguientes son relativas a `shared/src/<source set>/kotlin/pe/edu/upeu/pharmamobile/`.

| Capacidad o contrato | commonMain | androidMain | iosMain |
| --- | --- | --- | --- |
| Moneda `expect fun formatearSoles(valor: Double): String` | `platform/Formato.kt` | `platform/Formato.android.kt`, NumberFormat y Locale | `platform/Formato.ios.kt`, NSNumberFormatter y NSLocale |
| Compartir `interface Compartidor` (contrato con inyecciÃƒÂ³n) | `domain/platform/Compartidor.kt` | `platform/CompartidorAndroid.kt`, Intent.ACTION_SEND | `platform/CompartidorIos.kt`, UIActivityViewController |
| Dispositivo `expect class InfoDispositivo()` con sistema y version | `platform/InfoDispositivo.kt` | `platform/InfoDispositivo.kt`, Build.VERSION.RELEASE | `platform/InfoDispositivo.kt`, UIDevice.systemName y systemVersion |
| InyecciÃƒÂ³n `expect val platformModule: Module` | `di/AppModule.kt` | `di/PlatformModule.android.kt`, OkHttp y androidContext para Compartidor | `di/PlatformModule.ios.kt`, Darwin y CompartidorIos |
| URL `expect val backendBaseUrl: String` | `di/AppModule.kt` | `di/PlatformModule.android.kt`, direcciÃƒÂ³n 10.0.2.2 del emulador | `di/PlatformModule.ios.kt`, localhost del simulador |
| Plataforma `expect fun getPlatform(): Platform` heredada | `Platform.kt` | `Platform.android.kt`, Build.VERSION.SDK_INT | `Platform.ios.kt`, UIDevice.systemName y systemVersion |

### Tercera capacidad de la actividad autÃƒÂ³noma

Abrir **Acerca de** desde el menÃƒÂº lateral o la barra de navegaciÃƒÂ³n. La pantalla muestra el sistema operativo y su versiÃƒÂ³n real mediante `InfoDispositivo`. Android obtiene la versiÃƒÂ³n de Build; iOS la obtiene de UIDevice. La pantalla comÃƒÂºn no importa Android ni UIKit.

Para la evidencia, capturar esta pantalla en Android e iOS. La compilaciÃƒÂ³n de iOS requiere macOS y Xcode. Comparar tambiÃƒÂ©n el precio literal del mismo producto y la interfaz de compartir.


## Autenticación — Sesión 10

<!-- [Sesion 10 | Documentacion] Resume configuracion, permisos y verificaciones JWT. -->
PharmaMobil autentica contra `POST /api/v1/auth/login` y recupera la identidad
con `GET /api/v1/auth/me`. La URL base ya incluye el host; las rutas incluyen
`api/v1/`. Android usa `10.0.2.2:8080` y el simulador iOS usa `localhost:8080`.
PharmaSoft y Oracle deben estar iniciados, con las migraciones V2 y V3 aplicadas.

| Usuario | Contraseña | Acceso |
| --- | --- | --- |
| admin | Admin123 | Todos los permisos |
| vendedor | Vendedor123 | Catálogo de lectura; clientes y ventas |
| almacen | Almacen123 | Lectura y escritura de catálogo |

El token se guarda en preferencias cifradas con Android Keystore o en Keychain
en iOS. El plugin Auth de Ktor adjunta Bearer; login se excluye de autenticación.
Después de guardar o borrar el token se limpia la caché Bearer. Los registros
solo se activan en depuración y ocultan Authorization; no registran contraseñas.
Un 401 protegido elimina la sesión y muestra login con aviso; un 403 conserva
la sesión y muestra falta de permisos. El formulario, editar y eliminar producto
requieren `CATALOGO_ESCRIBIR`; el menú filtra clientes y ventas por permisos.
Las pantallas existentes de clientes y pedidos conservan su implementación previa;
esta sesión incorpora autenticación al CRUD REST de productos ya disponible.

### Verificación manual
1. Iniciar sesión con cada usuario y comprobar acciones disponibles.
2. Cerrar y reabrir la app: recupera sesión mediante `/auth/me`.
3. Cerrar sesión e iniciar con otro usuario: recarga productos con la nueva sesión.
4. Provocar un 401 con token inválido/expirado: volver al login con aviso.
5. Provocar un 403: conservar sesión y mostrar mensaje de falta de permisos.
6. Revisar Logcat: Authorization oculto; no aparece el token ni la contraseña.
7. Compilar y probar iOS desde macOS/Xcode; Windows no ejecuta esos destinos.

Los comentarios agregados usan `[Sesion 10 | finalidad]` para identificar la
sesión y el propósito. Los comentarios anteriores conservan sus etiquetas originales.

### Validación realizada
- APK Android debug generado correctamente.
- 15 pruebas Android aprobadas, incluyendo 4 pruebas nuevas de autenticación.
- Código Kotlin compilado para iPhone (`iosArm64`) y simulador (`iosSimulatorArm64`).
- Ejecución real del login y migraciones pendiente de iniciar Oracle y PharmaSoft.
- Ejecución y enlace final de la app iOS pendiente de macOS/Xcode.

```powershell
.\gradlew.bat :shared:testAndroidHostTest :shared:compileKotlinIosSimulatorArm64 :shared:compileKotlinIosArm64 :androidApp:assembleDebug
```
