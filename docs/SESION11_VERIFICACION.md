# Verificación de persistencia offline-first

Fecha: 20 de octubre de 2026.

## Resultado automático

- APK Android debug compilado correctamente.
- Compilación de pruebas Android en dispositivo correcta (sin ejecución en dispositivo).
- Código y pruebas Kotlin compilados para iosArm64 e iosSimulatorArm64.
- Las pruebas iOS no se ejecutaron: requieren macOS.

Comandos ejecutados correctamente:

```powershell
.\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug
.\gradlew.bat :shared:testAndroidHostTest :shared:compileKotlinIosArm64 :shared:compileKotlinIosSimulatorArm64 :shared:compileAndroidDeviceTest
.\gradlew.bat :shared:compileTestKotlinIosArm64 :shared:compileTestKotlinIosSimulatorArm64
```

Resultados de JUnit leídos de `shared/build/test-results/`:

| Clase | Pruebas | Fallos | Errores |
|---|---:|---:|---:|
| AuthRepositorioRestTest | 6 | 0 | 0 |
| ProductoRepositorioOfflineTest | 7 | 0 | 0 |
| ProductRepositoryTest | 3 | 0 | 0 |
| ClienteTest | 1 | 0 | 0 |
| ProductoViewModelTest | 6 | 0 | 0 |
| SesionViewModelTest | 1 | 0 | 0 |
| SharedCommonTest | 1 | 0 | 0 |
| SharedLogicAndroidHostTest | 1 | 0 | 0 |

Total: **26 pruebas aprobadas**.

El reporte navegable se genera en
`shared/build/reports/tests/testAndroidHostTest/index.html`.

## Cobertura nueva

- Alta sin red con ID negativo y estado pendiente.
- Descarga con red preservando campos del modelo.
- Subida antes de descarga y ausencia de reenvío de altas confirmadas.
- Fallo parcial durante la subida sin pérdida de pendientes.
- Actualización de datos sincronizados sin borrar pendientes.
- Edición y eliminación de un pendiente sin red.
- Persistencia del perfil y eliminación al cerrar sesión.
- Restauración de sesión sin red mediante AuthRepositorioRest.
- Rechazo HTTP 401 que elimina la sesión e impide restauración offline.
- Fallo de sincronización que conserva el listado local en el ViewModel.

## Evidencias manuales pendientes

Ejecutar el ciclo descrito en el README con PharmaSoft y comprobar en Swagger
el ID positivo. Tomar las capturas Android e iOS del listado sin red y del registro
pendiente. No se han simulado capturas ni verificación contra el servidor real.
