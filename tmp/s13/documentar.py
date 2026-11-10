from pathlib import Path
p=Path('docs/SESION13_INTEGRADOR.md')
p.write_text('''# Sesión 13 Proyecto integrador

## Implementación

La migración `2.sqm` amplía la base a versión 3 sin borrar productos. Guarda
`intentos` y `ultimoError` por fila. Cinco intentos agotan la fila; validación,
conflicto, no encontrado, falta de permiso y sesión expirada la marcan fallida.
Las filas fallidas siguen visibles y la descarga conserva todos los pendientes.

Los POST no usan una clave idempotente en PharmaSoft. Por ello no se implementa
un bucle automático de reenvíos inciertos. Una pulsación de Sincronizar autoriza
un nuevo intento de los transitorios; los fallidos requieren confirmar el reenvío
por fila o editar su contenido. Se informa al usuario que compruebe antes si el
producto ya existe. La espera antes de los reenvíos crece 1, 2, 4, 8 y 16 segundos.
La creación de otro producto no reenvía automáticamente los fallos anteriores.

La pantalla calcula pendientes y fallidas desde el Flow local, muestra el error
por producto y conserva la última sincronización correcta. La marca no se actualiza
cuando ocurre un fallo de envío. Los fallidos excluidos no bloquean la descarga.
Editar un pendiente reinicia su estado para permitir corregir una validación.

## Permiso real de notificaciones

El dominio declara GestorPermisos y los tres estados. Android recuerda si se pidió
el permiso y consulta la explicación del sistema para distinguir primera solicitud
y denegación definitiva. La Activity registra su lanzador al crearse y lo libera al
destruirse; las solicitudes se serializan. La pantalla refresca al volver de Ajustes.
En Android anterior a 13 se consulta la habilitación global de las notificaciones.

La aplicación explica el propósito antes de solicitar. Al conceder se ofrece una
notificación local de prueba; al denegar definitivamente se ofrece abrir Ajustes.
iOS utiliza UserNotifications y los ajustes de la app. Las notificaciones locales
no necesitan una descripción de cámara/ubicación en Info.plist porque no se utilizan
esas capacidades. FCM y el envío de notificaciones remotas no están implementados.

## Firebase

Se añadió GitLive Crashlytics 2.7.0 detrás de Telemetria del dominio. Las referencias
al SDK están únicamente en data/firebase. Koin proporciona la implementación y
el repositorio registra categorías de sincronización. No se transmiten nombres de
productos, usuarios, mensajes de errores remotos ni tokens. registrarEvento usa
los logs de Crashlytics, no Firebase Analytics.

Falta la configuración de la cuenta Firebase, que no existe en el repositorio:

1. En Firebase registrar Android con paquete pe.edu.upeu.pharmamobile.
2. Descargar google-services.json y ponerlo en androidApp/google-services.json.
3. Sincronizar Gradle. Los plugins Google Services y Crashlytics se aplican solo
   cuando existe ese archivo. Antes de ello las llamadas están protegidas y no
   confirman recepción de telemetría.
4. Ejecutar en dispositivo con red y verificar un informe en la consola. No basta
   con que compile: la entrega remota debe comprobarse con el proyecto real.
5. Para iOS añadir la configuración GoogleService-Info.plist y enlazar Firebase
   en el proyecto Xcode siguiendo GitLive; sin ello no hay telemetría remota iOS.

## Revisión de huecos

Esta tabla procede de revisión del código. Completar con el recorrido real y las
capturas antes de presentarla como prueba de uso.

| Momento | Hallazgo | Gravedad | Decisión |
|---|---|---|---|
| Primera apertura | Requiere primer login con red y explica ausencia de datos | Media | Conservar, verificar manualmente |
| Login incorrecto | Existe traducción de credenciales inválidas y falta de red | Media | Verificar ambos casos |
| Lista vacía | Tiene texto informativo y Nunca sincronizado | Baja | Conservar |
| Alta sin red | Faltaba memoria del intento y error | Alta | Resuelto con migración 2 |
| Reconexión | POST repetido puede duplicar por respuesta perdida | Alta | Reenvío explícito informado; idempotencia backend pendiente |
| Validación remota de alta | El alta local conserva pendiente; faltaba mostrar el motivo | Alta | Error por fila y edición del pendiente |
| Token durante formulario | El 401 descarta contenido protegido y puede perder borrador | Media | Sesión 14, persistir borrador por usuario |
| Cambio de usuario | El catálogo local es compartido entre sesiones | Alta | Sesión 14, definir separación por usuario/tenant antes de datos privados |
| Permisos | No había gestor nativo común | Media | Implementado notificaciones; verificar estados |
| Firebase | No existe configuración del proyecto | Media | Preparado; pendiente archivo y consola de la cuenta |

## Cómo probar

1. Ejecutar `.\\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug`.
2. Abrir Productos, solicitar notificaciones, denegar y capturar Denegado.
3. Volver a solicitar y denegar hasta que Android deje de mostrar el diálogo.
   Capturar Denegado para siempre y comprobar Abrir Ajustes.
4. Habilitar desde Ajustes, volver y capturar Concedido; pulsar Probar notificación.
5. Crear sin red: comprobar pendiente, intentos y mensaje de error. Pulsar
   Sincronizar para reintentar; las esperas usan corutinas, no bloquean la interfaz.
6. Provocar 409 con nombre duplicado: la fila debe ser fallida y seguir visible.
   Sincronizar otra vez no envía esa fila; corregirla o confirmar su reenvío.
7. Con cinco fallos transitorios explícitos debe agotarse. Comprobar contadores.
8. Recuperar conexión y verificar IDs reales en Swagger. Revisar posibles altas
   ya aceptadas antes de confirmar un reenvío incierto.
9. Verificar telemetría real solo después de añadir la configuración Firebase.

## Git

No se han creado commits ni cambiado de rama porque el árbol contiene trabajo
previo de la actividad 11 todavía sin guardar. La guía pide feature/integrador-13
desde develop: primero conservar/publicar S11 e integrar su base en develop;
luego crear la rama de S13 con sus cambios. No simular commits distribuidos.
''',encoding='utf-8')
