# Actividad autónoma 13: flujo y evidencias

Revisión: 10 de noviembre de 2026. Estudiante: Tania Antonella Baldeon Ramirez, código 202311724, grupo 2.

Estado: informe parcial. La revisión del código no sustituye una ejecución. Las capturas de `docs/captura/s13/` corresponden a evidencias previas y no acreditan un recorrido nuevo completo.

## A. Mapa del flujo completo

Ejecutar en una instalación de prueba sin borrar los datos del dispositivo habitual. No incluir contraseñas, JWT ni encabezados Authorization en las capturas.

| Paso | Acción y estado que debe registrarse | Evidencia actual |
| --- | --- | --- |
| 1 | Primera apertura: login, base local vacía y ausencia de token. La pantalla por sí sola no demuestra las dos últimas condiciones. | Pendiente de ejecución limpia. |
| 2 | Login correcto: token en almacenamiento seguro; anotar usuario, rol y privilegios devueltos por el servicio. | Implementado; falta captura del recorrido. |
| 3 | Primera sincronización: cantidad de filas y fecha UTC del último éxito. | La pantalla muestra ambos; falta captura. |
| 4 | Alta con conexión: nombre único e ID positivo del servidor, sin marca pendiente. | Implementado; falta captura y comprobación remota. |
| 5 | Alta en modo avión y sin Wi-Fi: ID local negativo y pendiente. | Captura previa `../captura/s13/05_pendiente_intento.png`. |
| 6 | Recuperar conexión y pulsar Sincronizar: anotar pendientes antes/después y sustitución del ID negativo por el definitivo. Comprobar que no se duplicó. | Pendiente. La sincronización es manual; no se afirma recuperación automática. |
| 7 | Provocar validación remota: registrar código HTTP y mensaje en el campo correspondiente. Una validación local no acredita HTTP 400. | Existe prueba automatizada; falta evidencia con el backend. |
| 8 | Cuenta sin escritura: formulario oculto; petición REST separada rechazada con 403. Comprobar que conserva la sesión. | Implementado; falta evidencia del rechazo remoto. |
| 9 | Token realmente vencido: petición protegida con 401, borrado del token y retorno a login con aviso. | Implementado; falta ejecución. Consultar duración real del JWT, sin asumir un minuto. |
| 10 | Cerrar sesión: login visible; token e identidad local borrados. Los productos permanecen en SQLite. | Verificado en código; falta captura y comprobación local. |

Para el paso 7, confirmar primero la restricción vigente en PharmaSoft. Si el nombre admite hasta 150 caracteres, usar 151 con los demás campos válidos. Para el paso 8, ocultar el token en la evidencia REST; no modificar los privilegios del usuario para conseguir la captura.

## B. Evidencias por plataforma

| Aspecto | Android | iOS |
| --- | --- | --- |
| Token | EncryptedSharedPreferences y Android Keystore; preferencias excluidas del respaldo. Reinstalación aún no ensayada. | Implementación Keychain; reinstalación sin verificar. |
| Permisos | POST_NOTIFICATIONS: solicitud en Android 13 o superior; salida a Ajustes en denegación definitiva. Capturas previas de los tres estados. | Adaptador UserNotifications; denegación dirige a Ajustes. Sin captura de ejecución. |
| Sin red | SQLDelight y altas locales pendientes. Sincronización explícita al recuperar conexión. | Repositorio compartido; recorrido visual pendiente. |
| Notificaciones | Notificación local de prueba, con captura previa. No equivale a recepción de FCM. | Adaptador de notificación local; entrega real sin verificar. |
| Interfaz | Capturas disponibles del catálogo y permisos. | Tipografías, barras y áreas seguras aún no comparadas. |

### Límite de iOS

La estación actual es Windows. El proyecto contiene `iosApp` e implementaciones `iosMain`, pero Xcode y la ejecución del simulador requieren macOS. No se atribuye un error de código que no se haya observado. Plan para sesión 14: abrir el mismo estado del proyecto en macOS con Xcode, compilar, ejecutar el recorrido y registrar las diferencias. No se presenta la presencia de código compartido como evidencia de ejecución iOS.

