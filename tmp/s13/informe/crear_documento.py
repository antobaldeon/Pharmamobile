from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import xml.etree.ElementTree as E,json
D=Document();sec=D.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=sec.bottom_margin=Cm(1.65);sec.left_margin=sec.right_margin=Cm(2)
for n in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=D.styles[n];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
D.styles['Normal'].font.size=Pt(10.5);D.styles['Normal'].paragraph_format.space_after=Pt(6);D.styles['Normal'].paragraph_format.line_spacing=1.08
D.styles['Title'].font.size=Pt(24);D.styles['Heading 1'].font.size=Pt(17);D.styles['Heading 2'].font.size=Pt(12)
D.styles['Caption'].font.size=Pt(9);D.styles['Caption'].font.bold=False
for node in D.styles['Title'].element.xpath('./w:pPr/w:pBdr'):node.getparent().remove(node)
D.core_properties.title='Proyecto integrador y evidencias de Android en PharmaMobil';D.core_properties.author=''
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;r=f.add_run('Página ');r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
def p(t='',style=None):return D.add_paragraph(t,style)
def h(t):D.add_heading(t,1)
def sub(t):D.add_heading(t,2)
def page():D.add_page_break()
def pic(name,height=17.5):
 q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture('docs/captura/s13/'+name+'.png',height=Cm(height))
def table(headers,rows,widths):
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for c,v in zip(t.rows[0].cells,headers):c.text=v
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 for ri,row in enumerate(t.rows):
  for ci,c in enumerate(row.cells):
   c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=c._tc.get_or_add_tcPr();bd=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    z=OxmlElement('w:'+edge);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'D9D9D9');bd.append(z)
   pr.append(bd);mar=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    z=OxmlElement('w:'+edge);z.set(qn('w:w'),'85');z.set(qn('w:type'),'dxa');mar.append(z)
   pr.append(mar);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6F1' if ri==0 else ('F5F7F9' if ri%2==0 else 'FFFFFF'));pr.append(sh)
   for q in c.paragraphs:
    q.paragraph_format.space_after=Pt(3)
    for r in q.runs:r.font.size=Pt(9);r.bold=ri==0
  cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
  if ri==0:rep=OxmlElement('w:tblHeader');row._tr.get_or_add_trPr().append(rep)
 p()

p('Proyecto integrador y evidencias de Android en PharmaMobil','Title')
p('Informe de la guía práctica 13','Subtitle')
p('Desarrollo de Aplicaciones Móviles | Unidad 3 | Ciclo VI | Semestre 2026 2')
p('Fecha: 3 de noviembre de 2026')
p('Estudiante: __________________________________________ Baldeón')
p('Integrante adicional: ______________________________________________')
p('Docente: Benjamin David Reyna Barreto')
p('Repositorio: https://github.com/antobaldeon/Pharmamobile')
h('1 Propósito y alcance')
p('Refinar la persistencia offline first de PharmaMobil, controlar los fallos de envío y resolver un permiso nativo real desde una interfaz común. Este informe documenta exclusivamente Android. No incluye ejecución, capturas ni evaluación funcional de iOS.')
h('2 Trabajo implementado')
for t in [
'La migración SQLDelight 2.sqm amplía la base local a versión 3 con intentos y ultimoError. Conserva los productos y pendientes existentes.',
'El repositorio diferencia errores transitorios y permanentes. Una fila que alcanza cinco intentos queda fallida, permanece visible y puede revisarse o reenviarse mediante una decisión explícita.',
'Los reenvíos de altas utilizan espera creciente. Como PharmaSoft no ofrece una clave idempotente para POST, no se repiten automáticamente envíos inciertos; el usuario recibe una advertencia para comprobar antes el servidor.',
'La pantalla observa la base local y presenta pendientes, fallidas, último error, intentos y antigüedad de los datos. La subida precede a la descarga y los fallos no borran las filas locales.',
'El permiso de notificaciones distingue Denegado, Denegado para siempre y Concedido. Se explica su finalidad, se ofrece abrir Ajustes y se puede emitir una notificación local de prueba.'
]:p(t)
p('Se preparó Crashlytics mediante GitLive detrás de Telemetria. La comprobación remota de Firebase continúa pendiente porque no se ha incorporado google-services.json; una notificación local no demuestra integración con Firebase.')

