# Verificación de práctica 14

## Actualización posterior de pruebas y sesión

Cambio posterior de red: la IPv4 Wi-Fi pasó de `172.17.26.38` a `10.40.30.138`. La primera dirección agotó el tiempo de conexión y la actual respondió HTTP 401 al endpoint protegido. Se regeneraron y verificaron los paquetes release con la nueva IP; se actualizaron los archivos y hashes. La variante debug se compiló por separado con su valor predeterminado `10.0.2.2`, exclusivo del emulador y ajeno a los cambios de IPv4 Wi-Fi. No se borraron ni reenviaron productos. Logs: `tmp/s14-cambio-ip.log` y `tmp/s14-emulador-url.log`. El informe Word/PDF previo conserva su corte anterior de dirección y hashes.

Corrección posterior de avisos de envío: se confirmó `GET /api/v1/categorias` con HTTP 200 y lista vacía. A solicitud de la estudiante se crearon Medicamentos (ID 1) y Analgésicos (ID 2), ambas activas. El producto pendiente no se borró ni se volvió a crear. Los rechazos permanentes detienen el envío asignando el límite interno de intentos; ese valor no acredita cinco llamadas reales. La interfaz ahora muestra Envío detenido, permite Corregir producto y limpia avisos obsoletos al editar o volver a operar. Se regeneraron APK/AAB y se verificaron sus firmas. La suite pasó con 48 pruebas, cero fallos y cero errores, incluidas dos regresiones para edición y reenvío. El éxito del reenvío del Paracetamol debe comprobarse en el dispositivo. Log: `tmp/s14-corregir-reintentos.log`. Los hashes del informe Word/PDF anterior corresponden a su corte de generación; los actuales están en `SHA256.txt`.

Los apartados iniciales conservan el resultado del primer corte. Posteriormente se aportó una fotografía de la app abierta en un teléfono Android con error de conexión al iniciar sesión. Por ello ya existe evidencia de apertura física, pero no de un recorrido exitoso. La estudiante confirmó HTTP 401 desde Chrome del teléfono al consultar productos sin token; la causa del fallo en el APK sigue pendiente de Logcat. No se conoce el modelo ni la versión del teléfono.

PharmaSoft respondió al login REST desde la laptop. En el perfil dev se amplió la expiración de 1 minuto a `${JWT_EXPIRACION_MINUTOS:480}` y, después de reiniciar el servidor, se verificó `exp - iat = 28800` segundos. Los nuevos tokens duran ocho horas; producción no se modificó. Esta verificación no implica haber completado ocho horas de uso físico.

El informe de documentación incorpora estas evidencias y mantiene pendientes el login físico, la matriz completa, el segundo y tercer dispositivos, la captura visual de firma y la firma/instalación iOS.

Fecha: 10/11/2026. Rama: `feature/builds-14`. Los cambios locales todavía no están consolidados en un commit; no se creó la etiqueta final.

## Android

Build con minificación habilitada y R8 9.1.29: BUILD SUCCESSFUL. La nueva compilación no presentó el aviso de metadatos Kotlin del R8 anterior. No se añadieron reglas generales de conservación ni se desactivó la minificación.

```powershell
$env:JAVA_HOME = 'C:/Program Files/Android/Android Studio/jbr'
.\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug `
  :androidApp:bundleRelease :androidApp:assembleRelease `
  -PpharmaBackendUrl=http://172.17.26.38:8080/ -PpharmaAllowHttp=true --console=plain
```

