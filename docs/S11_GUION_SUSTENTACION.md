# Guion de sustentación del Producto U2

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
