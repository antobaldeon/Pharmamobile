from pathlib import Path
# Reuse the document building primitives, without rewriting the previous deliverable.
base=Path('tmp/s13/informe/crear_documento.py').read_text(encoding='utf-8-sig')
exec(base.split("p('Proyecto integrador y evidencias")[0])
from docx.enum.section import WD_SECTION
sec.left_margin=sec.right_margin=Cm(2.25)
for n in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 D.styles[n].font.name='Times New Roman'
D.styles['Normal'].font.size=Pt(11)
D.styles['Normal'].paragraph_format.line_spacing=1.05
D.styles['Heading 1'].font.size=Pt(16)
D.styles['Heading 2'].font.size=Pt(12)
D.styles['Title'].font.size=Pt(17)
D.core_properties.title='Informe de práctica de laboratorio 13 PharmaMobil Android'
D.sections[0].different_first_page_header_footer=True
# Cover mirroring the supplied university report.
def center(text,size=12,bold=False,after=9):
 q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.space_after=Pt(after)
 r=q.add_run(text);r.bold=bold;r.font.size=Pt(size)
center('UNIVERSIDAD PERUANA UNIÓN',18,True,14)
center('FACULTAD DE INGENIERÍA Y ARQUITECTURA',12,False,4)
center('Escuela Profesional de Ingeniería de Sistemas',12,False,24)
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture('tmp/s13/referencia/logo_0.png',width=Cm(9))
p();p()
center('INFORME DE PRÁCTICA DE LABORATORIO N.º 13',12,True,18)
q=D.add_paragraph('Proyecto integrador sincronización robusta permisos y Firebase','Title');q.alignment=WD_ALIGN_PARAGRAPH.CENTER
center('Proyecto PharmaMobil sobre PharmaSoft',12,False,24)
center('Asignatura',12,True,3);center('Desarrollo de Aplicaciones Móviles',12,False,16)
center('Autor',12,True,3);center('____________________________ Baldeón',12,False,16)
center('Docente',12,True,3);center('Mg. Reyna Barreto Benjamin David',12,False,22)
center('Ciclo VI · Semestre 2026-2',12,False,3)
center('3 de noviembre de 2026',12,False,3);center('Perú',12)
contentsec=D.add_section(WD_SECTION.NEW_PAGE);contentsec.different_first_page_header_footer=False
contentsec.header.is_linked_to_previous=False;contentsec.footer.is_linked_to_previous=False
header=contentsec.header.paragraphs[0];header.text='UNIVERSIDAD PERUANA UNIÓN                                      Ingeniería de Sistemas'
for r in header.runs:r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string('666666')
footer=contentsec.footer.paragraphs[0];footer.text='Baldeón | Desarrollo de Aplicaciones Móviles                                      '
for r in footer.runs:r.font.size=Pt(8)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
num=OxmlElement('w:pgNumType');num.set(qn('w:start'),'1');contentsec._sectPr.append(num)
# 2
h('Presentación e índice')
p('Informe académico de la actividad práctica de la sesión 13','Caption')
p('Introducción. Este informe documenta el refinamiento de PharmaMobil sobre PharmaSoft: memoria de intentos y errores por fila, distinción de fallos transitorios y permanentes, estado observable de sincronización y permiso de notificaciones en Android. La telemetría se integra detrás de una interfaz del dominio y se verifica en Firebase Crashlytics.')
p('Objetivo. Evitar que una creación offline desaparezca sin explicación, hacer visibles los pendientes y las fallidas, y ofrecer una salida cuando el permiso es denegado definitivamente.')
contents=[('1 Desarrollo de la práctica','2'),('2 Paso 1 Tabla de huecos','3'),('3 Pasos 2 y 3 Esquema y sincronización','4'),('4 Evidencias Permiso de notificaciones','5'),('5 Evidencias Denegación definitiva y concesión','6'),('6 Evidencias Estado de sincronización','7'),('7 Evidencias Fila fallida y notificación','8'),('8 Comprobación en PharmaSoft y SQLite','9'),('9 Pruebas y resultados','10'),('10 Salida real de las pruebas','11'),('11 Firebase y desviaciones','12'),('12 Guion de sustentación','13'),('13 Lista de cotejo y referencias','14')]
table(['Contenido','Página'],contents,[14.2,2.3])
p('Conclusiones de la ejecución. La suite Android registra 45 pruebas aprobadas y cero fallos. En el emulador se observaron los tres estados del permiso, una notificación local y el paso de una fila pendiente a fallida al agotar cinco intentos. SQLite conservó la fila con ID negativo, pendiente igual a 1 e intentos igual a 5.')
p('Alcance: evidencias y demostración exclusivamente Android. No se incluyen pruebas de ejecución iOS.')
#3
page();h('1 Desarrollo de la práctica')
p('Guía práctica de laboratorio 13 | Unidad 3 | PharmaMobil Android','Caption')
p('Se integran la persistencia local y la autenticación existentes con la gestión de errores por fila y un permiso nativo. La pantalla sigue observando la base mediante Flow y no depende de recargas de la lista después de cada escritura.')
p('Rama actual: feature/offline-first-baldeon. Rama solicitada por la guía: feature/integrador-13, pendiente de preparar y publicar. Repositorio: github.com/antobaldeon/Pharmamobile.')
table(['Paso solicitado','Implementación real'],[
('1 Recorrido y huecos','Revisión del flujo y tabla de hallazgos con gravedad y decisión.'),
('2 Esquema','Producto.sq con intentos y ultimoError; migración 2.sqm a versión 3.'),
('3 Sincronización','Clasificación de errores, cinco intentos y espera creciente; reenvío explícito de altas no idempotentes.'),
('4 Estado en la interfaz','Pendientes, fallidas, antigüedad, motivo, intentos y acción para confirmar reenvío.'),
('5 Permisos','GestorPermisos común, lanzador Android en MainActivity y declaración POST_NOTIFICATIONS.'),
('6 Firebase','GitLive Crashlytics 2.7.0 mediante Telemetria. Configuración Android activa y evento no fatal recibido en consola.'),
('7 Pruebas','MockEngine, SQLite en memoria y gestor falso; siete casos nuevos de S13.')
],[4.0,12.5])
sub('Flujo de sincronización')
p('Pendientes elegibles → envío por fila → confirmación con ID positivo o registro de error → si no hubo fallo en la ronda, descarga del catálogo → conciliación local y marca de última sincronización. Las filas ya fallidas permanecen almacenadas y no se reenvían automáticamente.')
sub('Estado del repositorio')
p('Último commit disponible al preparar el informe: b660000. Los cambios de S13 aún están sin publicar. No se atribuyen commits distribuidos que no se hayan realizado. La revisión de la base del trabajo debe conservar primero los cambios previos de la sesión 11.')
#4
page();h('2 Paso 1 Tabla de huecos')
p('Se distingue la observación de Android de los hallazgos de revisión de código. Las decisiones pendientes se mantienen explícitas.','Caption')
table(['N.º','Hueco o hallazgo','Sev.','Decisión'],[
('1','Faltaba memoria del error por producto pendiente.','Alta','Resuelto: intentos y ultimoError.'),
('2','No se distinguía rechazo permanente de fallo transitorio.','Alta','Resuelto: clasificador en datos.'),
('3','Faltaba límite visible de envíos fallidos.','Alta','Resuelto: máximo cinco intentos.'),
('4','La pantalla no mostraba contador de fallidas ni motivo por fila.','Alta','Resuelto y capturado.'),
('5','No existía gestor común del permiso de notificaciones.','Media','Resuelto: interfaz y Android real.'),
('6','La denegación definitiva necesita una salida.','Media','Resuelto: Abrir Ajustes y refresco al volver.'),
('7','Un POST aceptado cuya respuesta se pierde puede duplicarse.','Alta','Reenvío explícito informado; idempotencia para sesión 14.'),
('8','El 401 a mitad del formulario puede descartar el borrador.','Media','Sesión 14: conservar borrador por usuario.'),
('9','El catálogo local es compartido entre sesiones.','Alta','Sesión 14: definir separación por usuario o tenant.'),
('10','La integración Firebase necesitaba validación externa.','Media','Resuelto: configuración Android y evento recibido en Crashlytics.'),
('11','TESTDB mezclaba historial Flyway de otro proyecto.','Alta','Resuelto: esquema PHARMASOFT_DEV aislado.'),
('12','Cámara o ubicación no tienen una función en esta entrega.','Baja','Descartado para esta práctica; se usa notificaciones.')
],[0.8,8.0,1.5,6.2])
p('Se verificó el acceso al formulario de login después de una sesión vencida. El primer acceso correcto descargó el catálogo vacío del esquema nuevo. El estado de antigüedad y los contadores se actualizaron desde la base local.')
#5
page();h('3 Pasos 2 y 3 Esquema y sincronización')
p('SQLDelight 2.1.0 | ProductoRepositorioOffline en commonMain','Caption')
sub('Migración sin pérdida de datos')
p('La actividad 11 ya usa 1.sqm para guardar la última sincronización. Por eso las nuevas columnas se incorporan en 2.sqm y la base pasa a versión 3.')
for line in ['ALTER TABLE producto ADD COLUMN intentos INTEGER NOT NULL DEFAULT 0;','ALTER TABLE producto ADD COLUMN ultimoError TEXT;']:
 r=p(line).runs[0];r.font.name='Consolas';r.font.size=Pt(9)
