# Firma, build e instalación - sesión 14

## Configuración de firma

Se creó la primera clave del equipo el 10/11/2026, alias `pharmamobil`, RSA 2048, JKS y vigencia de 10000 días. Está fuera del repositorio en `C:/Users/tania/.pharmamobil-signing/pharmamobil-release.jks`. Las credenciales están en `keystore.properties` local y en una copia junto al almacén; no se imprimen ni se incluyen en el informe.

Hay que respaldar esa carpeta completa en un lugar seguro fuera de esta laptop. La copia de credenciales en el mismo disco no sustituye ese respaldo del equipo.

Para otro integrante, crear en la raíz un `keystore.properties` con los siguientes campos, obteniendo las credenciales por un medio privado:

```properties
storeFile=C:/ruta/privada/pharmamobil-release.jks
storePassword=CONTRASENA_LOCAL
keyAlias=pharmamobil
keyPassword=CONTRASENA_LOCAL
```

Usar `/` en las rutas de Windows. `.gitignore` excluye `keystore.properties`, `*.jks` y `*.keystore`. Sin credenciales, debug debe seguir compilando; release se detiene con una indicación para configurarlas. No usar una clave debug como sustituto.

## Build para celulares en la red local

La app recibe la URL mediante metadatos Android configurados por Gradle y la inyecta en Ktor. El valor predeterminado sigue siendo el emulador `http://10.0.2.2:8080/`; iOS conserva su configuración anterior. Para teléfonos físicos, usar la IPv4 de Wi-Fi de la laptop, no las interfaces de VMware o WSL.

IPv4 observada el 10/11/2026: `10.40.30.138`. Puede cambiar al reconectar la laptop. Comprobar con `ipconfig` antes de generar el build y abrir `http://<IP>:8080/` desde el teléfono para verificar que el puerto responde. PharmaSoft debe estar iniciado y Windows debe permitir conexiones entrantes al puerto 8080. Algunas redes Wi-Fi aíslan clientes.

```powershell
$env:JAVA_HOME = 'C:/Program Files/Android/Android Studio/jbr'
.\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug `
  :androidApp:assembleRelease :androidApp:bundleRelease `
  -PpharmaBackendUrl=http://10.40.30.138:8080/ -PpharmaAllowHttp=true --console=plain
```

`pharmaAllowHttp=true` habilita HTTP explícitamente para esta revisión con el servicio local. Para distribución con HTTPS, omitir esa opción y proporcionar la URL HTTPS. El valor predeterminado de release bloquea HTTP. No configurar una URL HTTPS que el servicio no ofrezca realmente.

Salidas originales:

- `androidApp/build/outputs/bundle/release/androidApp-release.aab`
- `androidApp/build/outputs/apk/release/androidApp-release.apk`
- `androidApp/build/outputs/mapping/release/mapping.txt` (conservar para interpretar fallos ofuscados).

El APK se instala; el AAB no se instala directamente. Copiar el APK al teléfono y abrirlo para instalar, autorizando la instalación desde esa fuente si Android la solicita. Si ya hay una instalación debug con el mismo identificador, Android puede rechazar la actualización por firma distinta: preservar los datos y usar un dispositivo de prueba limpio; no desinstalar la app habitual sin respaldo.

No compilar ni entregar una variante sin minificación para ocultar un fallo. Este release usa R8. Si aparece un fallo de serialización o inyección en el recorrido real, conservar Logcat, agregar solo la regla necesaria y repetir las pruebas.

### Herramienta de minificación

El proyecto usa Kotlin 2.4.10. La primera compilación con el R8 incluido en AGP produjo avisos de metadatos incompatibles. Se fijó R8 9.1.29 en `pluginManagement.buildscript`, obtenido del repositorio oficial de R8; no se cambió Kotlin, AGP ni las dependencias de la aplicación. Referencias: [compatibilidad Kotlin/R8](https://developer.android.com/build/kotlin-support) y [sustitución de R8 en AGP](https://r8.googlesource.com/r8/+/refs/heads/main/README.md#Replacing-R8-in-Android-Gradle-plugin).

La subida automática de `mapping.txt` a Crashlytics quedó deshabilitada en release. El mapa se conserva localmente. La revisión automática rechazó una nueva compilación que incluía esa subida; los builds posteriores la excluyen. Sin subir el mapa, las trazas de ese release en Firebase permanecen ofuscadas. Configuración documentada por [Firebase](https://firebase.google.com/docs/crashlytics/android/get-deobfuscated-reports).

## Verificación del certificado

```powershell
& "$env:LOCALAPPDATA/Android/Sdk/build-tools/36.0.0/apksigner.bat" verify --verbose --print-certs `
  androidApp/build/outputs/apk/release/androidApp-release.apk
& "$env:JAVA_HOME/bin/jarsigner.exe" -verify `
  androidApp/build/outputs/bundle/release/androidApp-release.aab
```

Guardar la salida y una captura con titular y huella visibles. Las contraseñas no forman parte de la evidencia. La verificación de firma no acredita funcionamiento de red, serialización ni inyección en dispositivos.

## Ficha de versión

| Dato | Valor |
| --- | --- |
| applicationId | pe.edu.upeu.pharmamobile (se conserva el existente) |
| versionCode | 1 |
| versionName | 1.0.0 |
| Alias | pharmamobil |
| Rama | feature/builds-14 |
| Git tag final | Pendiente de pruebas y commit definitivo; no creado |
| Nombre de entrega autorizado | Baldeon_ProyectoFinal_Android.aab y Baldeon_ProyectoFinal_Android.apk |

La estudiante indicó usar `Baldeon` en lugar de la nomenclatura por equipo. Se conservan también las salidas originales de Gradle.

## Alcance de plataforma

Android cuenta con APK y AAB firmados. La estudiante retomó iOS porque su único teléfono es un iPhone: [preparación y limitación de macOS](IOS_EN_IPHONE.md). No se generó un IPA ni se acreditó instalación iOS desde Windows.

## Cierre

Completar la matriz en `ALCANCE_Y_PRUEBAS.md`, respaldar la clave, consolidar el código en Git y generar los builds definitivos desde ese commit. Verificar otra vez firma y recorrido antes de etiquetar `v1.0-final`. La entrega de builds es el 16/11/2026 y la sustentación el 17/11/2026.