- Suite Android Host: 46 pruebas, cero fallos, cero errores y cero omitidas. Log de compilación en `tmp/s14-build.log`.
- APK: `output/android/s14/Baldeon_ProyectoFinal_Android.apk`, 3 358 576 bytes.
- AAB: `output/android/s14/Baldeon_ProyectoFinal_Android.aab`, 6 448 717 bytes.
- Mapa R8 preservado en `output/android/s14/mapping.txt`, con cabecera `compiler_version: 9.1.29`.
- `aapt2 dump badging`: applicationId `pe.edu.upeu.pharmamobile`, versionCode `1`, versionName `1.0.0`, target SDK `36`.
- Manifiesto release: URL `http://172.17.26.38:8080/` y HTTP habilitado explícitamente para el laboratorio. La IP puede cambiar; regenerar si cambia la red.
- `apksigner verify --verbose --print-certs`: Verifies, esquema v2 válido, un firmante RSA 2048.
- `jarsigner -verify`: jar verified. Conserva avisos del verificador Java sobre certificado autofirmado, ausencia de timestamp y lectura ZIP como stream; no se presentan como validación de bundletool ni como ejecución en un dispositivo.
- El certificado del AAB, extraído con `keytool -printcert -jarfile`, coincide con el del APK.
- Titular: `CN=Equipo PharmaMobil, OU=Desarrollo, O=PharmaMobil, L=Lima, C=PE`.
- Huella SHA-256 del certificado: `E91E0751E2960BD3D6C6C61D09068464F121891968C9E28AFEE2C82A78574BBB`.
- Evidencias: `FIRMA_APK.txt`, `FIRMA_AAB.txt`, `CERTIFICADO_AAB.txt` y `SHA256.txt` en esta carpeta. Los hashes de archivos no son la huella del certificado.

Prueba sin credenciales: se retiró temporalmente el archivo local, se ejecutó `assembleDebug --offline --no-configuration-cache` y se obtuvo BUILD SUCCESSFUL. `preReleaseBuild` falló deliberadamente con «Configura keystore.properties con las credenciales del equipo para generar release». El archivo se restauró mediante `finally` y se comprobó su existencia. Los registros están en `tmp/s14-debug-sin-clave.log` y `tmp/s14-release-sin-clave.log`.

Git ignora `keystore.properties`, `*.jks` y `*.keystore`; `git ls-files` no encontró esos archivos versionados. La clave está fuera del repositorio. Sigue pendiente un respaldo seguro fuera de esta laptop.

## iOS

```powershell
.\gradlew.bat :shared:compileKotlinIosArm64 --offline --console=plain
```

Resultado después de los ajustes: BUILD SUCCESSFUL. Se verificó además que Info.plist es XML válido y que el proyecto OpenStep tiene sintaxis y referencias internas válidas para los productos SPM añadidos. Estas comprobaciones no sustituyen Xcode.

No se compiló Swift, no se resolvieron los paquetes con Xcode, no se enlazó la aplicación final, no se generó `.xcarchive`/IPA y no se instaló en el iPhone. La estudiante dispone solo de Windows y un iPhone 15 Pro Max (iOS 26.6 declarado). Falta acceso a macOS con Xcode y configurar el equipo Apple real. Preparación en `IOS_EN_IPHONE.md`.

## Límites y cierre pendiente

- ADB respondió con lista vacía: no hay ejecución física Android acreditada.
- PharmaSoft no respondió en localhost:8080 durante la revisión. No se acreditó el recorrido real contra backend.
- Las pruebas de serialización, inyección y permisos en el APK minificado siguen pendientes en la matriz; la compilación no las sustituye.
- Falta la captura visual de la verificación de firma; las salidas originales están conservadas.
- No se acredita la matriz de dos teléfonos Android ni el tercer dispositivo autónomo. Solo se declaró un iPhone disponible.
- Falta consolidar commits, generar el build definitivo desde ese estado, verificarlo y etiquetar. Se preservaron los cambios previos del directorio de trabajo.

La revisión automática rechazó una recompilación que incluía la subida del mapa de ofuscación a Firebase. Se continuó con una alternativa local: `mappingFileUploadEnabled=false`. La tarea de subida dejó de generarse y no forma parte del build final. No se solicita autorización adicional para esa subida porque quedó deshabilitada.

## Regeneración con pantalla limpia

Se regeneraron APK y AAB después de quitar el bloque de diagnóstico y prueba de notificaciones de Productos. Build release correcto, firmas verificadas y mismo certificado del equipo. Las salidas anteriores se reemplazaron por las nuevas y se actualizaron SHA256.txt y mapping.txt. Log: `tmp/s14-regenerar.log`. No se ejecutó un nuevo recorrido físico.
