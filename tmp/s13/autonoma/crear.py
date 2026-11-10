from pathlib import Path
base=Path('tmp/s13/informe/crear_documento.py').read_text(encoding='utf-8-sig')
exec(base.split("p('Proyecto integrador y evidencias")[0])
sec.page_width=Cm(21.59);sec.page_height=Cm(27.94)
D.core_properties.author='Tania Antonella Baldeon Ramirez'
D.core_properties.title='Actividad autónoma 13 Evidencias de PharmaMobil'
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:D.styles[name].font.name='Times New Roman'
D.styles['Normal'].font.size=Pt(11)
def imagen(path,width=7.2):
 q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture(str(path),width=Cm(width))
def espacio(text):
 p('CAPTURA PENDIENTE: '+text,'Caption');p()
def flujo(n,t,acciones,estado,archivo=None):
 sub(f'{n} {t}');p(acciones);p('Estado que se debe comprobar: '+estado)
 if archivo:imagen(archivo,5.2);p('Evidencia previa del proyecto. Repetir el paso si se necesita demostrar el estado actual.','Caption')
 else:espacio(t)
p('Actividad autónoma 13\nEvidencias del flujo de PharmaMobil','Title')
p('Desarrollo de Aplicaciones Móviles','Subtitle')
imagen('tmp/s13/referencia/logo_0.png',9)
p('Universidad Peruana Unión\nFacultad de Ingeniería y Arquitectura\nEscuela Profesional de Ingeniería de Sistemas')
p('Estudiante: Tania Antonella Baldeon Ramirez\nCódigo: 202311724\nGrupo: 2\nCiclo VI · Semestre 2026-2')
p('Docente: Benjamin David Reyna Barreto\nFecha de preparación: 6 de noviembre de 2026')
p('BORRADOR DE EVIDENCIAS. Incluye capturas reales previas y espacios identificados para completar el recorrido actual. No presentar como recorrido completo mientras existan capturas pendientes.')
page();h('Índice y alcance')
table(['Parte','Página'],[('A Flujo completo pasos 1 y 2','3'),('A Flujo completo pasos 3 y 4','4'),('A Flujo completo pasos 5 y 6','5'),('A Flujo completo pasos 7 y 8','6'),('A Flujo completo pasos 9 y 10','7'),('B Evidencias por plataforma','8'),('C Bitácora de permisos','9'),('C Notificación y Firebase','10'),('D Ficha de integración','11'),('Repositorio y cierre','12')],[13,4])
p('Este documento organiza los cuatro productos de la actividad autónoma. La aplicación implementa persistencia SQLDelight, autenticación, permiso de notificaciones y Crashlytics. Se distingue la evidencia capturada previamente de las comprobaciones aún pendientes de este recorrido.')
p('La revisión de código permite explicar el almacenamiento y la sesión, pero no sustituye las diez capturas solicitadas. La notificación local y la recepción de Crashlytics se documentan como funciones diferentes.')
p('Verificación automática del 6 de noviembre: 46 pruebas aprobadas y cero fallos. APK debug generado correctamente. La nueva prueba comprueba que el HTTP 400 vuelve al formulario y que su fila fallida se conserva.')
p('Preparación del recorrido: iniciar Docker y Oracle, ejecutar PharmaSoft en el puerto 8080, instalar el APK actualizado y abrir el emulador Android. No borrar la base de uso actual: utilizar un AVD separado para demostrar una primera apertura limpia.')
page();h('A Flujo completo inicio de sesión')
flujo(1,'Primera apertura sin sesión','Abrir una instalación nueva en un emulador separado. Mostrar la pantalla de acceso antes de ingresar credenciales.','Sin token ni filas locales en esa instalación; documentar la comprobación sin revelar credenciales ni JWT.')
flujo(2,'Inicio de sesión correcto','Entrar con la cuenta de desarrollo admin. Capturar el encabezado de Productos con usuario, roles y acceso al catálogo.','Token guardado en EncryptedSharedPreferences; clave gestionada por Android Keystore. Anotar los roles y privilegios realmente devueltos.')
page();h('A Flujo completo primera sincronización y alta')
flujo(3,'Listado tras sincronizar','Pulsar Sincronizar con conexión y esperar a que termine. La pantalla actualizada muestra registros locales, confirmados y fecha UTC.','Anotar cantidad real y fecha; un resultado de cero filas es válido si el catálogo está vacío.')
flujo(4,'Crear un producto con conexión','Registrar un nombre único, precio 5.50, stock 10 y una categoría existente. Desplazarse hasta la tarjeta creada.','La tarjeta debe mostrar ID del servidor positivo y no debe tener marca pendiente. Si falla, documentar el motivo antes de continuar.')
page();h('A Flujo completo trabajo sin red')
p('La captura de esta página procede del recorrido S13 anterior; no demuestra todavía la recuperación exitosa del paso 6.','Caption')
flujo(5,'Crear en modo avión','Con sesión iniciada, activar modo avión y desactivar Wi-Fi. Registrar otro nombre único. Capturar su tarjeta y el contador.','ID local negativo, pendiente verdadero y datos conservados. La pantalla puede registrar un intento fallido.','docs/captura/s13/05_pendiente_intento.png')
sub('6 Recuperar conexión y sincronizar');p('Restaurar Wi-Fi y desactivar modo avión. Renovar la sesión si venció. Comprobar el servidor antes de reenviar y pulsar Sincronizar; si alcanzó cinco intentos, usar la confirmación explícita de reenvío.')
p('Estado que se debe comprobar: pendientes antes ___ y después ___; ID provisional ___ sustituido por ID definitivo ___. Verificar que solo exista una fila remota para ese nombre.')
espacio('Resultado de sincronización exitosa con ID definitivo')
page();h('A Flujo completo errores controlados')
flujo(7,'Validación devuelta por el servidor','Distinguir validación local de HTTP 400. Para provocar una validación remota, usar un nombre de 151 caracteres (el máximo del DTO es 150) manteniendo precio y stock válidos. Verificar el límite antes de enviar.','Registrar el código real 400 y el mensaje por campo. La corrección de esta actividad propaga ErrorApi.Validacion al formulario y conserva la fila rechazada como fallida.')
flujo(8,'Operación sin privilegios','Iniciar sesión como vendedor. Capturar que el formulario de escritura no se muestra. En una prueba REST separada intentar POST con el token de ese usuario.','La interfaz permite lectura y oculta escritura. El servicio debe responder 403; conservar evidencia del código sin mostrar el token. No confundir ocultar el botón con haber probado el rechazo HTTP.')
page();h('A Flujo completo vencimiento y cierre')
flujo(9,'Token vencido','Iniciar sesión y esperar a que venza el JWT según la configuración del backend. En el perfil dev actual la duración configurada es un minuto. Pulsar Sincronizar con conexión.','Una respuesta protegida 401 borra el token y lleva a Login con aviso de sesión vencida. Medir el plazo real; no presentar un fallo de red como expiración.')
flujo(10,'Cierre voluntario de sesión','Volver a iniciar sesión y pulsar Cerrar sesión. Capturar Login y comprobar las tablas locales por separado.','AuthRepositorioRest borra token, identidad de sesión y caché Bearer. Los productos SQLDelight se conservan; esta conducta está implementada y debe corroborarse en el recorrido.')
page();h('B Evidencias por plataforma')
table(['Aspecto','Android','iOS'],[
('Token','EncryptedSharedPreferences y Android Keystore. JWT excluido de respaldo.','Implementación Keychain en AlmacenSeguroIos; sin recorrido visual disponible.'),
('Reinstalación','La actualización con install -r conserva datos. Desinstalación y reinstalación deben probarse en un AVD aparte.','No verificado; no afirmar que Keychain se vacía al reinstalar.'),
('Permiso','Tres estados observados en las capturas S13. Recuperación desde Ajustes.','Adaptador nativo existente; diálogo y recuperación sin evidencia de ejecución.'),
('Sin red','Fila conservada y fallos por intento observados previamente. Recuperación exitosa pendiente.','Repositorio compartido; comportamiento visual no ejecutado.'),
('Notificación','Notificación local real capturada. Crashlytics recibió un error no fatal.','Sin evidencia de recepción ni notificación.'),
('Interfaz','Capturas Android disponibles.','Tipografía, barras y áreas seguras pendientes de comparación real.')],[3,7,7])
sub('Estado real de iOS al 6 de noviembre de 2026')
p('El repositorio contiene iosMain y un objetivo iOS. Esta estación usa Windows, por lo que no permite ejecutar Xcode ni el simulador iOS. No se atribuye un error de compilación de código no observado ni se presenta esta limitación como una exoneración del docente.')
p('Plan: trasladar el mismo commit a macOS con Xcode, compilar el objetivo de iosApp, ejecutar los diez pasos y añadir capturas y diferencias. Hasta entonces la evidencia iOS permanece incompleta y debe comunicarse al docente.')
page();h('C Bitácora de notificaciones')
table(['Estado','Qué ve el usuario','Recuperación'],[
('Denegado','Explicación del propósito y botón Permitir notificaciones.','Volver a solicitar si Android permite mostrar el diálogo.'),
('Denegado para siempre','Estado definitivo y botón Abrir Ajustes.','Ajustes de la aplicación > Notificaciones > permitir; volver a PharmaMobil.'),
('Concedido','Botón Probar notificación disponible.','La función ya está disponible; si se revoca, habilitar desde Ajustes.')],[3.8,6.8,6.4])
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
for name in ['01_permiso_denegado','02_permiso_permanente','03_permiso_concedido']:
 q.add_run().add_picture('docs/captura/s13/'+name+'.png',width=Cm(5.2));q.add_run(' ')
