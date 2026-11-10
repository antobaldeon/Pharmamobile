# Actividad autónoma 13 Cómo probar

Estado revisado al 10/11/2026: [los cuatro productos y pendientes](EVIDENCIAS.md) y [verificación actual](VERIFICACION.md). Hay un informe parcial actualizado en `output/pdf/Baldeon_Tania_Sesion13_Evidencias_EstadoActual.pdf`; conserva los borradores anteriores y no acredita las capturas aún pendientes.

## Preparar
1. Inicia Docker Desktop y espera a que el motor responda a `docker info`.
2. Inicia tu contenedor Oracle: `docker start oracle-local`.
3. Inicia PharmaSoft con el perfil dev y el esquema PHARMASOFT_DEV. No cambies TESTDB.
4. En PharmaMobil ejecuta `./gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug`.
5. Instala androidApp/build/outputs/apk/debug/androidApp-debug.apk en el emulador.
6. Para la primera apertura y reinstalación usa otro AVD. Conserva los datos del emulador habitual.

## Diez capturas
1. Login en una instalación limpia. Confirma base vacía y ausencia de token sin mostrar el JWT.
2. Login correcto. Captura usuario, roles y acceso de lectura/escritura.
3. Pulsa Sincronizar. Captura cantidad de registros y fecha UTC del último éxito.
4. Crea un nombre único con red (precio 5.50, stock 10 y categoría existente). Captura ID del servidor positivo.
5. Activa modo avión y desactiva Wi-Fi. Crea otro nombre único. Captura ID local negativo y pendiente.
6. Recupera conexión. Si venció la sesión, vuelve a entrar. Verifica primero que el servidor no tenga ya el registro. Sincroniza o confirma el reenvío si está fallido. Captura pendientes antes/después y nuevo ID positivo; verifica ausencia de duplicados.
7. Con admin y red, envía un nombre de 151 caracteres. El DTO admite 150; el resto de campos debe ser válido. Captura HTTP 400 en el registro KTOR y el mensaje bajo Nombre. Una validación local no prueba el HTTP 400. La fila rechazada queda fallida y no se reenvía automáticamente.
8. Entra como vendedor. Captura que el formulario de escritura no aparece. En Postman usa el token de vendedor para POST /api/v1/productos y comprueba 403. Oculta Authorization antes de capturar. No agregues privilegios al vendedor.
9. Con admin, consulta la duración vigente del JWT en el backend, espera su vencimiento y pulsa Sincronizar con red. Captura HTTP 401 y retorno a Login con aviso. No confundas el fallo de red con el vencimiento.
10. Entra de nuevo y pulsa Cerrar sesión. Captura Login. Comprueba que desaparece el token y la identidad de sesión; los productos locales permanecen.

## Permisos y plataformas
- Repite Denegado, Concedido y Denegado para siempre; documenta cuántas solicitudes mostró Android y cómo vuelves de Ajustes.
- Incluye la notificación local y la evidencia real de Crashlytics que ya están en docs/captura/s13.
- No desinstales el emulador habitual para probar reinstalación. Usa un AVD de prueba.
- El equipo Windows no ejecuta Xcode ni simulador iOS. El borrador registra esa limitación sin inventar un error del código. La guía no concede una exoneración automática.

## Documento
Abre output/doc/Baldeon_Tania_Sesion13_Evidencias_Borrador.docx. Inserta las capturas señaladas y reemplaza los estados por resultados reales. Actualiza el enlace al commit final después de probar y publicar. Exporta a Baldeon_Tania_Sesion13_Evidencias.pdf, carta, 8 a 14 páginas y menos de 20 MB. No entregues como completo un borrador con capturas pendientes.

Verificado el 6 de noviembre de 2026: 46 pruebas aprobadas y APK debug generado. La prueba nueva verifica propagación del HTTP 400 y conservación de la fila fallida.