sub('Traducción de errores en la capa de datos')
table(['ErrorApi','Clasificación','Efecto'],[
('SinConexion, TiempoAgotado, Servidor','Transitorio','Suma un intento y conserva la fila. Al quinto fallo se agota.'),
('Validacion, Conflicto, NoEncontrado, SinPermiso','Permanente','Se asignan cinco intentos y el motivo para mostrarla como fallida.'),
('SesionExpirada','Permanente','Se conserva el producto. La autenticación debe renovarse antes de reenviar.')
],[6.5,3.0,7.0])
sub('Espera y reintento explícito')
p('esperaEnvio(i) = 1000L shl (i - 1).coerceIn(0, 4).toInt(). La función produce 1, 2, 4, 8 y 16 segundos y no supera 16 segundos. Las esperas se verifican con tiempo virtual en las pruebas.')
p('No se ejecuta un bucle automático de POST. Registrar otro producto tampoco reenvía automáticamente las filas que ya fallaron. Sincronizar autoriza una nueva ronda de transitorios; las fallidas requieren una confirmación de reenvío o una corrección del contenido.')
p('Los productos confirmados reemplazan el ID negativo por el ID del servidor. Se sube antes de descargar; la descarga conserva las filas pendientes. Si hubo un fallo en la ronda, se comunica el error y no se actualiza una falsa fecha de sincronización correcta.')
#6
page();h('4 Evidencias Permiso de notificaciones')
p('Estado inicial Denegado y explicación previa al diálogo del sistema','Caption')
p('Se abrió la aplicación con admin y se verificó que la tarjeta explicara el propósito. El botón Permitir notificaciones abrió la solicitud real de Android. Se denegó dos veces para obtener la denegación definitiva.')
pic('01_permiso_denegado',17)
p('Figura 1. Captura Android real. El permiso aún no concedido se muestra como Denegado y la tarjeta ofrece solicitarlo.','Caption')
#7
page();h('5 Evidencias Denegación definitiva y concesión')
p('Recuperación del permiso desde Ajustes y actualización al volver','Caption')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture('docs/captura/s13/02_permiso_permanente.png',width=Cm(7.4));q.add_run('   ');q.add_run().add_picture('docs/captura/s13/03_permiso_concedido.png',width=Cm(7.4))
p('Figura 2. Tras la segunda negativa, Denegado para siempre y Abrir Ajustes. Figura 3. Habilitado en Ajustes, la pantalla muestra Concedido y Probar notificación.','Caption')
p('Resultado: Android diferencia los tres estados. La consulta al volver de Ajustes actualiza la tarjeta sin reinstalar la aplicación. No se solicitó cámara ni ubicación.')
#8
page();h('6 Evidencias Estado de sincronización')
p('Antigüedad, contador de pendientes y motivo del primer fallo','Caption')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture('docs/captura/s13/03_permiso_concedido.png',width=Cm(7.4));q.add_run('   ');q.add_run().add_picture('docs/captura/s13/05_pendiente_intento.png',width=Cm(7.4))
p('Figura 4. Después de sincronizar: cero pendientes y cero fallidas. Figura 5. En modo avión: una creación local pendiente, error de conexión e Intentos 1/5.','Caption')
p('Se registró EvidenciaS13Android con precio 5.50, stock 10 y categoría 1 mientras el emulador estaba sin conexión. La operación local se conservó pese al fallo del envío.')
p('La pantalla advierte que un envío sin respuesta puede haberse registrado en el servidor y pide verificar antes de reenviar. La antigüedad no se reinicia por un intento fallido.')
#9
page();h('7 Evidencias Fila fallida y notificación')
p('Agotamiento de cinco intentos y capacidad nativa Android','Caption')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture('docs/captura/s13/06_fila_fallida_cinco_intentos.png',width=Cm(7.4));q.add_run('   ');q.add_run().add_picture('docs/captura/s13/04_notificacion_real.png',width=Cm(7.4))
p('Figura 6. Cuatro reintentos explícitos adicionales dejaron la fila en Intentos 5/5 y el contador en una fallida. Figura 7. Notificación local real de PharmaMobil.','Caption')
p('La notificación de esta implementación se generó con Probar notificación. No se afirma que el agotamiento la dispare automáticamente. El rechazo 409 se verifica con MockEngine en la suite; no se presenta una captura manual de 409 que no se haya obtenido.')
p('Al finalizar se restauró la conexión original. La creación de prueba permanece local como fallida; no se confirmó su reenvío al backend.')
#10
page();h('8 Comprobación en PharmaSoft y SQLite')
p('Separación del esquema remoto y comprobación de la fila local','Caption')
p('PharmaSoft se conectaba al usuario TESTDB, cuyo historial registraba una migración fallida ajena al proyecto. Se creó PHARMASOFT_DEV en Oracle FREEPDB1 y se configuró el perfil dev para usarlo. Se conservaron las tablas y el historial de TESTDB.')
table(['Esquema','Resultado comprobado'],[
('TESTDB','22 tablas antes de separar; la migración fallida add labor registration timestamp se conserva sin reparar ni borrar.'),
('PHARMASOFT_DEV','Migraciones V1 esquema inicial, V2 seguridad empleados usuarios y V3 datos iniciales seguridad aplicadas correctamente.'),
('REST de PharmaSoft','Login admin correcto y GET /api/v1/productos con HTTP 200 durante la validación del esquema nuevo.'),
('Catálogo remoto nuevo','Sin productos al completar la separación; no se copiaron registros del otro esquema.')
],[4.0,12.5])
sub('Consulta real de la base del emulador')
r=p('SELECT id, nombre, pendiente, intentos, ultimoError FROM producto;').runs[0];r.font.name='Consolas';r.font.size=Pt(9)
table(['Campo','Valor observado'],[['id','-1'],['nombre','EvidenciaS13Android'],['pendiente','1'],['intentos','5'],['ultimoError','No se pudo conectar con el servidor']],[4,12.5])
p('Resultado: la fila local no se perdió al agotar el límite. La comprobación documentada no demuestra un alta confirmada en el servidor: el producto de esta ronda sigue sin enviar.')
#11
page();h('9 Pruebas y resultados')
p('commonTest con MockEngine y SQLDelight en memoria','Caption')
table(['Caso S13','Resultado comprobado'],[
('Estados de permiso','Primera solicitud, denegación temporal, definitiva y concesión se distinguen.'),
('Gestor falso','Se consulta, solicita y abre Ajustes sin depender de un dispositivo.'),
('Espera creciente','La función devuelve 1000, 2000, 4000, 8000 y 16000 ms; el límite es 16000.'),
('Clasificación','Sin conexión y timeout son transitorios; conflicto y sesión expirada son permanentes.'),
('503 transitorio','Un intento de alta incrementa el contador una vez; no crea un bucle de POST.'),
('409 permanente','La fila queda fallida y una sincronización posterior no vuelve a enviar ese POST.'),
('Cinco transitorios','La fila conserva sus datos, alcanza cinco intentos y deja de enviarse en rondas ordinarias.')
],[4.5,12.0])
sub('Regresión de las sesiones anteriores')
p('Las pruebas S11 siguen verificando subida antes de descarga, Flow con la lista completa, alta sin red, preservación de pendientes, separación de IDs y ausencia de duplicación en sincronizaciones confirmadas. También se prueba la persistencia de la fecha correcta y la migración desde la versión 1 hasta la versión actual.')
p('En esta entrega no se añadió una clase de instrumentación Android. Las capturas se obtuvieron mediante un recorrido real del emulador y las pruebas automáticas corresponden al destino Android Host.')
p('Comando de verificación: .\\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug.')
p('Reporte generado por Gradle: shared/build/reports/tests/testAndroidHostTest/index.html. Los resultados se comprobaron en los XML JUnit de shared/build/test-results.')
#12
page();h('10 Salida real de las pruebas')
p('Resumen leído de los XML JUnit y extracto del registro Gradle','Caption')
results=[];total=0
for f in sorted(Path('shared/build/test-results').rglob('TEST-*.xml')):
 r=E.parse(f).getroot();total+=int(r.attrib['tests']);results.append([r.attrib['name'].split('.')[-1],r.attrib['tests'],r.attrib['failures'],r.attrib.get('time','')])