## C. Bitácora de permisos

El manifiesto Android declara INTERNET y POST_NOTIFICATIONS. INTERNET es un permiso normal, sin diálogo ni tres estados de solicitud en tiempo de ejecución.

| Estado de notificaciones | Qué ve el usuario | Cómo recupera la función | Captura previa |
| --- | --- | --- | --- |
| Concedido | Estado Concedido y botón Probar notificación. | Puede emitir el aviso de prueba. Si lo revoca, habilitarlo en Ajustes. | `03_permiso_concedido.png` |
| Denegado | Estado Denegado, explicación y botón Permitir notificaciones. | Solicitar otra vez mientras el sistema lo permita. El catálogo sigue disponible. | `01_permiso_denegado.png` |
| Denegado para siempre | Estado definitivo y botón Abrir Ajustes. | Ajustes de la aplicación > Notificaciones > permitir; regresar a PharmaMobil. El estado se consulta al reanudar. | `02_permiso_permanente.png` |

Capturas en `docs/captura/s13/`. `04_notificacion_real.png` muestra el aviso local. Falta registrar versión de Android, texto exacto del diálogo y número real de solicitudes durante un nuevo ensayo; no asumir que todos los sistemas permiten el mismo número. En Android anterior a 13 no hay diálogo POST_NOTIFICATIONS: si las notificaciones están deshabilitadas, se recuperan desde Ajustes.

## D. Ficha de integración

Las fechas siguientes son objetivos de cierre, no pruebas de cumplimiento.

| Hueco | Gravedad | Decisión | Fecha de cierre o revisión | Justificación/resultado |
| --- | --- | --- | --- | --- |
| Permiso y recuperación desde Ajustes | Media | Cerrado en implementación previa | Revisión 10/11/2026 | Adaptadores e interfaz existentes; tres capturas previas. Falta repetir el diálogo. |
| Evidencias de los diez pasos Android | Alta | Sesión 14 | 10/11/2026, objetivo | Backend local sin respuesta en 8080 durante esta revisión; no se acreditó un recorrido completo. |
| Reinstalación y limpieza inicial | Media | Sesión 14 | 10/11/2026, objetivo | Usar instalación de prueba para conservar datos actuales. |
| Recorrido iOS y comparación visual | Alta | Sesión 14 | 10/11/2026, revisión | Requiere acceso a macOS/Xcode; registrar resultado real. |
| Reenvío de POST sin idempotencia | Alta | Sesión 14 | 10/11/2026, revisión | Una respuesta perdida puede duplicar un alta. Acordar contrato con PharmaSoft; no cambiar arquitectura en esta actividad documental. |
| Catálogo local conservado al salir | Media | Sesión 14 | 10/11/2026, revisión | Confirmar política de datos entre usuarios antes de cambiar el comportamiento existente. |
| Cámara y ubicación | Baja | Descartado | 10/11/2026 | No forman parte del recorrido de catálogo; no añadir permisos sin una función que los necesite. |

## Repositorio y entrega

- Rama solicitada y actual: https://github.com/antobaldeon/Pharmamobile/tree/feature/integrador-13
- Commit base: https://github.com/antobaldeon/Pharmamobile/commit/5b3aba229bfdfb2a427f79fb4a6953884f49baf3
- Hay cambios locales anteriores y de esta revisión sin commit. El commit base no representa esos cambios. El enlace al commit evaluado debe actualizarse cuando se consolide el trabajo.
- Formato solicitado: PDF carta, portada e índice, entre 8 y 14 páginas, menos de 20 MB. Nombre final: `Baldeon_Tania_Sesion13_Evidencias.pdf`.
- La guía indica entrega el 09/11/2026 a las 23:59. Este estado fue revisado el 10/11/2026; no se antedata.
- El PDF parcial permanece identificado como revisión hasta completar las capturas. No se debe entregar como evidencia completa.

Ejecución de pruebas y compilación:

```powershell
.\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug --console=plain
```

Consultar `VERIFICACION.md` para el resultado de esta revisión y `COMO_PROBAR.md` para el recorrido detallado.