page();h('3 Recorrido y tabla de problemas')
p('La tabla distingue lo observado durante esta verificación de los aspectos identificados al revisar el código. Las capturas siguientes corresponden a la aplicación real en un emulador Android, sin imágenes simuladas.')
table(['Momento y hallazgo','Gravedad','Decisión y estado'],[
('Inicio con sesión vencida: se mostró el mensaje y el formulario de login.','Media','Se verificó recuperación mediante login admin.'),
('Catálogo de PharmaSoft aislado y recién creado: no contenía productos.','Media','Mantener estado vacío informativo. No copiar tablas de otro proyecto.'),
('Permiso denegado: la pantalla explica el propósito y permite solicitar.','Media','Resuelto y capturado en Android.'),
('Denegación definitiva: el diálogo deja de aparecer.','Media','Abrir Ajustes; al regresar se actualiza el estado. Verificado.'),
('Alta sin red: faltaba memoria por fila del fallo.','Alta','Resuelto con intentos y ultimoError. Verificado con ID local negativo.'),
('Reintentos agotados: el producto no debe desaparecer.','Alta','Tras cinco envíos fallidos sigue en SQLite y aumenta el contador de fallidas.'),
('Respuesta perdida de un POST puede causar duplicados.','Alta','Reenvío explícito informado. Idempotencia del backend pendiente para sesión 14.'),
('El 401 puede descartar el borrador del formulario; catálogo compartido entre sesiones.','Alta','Identificado en código. Resolver borradores y separación por usuario en sesión 14.'),
('Firebase sin configuración del proyecto.','Media','Adaptador preparado. Pendiente configuración y recepción real en consola.')
],[8.0,1.7,7.3])
sub('Entorno y separación de datos')
p('Android: emulador Pixel 9a. Backend: PharmaSoft sobre Oracle en localhost:1522/FREEPDB1, con usuario exclusivo PHARMASOFT_DEV. Las migraciones V1, V2 y V3 se aplicaron correctamente al nuevo esquema; TESTDB conserva sus datos e historial anterior.')
p('No se borró el almacenamiento de PharmaMobil para estas pruebas. Se instaló el APK actualizado conservando sus datos y se inició sesión con admin. El nombre utilizado para el alta de prueba fue EvidenciaS13Android, precio 5.50 y stock 10.')

page();h('4 Permiso denegado')
p('Antes de conceder el permiso, la pantalla muestra Denegado, explica para qué se usarán las notificaciones y ofrece Permitir notificaciones. La consulta del catálogo no depende de conceder este permiso.')
pic('01_permiso_denegado')
p('Figura 1. Captura real del estado Denegado y de la explicación previa. Hora mostrada por el emulador: 08:37.','Caption')
p('Resultado: el estado inicial no se confunde con una denegación definitiva y el botón permite abrir el diálogo del sistema.')

page();h('5 Permiso denegado para siempre')
p('Se solicitó el permiso y se denegó dos veces desde el diálogo de Android. La aplicación cambió a Denegado para siempre y sustituyó la solicitud por Abrir Ajustes.')
pic('02_permiso_permanente')
p('Figura 2. Captura real de la denegación definitiva con acceso a Ajustes. Hora mostrada por el emulador: 08:38.','Caption')
p('Resultado: el usuario dispone de una salida cuando Android ya no permite volver a mostrar el diálogo. Se abrió la configuración de la aplicación para habilitar el permiso.')

