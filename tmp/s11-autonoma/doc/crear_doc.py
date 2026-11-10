from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import xml.etree.ElementTree as ET
D=Document();s=D.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=s.bottom_margin=Cm(1.7);s.left_margin=s.right_margin=Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=D.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
D.styles['Normal'].font.size=Pt(10.5);D.styles['Normal'].paragraph_format.space_after=Pt(6);D.styles['Normal'].paragraph_format.line_spacing=1.05
D.styles['Title'].font.size=Pt(24);D.styles['Heading 1'].font.size=Pt(16);D.styles['Heading 2'].font.size=Pt(12)
for bd in list(D.styles['Title'].element.xpath('./w:pPr/w:pBdr')):bd.getparent().remove(bd)
D.core_properties.title='Actividad autónoma 11 Pruebas unitarias y escenarios offline';D.core_properties.author=''
f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;f.add_run('Página ').font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
def p(t='',style=None):return D.add_paragraph(t,style)
def h(t):D.add_heading(t,1)
def sub(t):D.add_heading(t,2)
def page():D.add_page_break()
def code(t,size=8):
 q=p(t);q.paragraph_format.space_after=Pt(2);q.paragraph_format.line_spacing=1
 for r in q.runs:r.font.name='Consolas';r.font.size=Pt(size)
 return q
