# Actividad autónoma 11 y guía de pruebas

## Cambios implementados

- `S11PruebasOfflineTest` incluye las seis pruebas requeridas con MockEngine de Ktor,
  el repositorio REST real y una base SQL en memoria independiente por prueba.
- La tabla `estado_sincronizacion` guarda un único instante en milisegundos Unix.
  Se actualiza junto al catálogo en la transacción de una sincronización completa.
  Un fallo de subida o descarga conserva la fecha anterior.
- Productos muestra Nunca sincronizado, hace un momento, minutos, horas o días.
  La etiqueta se actualiza cada minuto mientras la pantalla está visible.
- La migración `1.sqm` conserva los productos de la versión anterior. Una base
  antigua muestra Nunca sincronizado hasta su siguiente sincronización correcta.
- En una instalación sin datos, el login informa que no hay productos locales y
  que el primer acceso requiere conexión. No se inventa una sesión para autenticar
  sin red. Si ya existe un perfil guardado, se mantiene la restauración offline.

## Preparación

1. Ejecutar `androidApp` desde Android Studio en el emulador.
2. Encender PharmaSoft, iniciar sesión con admin y sincronizar.
3. Elegir una categoría existente y un nombre único, como Autonoma Offline 01.
4. Mantener la fecha automática normal para las pruebas de red y token.
5. Guardar las capturas y los resultados antes de borrar datos de la aplicación.

El perfil dev de PharmaSoft consultado tiene `expiracion-minutos: 1` en
`src/main/resources/application-dev.yaml`. Revisa qué perfil estás ejecutando:
los tokens emitidos antes de un cambio conservan su vencimiento original.

## Pruebas automáticas

```powershell
.\gradlew.bat :shared:testAndroidHostTest
```

Abrir `shared/build/reports/tests/testAndroidHostTest/index.html` y entrar en
`S11PruebasOfflineTest`. Los métodos prueba1 a prueba6 corresponden a los seis
requisitos. También hay una prueba del fallo de sincronización y su fecha.
Adjuntar el resultado completo de la suite, no un único método en verde.
La salida guardada de esta implementación estará en `docs/S11_AUTONOMA_PRUEBAS.txt`.

## Bitácora de los cinco escenarios

Para cada escenario registrar fecha/hora, plataforma y versión, pasos, resultado
observado, estado de SQLite, captura y una conclusión propia. Completar con lo
que ocurra al ejecutar la aplicación; los resultados esperados no sustituyen las evidencias.

### E1 Apertura sin red con datos previos

Sincronizar con red. Cerrar la aplicación desde recientes. Activar modo avión y
comprobar que Wi-Fi no se reactive. Apagar PharmaSoft también evita que el acceso
al host del emulador permita peticiones. Reabrir: deben permanecer los productos,
la fecha anterior y el aviso de falta de conexión. Esperar el timeout si es necesario.
Capturar el listado y el icono de modo avión; registrar cuántas filas hay en SQLite.

### E2 Registro sin red

Sin salir del modo avión, registrar Autonoma Offline 01 con precio 5.50, stock 10
y categoría válida. Debe aparecer con Pendiente de sincronización. En SQLite debe
haber un ID negativo y pendiente igual a 1. Cerrar y reabrir para verificar persistencia.
Capturar la tarjeta y, adicionalmente, el registro en Database Inspector.

### E3 Reconexión y envío

Encender PharmaSoft, desactivar modo avión y pulsar Sincronizar. Si el token
venció durante la desconexión, la respuesta 401 lleva al login; iniciar sesión de
nuevo y volver a sincronizar. Los productos locales no se eliminan por ese 401.
Comprobar en Swagger el nombre y el ID positivo del producto. En SQLite no debe
quedar su ID negativo. Sincronizar otra vez: no debe enviarse otra alta confirmada.
Tomar captura de la app y de la respuesta de Swagger.

### E5 Sesión expirada sin red

Se realiza antes de borrar datos. Iniciar sesión de nuevo y sincronizar. Activar
modo avión y apagar el backend. Esperar más que la vigencia del token (por ejemplo,
90 segundos si dev realmente usa un minuto). Cerrar y abrir la app. Debe restaurar
el perfil guardado y mostrar los datos locales; sin red no se obtiene validación
remota de la sesión. Anotar lo observado. Al recuperar red y sincronizar, el 401
limpia perfil/token y pide login. Tras autenticar de nuevo, se retoma la sincronización.
Capturar la consulta local offline y la resolución de la sesión al reconectar.
Conclusión a desarrollar: mostrar información local evita un login imposible sin
red; la autorización de escrituras sigue dependiendo del servidor al reconectar.

### E4 Primera apertura sin red

Hacer al final: borrar datos elimina productos, pendientes, token y fecha guardada.
Usar Ajustes > Aplicaciones > PharmaMobil > Almacenamiento > Borrar almacenamiento.
Activar modo avión y abrir. Debe aparecer el login con No hay productos guardados
en este dispositivo y Nunca sincronizado, sin una pantalla de error. No es posible
crear la primera sesión autenticada sin servidor. Esta es la decisión de diseño
que debe explicarse en la bitácora. Capturar el mensaje y comprobar tabla vacía.

## Comprobar la base local

En Android Studio, con la app debug abierta: View > Tool Windows > App Inspection >
Database Inspector. Seleccionar PharmaMobil y `pharma.db`. Ejecutar:

```sql
SELECT id, nombre, pendiente FROM producto ORDER BY id;
SELECT * FROM estado_sincronizacion;
```

La primera consulta evidencia altas negativas y confirmaciones positivas. La segunda
permite verificar que la fecha no cambia cuando falla la red. Después de borrar datos
las tablas existen al abrir la app, pero no tienen filas de productos ni de sincronización.

## Evidencias de antigüedad

- Nunca sincronizado: capturar E4 antes del primer login/sincronización.
- Reciente: con fecha automática correcta, iniciar sesión, sincronizar y capturar
  Actualizado hace un momento.
- Más de un día: conservar una sincronización real, dejar pasar más de 24 horas
  sin sincronizar y capturar la etiqueta offline.
- Para ensayar sin esperar, puedes adelantar temporalmente dos días el reloj del
  emulador desde Ajustes > Sistema > Fecha y hora, desactivando fecha automática.
  Hacerlo con backend apagado y sin sincronizar. Cerrar y abrir, capturar y declarar
  en la bitácora que se simuló el paso del tiempo. Restaurar la fecha automática
  ANTES de reconectar o iniciar sesión. No presentar una simulación como tiempo real.

No se agrega un botón de datos simulados al producto ni se altera una fecha exitosa
para aparentar una sincronización que no ocurrió.

## Registro de bitácora para completar

Repetir este bloque para E1, E2, E3, E4 y E5:

- Identificador y nombre:
- Fecha y hora:
- Plataforma y versión:
- Pasos exactos:
- Resultado observado en pantalla:
- Estado de la base local y consulta usada:
- Ruta o nombre de las capturas:
- Conclusión propia:

## Entrega

Preparar el PDF S11_ActividadAutonoma_Baldeon.pdf con portada, enlace a la rama,
las pruebas y su salida completa, los cinco registros de bitácora, las evidencias
de antigüedad y el guion de ocho minutos en S11_GUION_SUSTENTACION.md.
Publicar commits nuevos en feature/offline-first-baldeon. Fecha de entrega de la
actividad: 26 de octubre de 2026, 23:59. Sustentación: 27 de octubre de 2026.
