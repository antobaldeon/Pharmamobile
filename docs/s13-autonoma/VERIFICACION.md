# Verificación de la actividad autónoma 13

Fecha: 10 de noviembre de 2026.

- Suite Android Host ejecutada nuevamente con `:shared:testAndroidHostTest --rerun --offline`: 46 pruebas, cero fallos, cero errores y cero omitidas. Resultado: BUILD SUCCESSFUL.
- Compilación `:androidApp:assembleDebug --offline`: BUILD SUCCESSFUL. El APK existente estaba actualizado; Gradle no necesitó reconstruirlo. No es un release firmado.
- Las pruebas cubren autenticación, validación por campo, persistencia offline, intentos de envío, clasificación de permisos y migración de SQLite.
- Android: ADB respondió correctamente; la lista de dispositivos conectados estaba vacía. No se capturó un recorrido nuevo ni se borraron datos.
- Backend: no hubo respuesta TCP en localhost:8080. No se realizaron altas reales ni se acreditaron respuestas HTTP 400, 403 o 401 en esta revisión.
- iOS: Gradle indicó que iosSimulatorArm64Test está deshabilitado en windows-x86_64 porque requiere macOS. No se acredita ejecución iOS.
- Los cambios de esta revisión son documentación y el PDF parcial. No se modificaron funciones, dependencias, arquitectura ni archivos de configuración de la aplicación.

Comandos ejecutados desde la raíz, con el JDK de Android Studio:

```powershell
$env:JAVA_HOME = 'C:/Program Files/Android/Android Studio/jbr'
.\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug --console=plain --offline
.\gradlew.bat :shared:testAndroidHostTest --rerun --console=plain --offline
```

Reporte HTML: `shared/build/reports/tests/testAndroidHostTest/index.html`.
Resultados por suite: `shared/build/test-results/testAndroidHostTest/TEST-*.xml`.

Queda pendiente ejecutar el recorrido con PharmaSoft accesible y un dispositivo o emulador, completar capturas y enlazar el commit que incluya los cambios locales. Las capturas anteriores permanecen identificadas como previas.