def slot(label,lines=5):
 q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.keep_together=True;q.paragraph_format.line_spacing=1;q.paragraph_format.space_after=Pt(9)
 q.add_run('\n'*(lines//2)+label+'\n'*(lines-lines//2)).font.size=Pt(12)
 for r in q.runs:r.font.color.rgb=RGBColor.from_string('777777')
 pr=q._p.get_or_add_pPr();bd=OxmlElement('w:pBdr')
 for edge in ['top','left','bottom','right']:
  e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');e.set(qn('w:space'),'7');bd.append(e)
 pr.append(bd)
def table(head,rows,widths):
 t=D.add_table(rows=1,cols=len(head));t.autofit=False
 for i,x in enumerate(head):t.rows[0].cells[i].text=str(x)
 for row in rows:
  for c,x in zip(t.add_row().cells,row):c.text=str(x)
 for ri,row in enumerate(t.rows):
  for i,c in enumerate(row.cells):
   c.width=Cm(widths[i]);pr=c._tc.get_or_add_tcPr();bd=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');bd.append(e)
   pr.append(bd);mar=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'75');e.set(qn('w:type'),'dxa');mar.append(e)
   pr.append(mar);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6F1' if ri==0 else ('F6F7F9' if ri%2==0 else 'FFFFFF'));pr.append(sh)
   for q in c.paragraphs:
    q.paragraph_format.space_after=Pt(2)
    for r in q.runs:r.font.size=Pt(9);r.bold=ri==0
  if ri==0:row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 p()

def scenario(id,title,steps,expected,app,db):
 page();h(f'{id} {title}')
 p('Fecha y hora: ____________________  Plataforma: ____________________')
 p('Dispositivo o simulador y versión: ____________________________________')
 sub('Procedimiento y criterio de comprobación');p(steps);p('Comportamiento esperado: '+expected)
 p('Pasos exactos realizados y variantes: __________________________________\n________________________________________________________________')
 sub('Evidencia de la aplicación');p(app);slot(f'Inserta aquí la captura de {id}',5)
 p('Qué mostró realmente la aplicación: ___________________________________\n________________________________________________________________')
 sub('Estado de la base local');p(db);slot(f'Inserta aquí la consulta de SQLite de {id}',3)
 p('Filas, identificadores y estado observados: ______________________________\n________________________________________________________________')
 p('Conclusión propia: __________________________________________________\n________________________________________________________________')

p('Actividad autónoma 11','Title');p('Pruebas unitarias y evidencia de escenarios offline','Subtitle')
p('Desarrollo de Aplicaciones Móviles | Unidad 2 | Semestre 2026 2')
p('Proyecto PharmaMobil sobre PharmaSoft')
p('Estudiante: _________________________________________________________')
p('Código universitario: __________________________________________________')
p('Docente: Mg. Reyna Barreto Benjamin David')
p('Fecha de elaboración: _________________________________________________')
p('Rama: feature/offline-first-baldeon')
p('Enlace de la rama: ____________________________________________________')
p('Entrega: lunes 26 de octubre de 2026 hasta las 23:59')
h('Propósito y alcance')
p('Verificar el funcionamiento offline de PharmaMobil mediante pruebas compartidas, documentar cinco escenarios reales, mostrar la antigüedad de la última sincronización correcta y preparar la sustentación del Producto U2.')
p('La implementación guarda productos en SQLDelight, observa el listado mediante Flow y envía las altas pendientes antes de descargar el catálogo. La nueva tabla de sincronización conserva su fecha entre aperturas. La migración de versión 1 a 2 mantiene productos y pendientes.')
h('Productos incluidos')
for t in ['Suite de seis pruebas exigidas con MockEngine y base SQL en memoria, más verificaciones adicionales.','Bitácora editable de los cinco escenarios con espacio para aplicación y estado de SQLite.','Registro y presentación de la antigüedad de datos, incluidos datos recientes, antiguos y nunca sincronizados.','Guion de ocho minutos con usuarios, preparación previa y criterios de la unidad.']:p(t,'List Bullet')
p('Completar nombres, fechas, resultados observados, capturas y conclusiones después de ejecutar cada prueba manual. Borrar los textos de los espacios e insertar las imágenes en línea con el texto, conservando sus proporciones.')

page();h('1 Suite de pruebas en commonTest')
p('Archivo: shared/src/commonTest/kotlin/pe/edu/upeu/pharmamobile/data/repository/S11PruebasOfflineTest.kt')
p('Cada caso crea su propia base en memoria y utiliza MockEngine de Ktor con ProductoApi y el repositorio REST reales. Las respuestas incluyen DTO y paginación; las pruebas no necesitan emulador, servidor ni esperas reales.')
rows=[('1','Sincronización con red','El Flow emite la lista completa descargada, incluidas todas las páginas.'),('2','Registro sin red','El producto aparece con ID negativo y pendiente igual a 1.'),('3','Envío al reconectar','La alta llega al servidor simulado y se confirma con ID positivo sin marca pendiente.'),('4','La bajada conserva pendientes','Descargar y reemplazar sincronizados no elimina las filas creadas localmente.'),('5','Identificadores sin colisión','Dos productos locales negativos conviven con un producto positivo del servidor.'),('6','Sincronizar dos veces no duplica','Se conserva la misma lista y solo se envía una creación confirmada.')]
table(['N.º','Caso','Verificación'],rows,[0.8,5.1,11.1])
sub('Resultados y comprobaciones adicionales')
roots=[ET.parse(x).getroot() for x in sorted(Path('shared/build/test-results').rglob('TEST-*.xml'))]
total=sum(int(x.attrib['tests']) for x in roots);fails=sum(int(x.attrib['failures']) for x in roots)
p(f'La ejecución verificada contiene {total} pruebas aprobadas y {fails} fallos. La clase de esta actividad contiene los seis casos requeridos y una prueba adicional que confirma que un fallo no modifica la fecha de la última sincronización correcta.')
p('También se verifican el formato de minutos, horas y días; el caso nunca sincronizado; y la migración que conserva pendientes de la versión anterior. El APK Android se generó correctamente. El código y las pruebas iOS compilaron; su ejecución requiere macOS.')
sub('Comando y reporte')
code('.\\gradlew.bat :shared:testAndroidHostTest')
p('Reporte: shared/build/reports/tests/testAndroidHostTest/index.html')
p('Salida completa guardada: docs/S11_AUTONOMA_PRUEBAS.txt')
p('Las pruebas 2 y 4 son esenciales para acreditar el patrón offline. El caso 4 verifica específicamente la bajada con la respuesta HTTP simulada y la operación local utilizada por el repositorio.')

page();h('Salida de la ejecución completa de las pruebas')
p('Transcripción de los resultados de todas las pruebas de la suite. El registro completo de Gradle está disponible en docs/S11_AUTONOMA_PRUEBAS.txt.','Caption')
log=Path('docs/S11_AUTONOMA_PRUEBAS.txt').read_text(encoding='utf-8-sig')
for line in log.splitlines():
 if line.endswith(' PASSED'):code(line,7.3)
for line in log.splitlines():
 if line.startswith('BUILD SUCCESSFUL'):code(line,9)
p(f'Total verificado: {total} pruebas. Fallos: {fails}.')

page();h('Evidencias de la suite ejecutada')
sub('Captura 1 Resumen de la ejecución completa')
p('Abrir el reporte HTML o el panel de pruebas y capturar el total, cero fallos y el resultado satisfactorio.')
slot('Inserta aquí el resumen de las 38 pruebas',8)
sub('Captura 2 Casos de la actividad autónoma')
p('Abrir S11PruebasOfflineTest y capturar los métodos prueba1 a prueba6 aprobados, además del caso de la fecha ante fallos.')
slot('Inserta aquí los resultados de S11PruebasOfflineTest',8)
p('Fecha y hora de la captura: ____________________________________________')

scenario('E1','Apertura sin red con datos previos',
'Sincronizar con red, cerrar completamente la app, activar modo avión y reabrir. Comprobar que Wi-Fi no permanezca conectado. Apagar el backend también garantiza que el emulador no acceda al host.',
'El listado permanece visible y se avisa que no hay conexión. La última sincronización conserva su valor.',
'Capturar el listado, el aviso sin conexión y el icono de modo avión. Esperar el timeout de red si es necesario.',
'En Database Inspector, consultar producto y estado_sincronizacion. Deben conservarse las filas y la fecha de la sincronización anterior.')
scenario('E2','Registro sin red',
'En modo avión y con el backend inaccesible, registrar Autonoma Offline 01 con precio 5.50, stock 10 y una categoría válida. Cerrar y reabrir para comprobar que permanece.',
'El producto aparece y queda marcado como pendiente, aunque el envío no se complete.',
'Capturar la tarjeta del producto con la etiqueta Pendiente de sincronización. Usar este mismo nombre al reconectar.',
'Consultar id, nombre y pendiente. El registro nuevo debe tener ID negativo y pendiente igual a 1; la fecha de sincronización no debe avanzar.')
scenario('E3','Reconexión y envío',
'Encender PharmaSoft, desactivar modo avión y pulsar Sincronizar. Si el JWT venció, iniciar sesión de nuevo y reintentar. Consultar el producto en Swagger y sincronizar una segunda vez.',
'El servidor contiene el producto con ID positivo; su pendiente local se confirma y no se vuelve a enviar en una nueva sincronización.',
'Insertar la app sin la etiqueta de pendiente y la respuesta GET de Swagger con nombre e ID positivo. No mostrar el token.',
'El producto debe tener ID positivo y pendiente igual a 0. No debe quedar su ID temporal. La marca de tiempo cambia solo al finalizar una sincronización correcta.')
scenario('E4','Primera apertura sin red',
'Hacer este escenario al final. Guardar antes las evidencias. En Ajustes de Android, borrar el almacenamiento de PharmaMobil, activar modo avión y abrir la aplicación.',
'Estado informativo sin datos. La implementación muestra el login con No hay productos guardados y Nunca sincronizado; el primer acceso autenticado requiere conexión.',
'Capturar el mensaje informativo y Nunca sincronizado. No intentar iniciar sesión sin servidor para esta evidencia inicial.',
'Las tablas de productos y de sincronización no deben tener filas. Borrar datos también elimina el token y el perfil almacenados.')
scenario('E5','Sesión expirada sin red',
'Realizar antes de E4. Iniciar sesión y sincronizar. Activar modo avión y apagar el backend. Esperar a que venza el token, cerrar y reabrir sin red. Recuperar la conexión y sincronizar.',
'Con perfil guardado se muestran datos locales sin red. Al reconectar, un 401 elimina el token y pide un nuevo login; los productos locales se conservan.',
'Insertar la consulta local con token vencido y la solicitud de login al reconectar. En el perfil dev consultado el token dura un minuto; confirmar el perfil utilizado.',
'Los productos se conservan durante el vencimiento y el 401. La fecha no avanza por un intento fallido. El perfil y token se eliminan cuando el servidor rechaza la sesión.')
p('Argumento sobre el comportamiento observado: ___________________________\n________________________________________________________________')

page();h('3 Antigüedad de los datos en pantalla')
p('La tabla estado_sincronizacion guarda ultima_correcta en milisegundos Unix. El catálogo y la fecha se escriben en una transacción después de subir pendientes y descargar correctamente. Un fallo conserva la fecha anterior. La etiqueta se actualiza cada minuto mientras la pantalla está visible.')
sub('Captura 10 Datos recientes')
p('Con fecha automática correcta, iniciar sesión y sincronizar. Capturar Actualizado hace un momento.')
slot('Inserta aquí la última sincronización reciente',6)
sub('Captura 11 Datos de más de un día')
p('Conservar una sincronización real y dejar pasar más de 24 horas sin sincronizar. Para ensayar, se puede adelantar el reloj del emulador dos días con la red desconectada, declarando la simulación. Restaurar fecha automática antes de reconectar.')
slot('Inserta aquí Actualizado hace 1 día o más',6)
p('Método usado: [ ] Tiempo real transcurrido   [ ] Simulación del reloj')
p('Instante guardado y fecha del dispositivo: _________________________________')
p('El caso Nunca sincronizado se evidencia en E4. No sustituir la evidencia real por una fecha modificada sin declararlo.')

page();h('4 Guion de sustentación del Producto U2')
p('Duración total: ocho minutos. Sustentación: 27 de octubre de 2026.')
sub('Preparación previa')
for t in ['Backend y base encendidos, categoría válida y productos de prueba disponibles.','App con sesión cerrada para demostrar login y catálogo previamente guardado.','Usuarios admin y vendedor preparados; comprobar la duración del token del perfil utilizado.','Swagger abierto con una petición válida de escritura para comprobar 403 con vendedor.','Android e iOS disponibles; ensayar el cambio de plataforma y la desconexión con cronómetro.']:p(t,'List Bullet')
table(['Tiempo','Usuario','Demostración'],[
('0 a 1 min','admin','Login incorrecto y correcto. Explicar JWT y almacenamiento seguro sin exponer el token.'),
('1 a 3 min','admin','Listar, registrar, actualizar y eliminar un producto de prueba contra PharmaSoft.'),
('3 a 5 min','vendedor y admin','Con vendedor, mostrar falta de permiso y provocar 403 en Swagger con un POST válido. Con admin, editar un producto del servidor con nombre de dos caracteres y mostrar el error bajo el campo; restaurar el nombre.'),
('5 a 7 min','admin','Activar modo avión, ver catálogo y antigüedad, crear pendiente, recuperar red y comprobar envío e ID positivo en Swagger. Renovar login si venció el token.'),
('7 a 8 min','Autorizado','Mostrar la funcionalidad en Android e iOS y explicar los drivers y el código compartido.')],[2.1,2.6,12.3])
p('La aplicación oculta las acciones no autorizadas; el 403 se demuestra mediante una petición real en Swagger con el usuario sin permiso. La compilación iOS no sustituye la demostración en ejecución.')
sub('Registro del ensayo')
p('Fecha y hora: ____________________  Duración medida: ____________________')
p('Incidencias y ajustes: __________________________________________________\n________________________________________________________________')

page();h('5 Repositorio y cierre de la actividad')
p('Rama: feature/offline-first-baldeon')
p('Enlace publicado: _____________________________________________________')
p('Commit de implementación: _____________________________________________')
p('Commit de pruebas y evidencias: _________________________________________')
p('Registrar hashes reales después de crear y publicar los commits de esta actividad.')
sub('Captura 12 Rama y commits nuevos')
slot('Inserta aquí la rama y el historial de la actividad autónoma',6)
sub('Lista de cotejo antes de entregar')
for t in ['Portada con nombre, fecha y enlace a la rama.','Seis casos requeridos implementados y salida completa de pruebas incluida.','Cinco escenarios con fecha, plataforma, pasos, captura, estado local y conclusión propia.','E3 incluye respuesta de Swagger con ID positivo.','E5 explica y argumenta la resolución de la sesión al reconectar.','Antigüedad reciente, mayor de un día y Nunca sincronizado evidenciadas.','Guion de ocho minutos con usuarios y preparación previa.','Commits publicados y enlace de rama accesible.']:p('[ ] '+t)
sub('Entrega y referencias')
p('Guardar una copia editable y exportar a S11_ActividadAutonoma_Baldeon.pdf. Subir el PDF al aula virtual y colocar el enlace a la rama en el comentario. Plazo: 26 de octubre de 2026, 23:59.')
p('Fuente: Actividad Autónoma 11, Pruebas unitarias y evidencia de escenarios offline, Desarrollo de Aplicaciones Móviles. Verificación del proyecto: docs/S11_AUTONOMA_PRUEBAS.txt. Instrucciones ampliadas: docs/S11_AUTONOMA_COMO_PROBAR.md.')
Path('output/doc').mkdir(parents=True,exist_ok=True)
D.save('output/doc/S11_ActividadAutonoma_Baldeon_Editable.docx')
print('Documento creado')