table(['Clase','Pruebas','Fallos','Tiempo s'],results,[9.5,2.1,2.1,2.8])
p(f'Total JUnit verificado: {total} pruebas, 0 fallos y 0 errores.')
for line in ['> Task :shared:testAndroidHostTest UP-TO-DATE','> Task :androidApp:assembleDebug','BUILD SUCCESSFUL in 7s','71 actionable tasks: 4 executed, 5 from cache, 62 up-to-date']:
 r=p(line).runs[0];r.font.name='Consolas';r.font.size=Pt(9)
p('La verificación más reciente reutilizó los resultados vigentes de pruebas. El APK se generó e instaló conservando los datos; se verificaron login y navegación hasta Productos. No se atribuyen 85 pruebas ni instrumentación al proyecto: esos resultados pertenecen al ejemplo de referencia.')
#13
page();h('11 Firebase y desviaciones')
p('Crashlytics verificado en el proyecto pharmamobile','Caption')
p('La configuración Android google-services.json está instalada. Las capturas aportadas de Firebase Console confirman S13_ERROR_CONTROLADO_NO_FATAL: un evento recuperable y un usuario afectado, versión 1.0 (1). La prueba registró una IllegalStateException sin cerrar la aplicación.')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture('docs/captura/s13/08_firebase_detalle.png',width=Cm(12.8))
p('Figura 8. Firebase Console confirma la recepción del error controlado no fatal.','Caption')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture('docs/captura/s13/09_firebase_pila.png',width=Cm(13.8))
p('Figura 9. Seguimiento de pila: PruebaCrashlytics.registrar y MainActivity.onCreate.','Caption')
p('TelemetriaFirebase aísla el SDK en datos. La prueba explícita solo se activa en una compilación depurable. Se utiliza Crashlytics; no se implementó FCM. Se mantienen la migración 2.sqm, el reintento explícito y la notificación local manual. El informe cubre Android. La publicación de la rama S13 sigue pendiente.')
#14
page();h('12 Guion de sustentación')
p('Demostración propuesta en Android | Duración ocho minutos','Caption')
table(['Tiempo','Demostración y explicación'],[
('0:00 a 0:45','Presentar PharmaMobil, el alcance Android, el estado del repositorio y la tabla de huecos.'),
('0:45 a 2:00','Mostrar Producto.sq y 2.sqm; explicar por qué la migración conserva productos y la fecha anterior.'),
('2:00 a 3:30','Explicar clasificación de errores, límite de cinco intentos, espera creciente y subida antes de descarga.'),
('3:30 a 4:30','Mostrar permiso inicial, denegación definitiva, Ajustes, concesión y notificación local de prueba.'),
('4:30 a 6:00','Mostrar modo avión, alta pendiente y error por fila; recorrer reintentos explícitos o sus capturas reales.'),
('6:00 a 7:00','Mostrar la fila agotada, el contador de fallidas y su persistencia en SQLite. Explicar la confirmación de reenvío.'),
('7:00 a 8:00','Presentar pruebas con MockEngine, los 45 resultados y la recepción del error en Firebase y el límite de idempotencia.')
],[3.1,13.4])
sub('Preparación')
p('Tener Oracle y PharmaSoft encendidos, el esquema PHARMASOFT_DEV configurado, APK actualizado y emulador disponible. Usar admin para el recorrido; el token del perfil dev tiene vigencia corta, por lo que debe renovarse cuando corresponda.')
p('No borrar datos para reiniciar el ensayo sin haber conservado las evidencias. Las solicitudes de permiso pueden restaurarse desde Ajustes del emulador. Tener a mano el reporte JUnit y el producto de prueba fallido.')
sub('Conclusiones')
p('El producto creado sin red permanece en la base local y el límite de intentos no lo elimina. La interfaz comunica el problema por fila y permite una decisión explícita sobre el reenvío. Android distingue los tres estados del permiso y genera una notificación local real.')
p('La suite automatizada respalda el clasificador y la persistencia; las capturas respaldan el recorrido Android. Firebase recibió el evento no fatal de prueba. La publicación de la rama S13 y la idempotencia del backend siguen pendientes.')
#15
page();h('13 Lista de cotejo y referencias')
p('Trazabilidad de la guía y estado real de la entrega Android','Caption')
table(['N.º','Criterio','Evidencia y estado'],[
('1','Recorrido y tabla de huecos','Sección 2. Incluye hallazgos observados y de código.'),
('2','Intentos y último error por fila','Producto.sq y SQLite de la sección 8.'),
('3','Transitorio frente a permanente','ClasificarEnvio y pruebas S13.'),
('4','Espera creciente y máximo','Cinco intentos; función acotada y test virtual.'),
('5','Fila agotada visible','Figura 6 e intentos 5 en SQLite.'),
('6','Subida antes de descarga','Repositorio y pruebas de regresión S11.'),
('7','Pendientes fallidas y antigüedad','Figuras 4 a 6.'),
('8','Interfaz común de permisos','domain/permiso/GestorPermisos.kt.'),
('9','Tres estados en Android','Figuras 1 a 3; pruebas de resolución.'),
('10','Declaración del permiso','POST_NOTIFICATIONS en AndroidManifest.xml.'),
('11','Explicación y acceso a Ajustes','Figuras 1 y 2; retorno verificado.'),
('12','SDK aislado en datos','TelemetriaFirebase y evento recibido en consola; figuras 8 y 9.'),
('13','commonTest aprobado','45 pruebas sin fallos; sección 10.'),
('14','Rama y commits por paso','Pendiente feature/integrador-13 y publicación.')
],[0.8,6.0,9.7])
sub('Referencias y archivos de verificación')
p('Reyna Barreto, B. D. (2026). Guía práctica de laboratorio N.º 13 Proyecto integrador refinamiento offline first Firebase y permisos nativos. Universidad Peruana Unión.')
p('Referencia de presentación: S13_Practica_Integrador_Juan_Paredes.pdf. Se utilizó como modelo de organización; sus resultados, capturas y commits no se trasladaron como propios.')
p('Código: github.com/antobaldeon/Pharmamobile. Capturas reales: docs/captura/s13. Resultados: shared/build/test-results y reporte HTML de Gradle. Migración: shared/src/commonMain/sqldelight/db/2.sqm.')
# Apply the serif typography of the reference instead of the base template theme.
for style in D.styles:
    for fonts in style.element.xpath('./w:rPr/w:rFonts'):
        for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
            fonts.attrib.pop(qn('w:'+key), None)
    if style.name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
        style.font.name='Times New Roman'
for para in D.paragraphs:
    if para.style.name=='Title':
        para.text='Proyecto integrador sincronización robusta\npermisos y Firebase'
        for run in para.runs: run.font.name='Times New Roman';run.font.size=Pt(17);run.bold=True
for tbl in D.tables:
    for row in tbl.rows:
        for cell in row.cells:
            for shade in cell._tc.get_or_add_tcPr().findall(qn('w:shd')):
                if shade.get(qn('w:fill'))=='DCE6F1': shade.set(qn('w:fill'),'EEEEEE')
D.save('output/doc/S13_Practica_Integrador_Baldeon_FormatoReferencia.docx')
print('GENERADO')
