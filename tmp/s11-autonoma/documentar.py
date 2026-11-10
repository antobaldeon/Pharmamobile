from pathlib import Path
p=Path('shared/build.gradle.kts');s=p.read_text(encoding='utf-8').replace('    testLogging {\n        showStandardStreams','    testLogging {\n        events("passed", "skipped", "failed")\n        showStandardStreams');p.write_text(s,encoding='utf-8')
p=Path('docs/S11_AUTONOMA_COMO_PROBAR.md')
p.write_text('''# Actividad autónoma 11 y guía de pruebas

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
.\\gradlew.bat :shared:testAndroidHostTest
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
''',encoding='utf-8')
p=Path('docs/S11_GUION_SUSTENTACION.md')
p.write_text('''# Guion de sustentación del Producto U2

Duración: ocho minutos. Fecha: 27 de octubre de 2026.

## Preparación previa

- PharmaSoft y su base deben estar encendidos con migraciones aplicadas.
- Tener categoría válida, catálogo con datos y un producto prescindible para eliminar.
- Preparar admin para escritura y vendedor para demostrar falta de permiso.
- Comprobar la vigencia del JWT: el perfil dev consultado expira tokens en un minuto.
  Si se utiliza otra duración en el ensayo, emitir un token nuevo y anotar la configuración.
- Dejar la app sin sesión al inicio, pero haber cargado previamente datos locales.
- Abrir Swagger y tener preparada una petición protegida de escritura con vendedor.
- Tener Android e iOS listos. Si se usan evidencias grabadas por disponibilidad de
  equipos, acordarlo previamente con el docente; una compilación no sustituye ejecución.
- Ensayar con cronómetro y no borrar datos durante la sustentación.

| Tiempo | Usuario | Acción y explicación |
|---|---|---|
| 0:00–1:00 | admin | Intentar contraseña incorrecta, mostrar error y luego iniciar sesión correctamente. Explicar JWT y almacenamiento seguro sin mostrar el token. |
| 1:00–3:00 | admin | Listar, crear un producto con categoría válida, actualizarlo y eliminar el producto de prueba. Mostrar la petición o respuesta REST y explicar que la pantalla observa SQLite. |
| 3:00–5:00 | vendedor y admin | Con vendedor, mostrar que no se ofrecen acciones de escritura. En Swagger ejecutar un POST válido de productos con su token y evidenciar 403. Volver a admin y editar un producto del servidor con nombre de dos caracteres para provocar la validación del backend bajo el campo. Restaurar el valor válido. |
| 5:00–7:00 | admin | Activar modo avión y garantizar falta de acceso al backend. Mostrar catálogo y antigüedad; registrar un producto y su marca pendiente. Recuperar red, sincronizar y verificar en Swagger el ID positivo. Si hay 401, renovar sesión y continuar; los pendientes se conservan. |
| 7:00–8:00 | usuario autorizado | Mostrar la misma consulta offline en iOS y Android y explicar drivers por plataforma, esquema compartido y las pruebas comunes. |

## Frases para explicar el código

- La pantalla lee SQLite; una respuesta HTTP se guarda antes de reflejarse en el listado.
- El ID negativo identifica una creación local; pendiente indica que aún falta confirmación.
- Se sube antes de descargar para no perder el trabajo offline.
- Cada alta confirmada reemplaza el ID temporal en una transacción.
- La fecha solo cambia después de una sincronización completa correcta y persiste al cerrar.
- MockEngine sustituye el transporte HTTP; se prueban los DTO, el mapeo, la paginación
  y el repositorio real con SQL en memoria sin emulador ni red.

## Resultado del ensayo para completar

Fecha/hora: ____________________
Duración medida: _______________
Incidencias y correcciones: ______________________________________________
''',encoding='utf-8')