page();h('6 Permiso concedido y notificación local')
p('Se habilitaron las notificaciones desde Ajustes y se volvió a PharmaMobil. La pantalla actualizó el estado a Concedido. Al pulsar Probar notificación apareció un aviso real en la bandeja de Android.')
# Images inline side by side, without using a table as a layout device.
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture('docs/captura/s13/03_permiso_concedido.png',width=Cm(7.4))
q.add_run('   ')
q.add_run().add_picture('docs/captura/s13/04_notificacion_real.png',width=Cm(7.4))
p('Figuras 3 y 4. A la izquierda, estado Concedido; a la derecha, notificación emitida por PharmaMobil y visible en la bandeja del sistema.','Caption')
p('Resultado: la implementación Android obtiene el permiso real y ejecuta una capacidad nativa. La notificación es local; no corresponde a un mensaje FCM ni acredita recepción de eventos en Firebase.')

page();h('7 Pendientes y límite de intentos')
p('Se activó el modo avión y se deshabilitó Wi Fi. Se registró EvidenciaS13Android. El primer intento dejó la fila pendiente con su error. Luego se pulsó Sincronizar cuatro veces, esperando el final de cada operación: al quinto fallo la fila pasó al contador de fallidas.')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture('docs/captura/s13/05_pendiente_intento.png',width=Cm(7.4));q.add_run('   ')
q.add_run().add_picture('docs/captura/s13/06_fila_fallida_cinco_intentos.png',width=Cm(7.4))
p('Figuras 5 y 6. Primer fallo: 1 cambio por enviar y 0 fallidos, Intentos 1/5. Límite: 0 cambios por enviar y 1 fallido, Intentos 5/5.','Caption')
rows=json.loads(Path('tmp/s13/informe/sqlite.json').read_text(encoding='utf-8'))
p('Comprobación de SQLite: la fila se mantuvo guardada después de agotar los intentos. Consulta ejecutada: SELECT id, nombre, pendiente, intentos, ultimoError FROM producto.')
for r in rows:
 if r[1]=='EvidenciaS13Android':p(f'ID {r[0]} | pendiente {r[2]} | intentos {r[3]} | último error: {r[4]}.')
p('Conclusión: alcanzar el límite no elimina el trabajo del usuario. La fila queda disponible para revisión. Al terminar se restableció la conexión original del emulador; el producto de prueba permanece fallido y no se ha confirmado su reenvío.')

page();h('8 Pruebas y estado de entrega')
p('Se comprobó la compilación del APK y la suite Android. El proyecto contiene 45 pruebas aprobadas y cero fallos. Las siete pruebas específicas de S13 comprueban clasificación de errores, espera creciente, límites y estados del permiso sin depender de un dispositivo.')
results=[];total=0
for f in sorted(Path('shared/build/test-results').rglob('TEST-*.xml')):
 r=E.parse(f).getroot();total+=int(r.attrib['tests']);results.append([r.attrib['name'].split('.')[-1],r.attrib['tests'],r.attrib['failures']])
table(['Clase de prueba','Pruebas','Fallos'],results,[12.0,2.5,2.5])
p('Verificación: .\\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug. Resultado BUILD SUCCESSFUL. Reporte HTML: shared/build/reports/tests/testAndroidHostTest/index.html.')
sub('Firebase y repositorio')
p('GitLive Crashlytics 2.7.0 está encapsulado en data/firebase y se utiliza mediante Telemetria del dominio. Solo se registran categorías técnicas. Falta añadir androidApp/google-services.json y comprobar los informes en la consola; no se presenta una captura ficticia de Firebase.')
p('Rama actual: feature/offline-first-baldeon. Último commit disponible: b660000. Los cambios de S13 siguen en el árbol de trabajo. Está pendiente publicarlos en la rama feature/integrador-13 solicitada por la guía; este informe no acredita commits que todavía no existen.')
p('Referencia: Guía Práctica 13 Proyecto integrador, 3 de noviembre de 2026, apartados 5, 7 y 8. Evidencias: capturas originales en docs/captura/s13 y resultados JUnit del proyecto.')
Path('output/doc').mkdir(parents=True,exist_ok=True)
D.save('output/doc/S13_ProyectoIntegrador_Android_Editable.docx')
print('DOCUMENTO CREADO',total)