p('Figuras 1 a 3. Capturas reales previas de PharmaMobil: denegado, denegado definitivamente y concedido. La captura del diálogo del sistema y el número de solicitudes deben registrarse al repetir el ensayo.','Caption')
p('POST_NOTIFICATIONS exige consentimiento en Android 13 o superior. INTERNET es un permiso normal declarado en el manifiesto y no tiene un diálogo de concesión en tiempo de ejecución; no se inventan tres estados para ese permiso.')
page();h('C Notificación local y Firebase')
imagen('docs/captura/s13/04_notificacion_real.png',4.3)
p('Figura 4. Notificación local real emitida mediante Probar notificación con el permiso concedido. No es un mensaje FCM.','Caption')
imagen('docs/captura/s13/09_firebase_pila.png',14)
p('Figura 5. Firebase Crashlytics recibió S13_ERROR_CONTROLADO_NO_FATAL. La consola muestra la pila de PruebaCrashlytics.registrar y MainActivity.onCreate. El error es recuperable y no cierra la aplicación.','Caption')
p('Con el permiso denegado, la interfaz orienta a solicitarlo o a Ajustes. La telemetría de Crashlytics no depende del permiso de notificaciones. Esta entrega no implementa Firebase Cloud Messaging.')
page();h('D Ficha de integración')
table(['Hueco','Gravedad','Decisión','Fecha o plazo'],[
('Memoria de intentos y error por fila','Alta','Cerrado en la práctica S13','03/11/2026'),
('Máximo de cinco intentos y fila fallida visible','Alta','Cerrado en la práctica S13','03/11/2026'),
('Permiso y salida a Ajustes','Media','Cerrado con evidencia Android','03/11/2026'),
('Recepción externa de Crashlytics','Media','Cerrado con consola aportada','04/11/2026'),
('Validación 400 no retornaba al formulario','Alta','Corregido; repetir recorrido real','06/11/2026'),
('IDs, cantidad de filas y roles poco visibles','Media','Añadidos a la interfaz; capturar APK nuevo','06/11/2026'),
('POST sin idempotencia','Alta','Sesión 14; definir clave y contrato backend','10/11/2026 previsto'),
('Catálogo compartido entre sesiones','Alta','Sesión 14; acordar separación por usuario','10/11/2026 previsto'),
('Borrador ante un 401','Media','Sesión 14; conservar por usuario','10/11/2026 previsto'),
('Recorrido completo y reinstalación','Alta','Completar antes de entregar','09/11/2026 límite'),
('Evidencias iOS','Alta','Ejecutar en macOS o acordar alcance con docente','09/11/2026 límite'),
('Cámara y ubicación sin función actual','Baja','Descartado: no pertenecen al flujo de catálogo','06/11/2026')],[5.5,1.6,6.2,3.7])
p('Las fechas previstas expresan un plan, no una resolución ya obtenida. Los huecos de evidencia siguen abiertos hasta registrar el resultado real.')
page();h('Repositorio y cierre de la entrega')
p('Rama de PharmaMobil: https://github.com/antobaldeon/Pharmamobile/tree/feature/integrador-13')
p('Commit existente: https://github.com/antobaldeon/Pharmamobile/commit/5b3aba229bfdfb2a427f79fb4a6953884f49baf3')
p('Ese commit es la base publicada. Las modificaciones de esta actividad están en el directorio de trabajo y requieren un nuevo commit. Sustituir el enlace anterior por el commit definitivo después de probar y publicar; no atribuirle cambios posteriores.')
sub('Comprobaciones antes de subir')
for t in ['Completar las diez capturas y sus estados, especialmente la recuperación exitosa del pendiente.','Corroborar HTTP 400, 403 y 401 y ocultar Authorization en cualquier registro.','Completar o fundamentar el estado de iOS; esta estación Windows no acredita su ejecución.','Registrar reinstalación en un emulador aparte sin eliminar la base utilizada habitualmente.','Actualizar la ficha de huecos con el resultado del recorrido y el commit definitivo.','Eliminar las marcas de borrador únicamente cuando las evidencias estén completas.','Exportar en carta, comprobar 8 a 14 páginas y menos de 20 MB. Entregar hasta el lunes 9 de noviembre de 2026 a las 23:59.']:p('• '+t)
sub('Referencia')
p('Actividad Autónoma N.º 13. Documentar el flujo completo y las evidencias por plataforma. Desarrollo de Aplicaciones Móviles, Universidad Peruana Unión, semestre 2026-2.')
D.save('output/doc/Baldeon_Tania_Sesion13_Evidencias_Borrador.docx')
print('DOCX_GENERADO')
