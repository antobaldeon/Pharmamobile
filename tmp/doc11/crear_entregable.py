from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
import xml.etree.ElementTree as ET
D=Document();s=D.sections[0]
s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=s.bottom_margin=Cm(1.8);s.left_margin=s.right_margin=Cm(2.1)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=D.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
D.styles['Normal'].font.size=Pt(10.5)
D.styles['Normal'].paragraph_format.space_after=Pt(6)
D.styles['Normal'].paragraph_format.line_spacing=1.08
D.styles['Title'].font.size=Pt(23)
D.styles['Heading 1'].font.size=Pt(16)
D.styles['Heading 2'].font.size=Pt(12)
D.styles['Caption'].font.size=Pt(9)
D.core_properties.title='Persistencia local y sincronización offline first en PharmaMobil'
D.core_properties.author=''
footer=s.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('Página ');r.font.size=Pt(9)
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
def p(t="",style=None): return D.add_paragraph(t,style)
def h(t):D.add_heading(t,1)
def sub(t):D.add_heading(t,2)
def page():D.add_page_break()
def code(t):
 r=p(t).runs[0];r.font.name='Consolas';r.font.size=Pt(8.5)
def slot(n,title,steps,criterion):
 sub(f'Captura {n} {title}')
 p(steps)
 q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
 q.paragraph_format.keep_together=True
 q.paragraph_format.space_before=Pt(4);q.paragraph_format.space_after=Pt(7)
 q.paragraph_format.line_spacing=1
 r=q.add_run('\n\n\nInserta aquí la captura '+str(n)+'\n\n\n');r.font.size=Pt(15);r.font.color.rgb=RGBColor.from_string('777777')
 pr=q._p.get_or_add_pPr();borders=OxmlElement('w:pBdr')
 for edge in ['top','left','bottom','right']:
  e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:space'),'8');e.set(qn('w:color'),'D9D9D9');borders.append(e)
 pr.append(borders)
 p('Comprobar: '+criterion,'Caption')
 p('Resultado observado: __________________________________________________')

def table(headers,rows):
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False
 widths=[10.0,2.1,2.1,2.1]
 for i,v in enumerate(headers):t.rows[0].cells[i].text=v
 for vals in rows:
  for cell,v in zip(t.add_row().cells,vals):cell.text=str(v)
 for ri,row in enumerate(t.rows):
  for i,c in enumerate(row.cells):
   c.width=Cm(widths[i]);pr=c._tc.get_or_add_tcPr()
   bd=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');bd.append(e)
   pr.append(bd)
   mar=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'75');e.set(qn('w:type'),'dxa');mar.append(e)
   pr.append(mar)
   shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DCE6F1' if ri==0 else ('F5F7F9' if ri%2==0 else 'FFFFFF'));pr.append(shade)
   for q in c.paragraphs:
    q.paragraph_format.space_after=Pt(2)
    if i>0:q.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for r in q.runs:r.font.size=Pt(9);r.bold=ri==0
  if ri==0:
   rep=OxmlElement('w:tblHeader');row._tr.get_or_add_trPr().append(rep)
 p('')

D.add_paragraph('Persistencia local y sincronización offline first en PharmaMobil','Title')
p('Informe de la práctica de laboratorio 11','Subtitle')
p('Desarrollo de Aplicaciones Móviles | Unidad 2 | Ciclo VI | Semestre 2026 2')
p('Fecha de la sesión: 20 de octubre de 2026')
p('Integrante 1: ________________________________________________________')
p('Integrante 2: ________________________________________________________')
p('Docente: Mg. Reyna Barreto Benjamin David')
p('Rama de trabajo: ____________________________________________________')
p('Enlace del repositorio y rama: __________________________________________')
h('1 Propósito de la práctica')
p('Implementar almacenamiento local con SQLDelight en PharmaMobil para consultar productos sin conexión y registrar altas pendientes. Al recuperar la conexión, la aplicación envía los registros locales antes de descargar el catálogo de PharmaSoft.')
h('2 Implementación realizada')
for t in [
'Se configuró PharmaDb con drivers Android e iOS y una tabla de productos que conserva precio, stock, estado activo, categoría y marca de pendiente.',
'ProductoLocal concentra las consultas. ProductoRepositorioOffline expone observar y sincronizar; la pantalla observa la base mediante Flow y conserva los datos cuando falla la red.',
'Las altas locales reciben identificadores negativos y pendiente igual a 1. Cada envío confirmado reemplaza la fila temporal por el identificador positivo del servidor y pendiente igual a 0.',
'La sincronización sube primero y descarga después. Las escrituras se serializan y el reemplazo del catálogo se realiza en una transacción.',
'Se conserva un perfil local sin JWT para restaurar la sesión ante falta de conexión después de un primer acceso con red. El token permanece en el almacén seguro; un 401 o cerrar sesión elimina la sesión guardada.'
]:p(t)
h('3 Alcance de las operaciones')
p('Crear productos, editar pendientes y eliminar pendientes funciona sin red. Editar o eliminar un producto ya sincronizado requiere conexión. Se sincroniza al abrir productos, al registrar y mediante el botón Sincronizar.')
p('La comprobación manual se documenta en las páginas siguientes. Completar cada resultado observado después de realizar la prueba.')

page();h('4 Organización del código y validación')
sub('Archivos principales')
for t in [
'Esquema SQL: shared/src/commonMain/sqldelight/db/Producto.sq y SesionLocal.sq.',
'Código común: data/local/ProductoLocal.kt, SesionLocal.kt y CreadorDeDriver.kt; data/repository/ProductoRepositorioOffline.kt; di/AppModule.kt.',
'Presentación: presentation/producto/ProductoViewModel.kt, ProductoUiState.kt y ProductoScreen.kt.',
'Plataformas: androidMain y iosMain contienen los drivers y sus registros en PlatformModule. Las pruebas comparten commonTest y usan drivers de prueba específicos por plataforma.'
]:p(t)
sub('Resultados automáticos verificados')
rows=[];total=0
for f in sorted(Path('shared/build/test-results').rglob('TEST-*.xml')):
 e=ET.parse(f).getroot();total+=int(e.attrib['tests'])
 rows.append([e.attrib['name'].split('.')[-1],e.attrib['tests'],e.attrib.get('failures','0'),e.attrib.get('errors','0')])
table(['Clase de prueba','Pruebas','Fallos','Errores'],rows)
p(f'El resultado verificado fue de {total} pruebas Android aprobadas. Se generó el APK debug y se compiló el código y las pruebas para iosArm64 e iosSimulatorArm64. Las pruebas iOS se compilaron, pero no se ejecutaron en Windows.')
code('.\\gradlew.bat :shared:testAndroidHostTest :androidApp:assembleDebug')
p('Reporte HTML: shared/build/reports/tests/testAndroidHostTest/index.html')
sub('Observaciones técnicas')
p('Los pendientes confirmados no se reenvían en una nueva sincronización. Si el servidor acepta un POST y su respuesta se pierde, evitar un duplicado en el reintento requiere idempotencia en PharmaSoft.')
p('Para completar el informe, reemplazar los espacios por capturas reales y anotar el resultado observado. En Word, borrar las líneas del espacio e insertar la imagen en línea con el texto; conservar sus proporciones.')
p('Fuente de la práctica: Guía Práctica de Laboratorio 11, Persistencia local con SQLDelight y estrategia offline first, 20 de octubre de 2026. Verificación del proyecto: docs/SESION11_VERIFICACION.md.','Caption')

page();h('5 Evidencias de consulta en Android')
slot(1,'Listado inicial con conexión','Encender PharmaSoft, iniciar sesión, abrir Productos y pulsar Sincronizar. Capturar el listado y el botón.','Se descargan productos y se muestran en la aplicación.')
slot(2,'Listado después de abrir sin conexión','Cerrar completamente la app. Detener PharmaSoft o activar modo avión y reabrir. Capturar productos y el aviso Sin conexión mostrando datos guardados.','El listado permanece disponible después de cerrar y abrir sin backend. Si se usa modo avión, incluir el icono o una captura adicional de ajustes.')

page();h('6 Evidencias de registro pendiente')
p('Usar el mismo nombre de producto en las capturas 3 a 6, por ejemplo Prueba Offline 01. Anotar un ID de categoría que exista en PharmaSoft.')
slot(3,'Producto creado sin red','Con el backend apagado, registrar Prueba Offline 01 con precio 5.50 y stock 10. Esperar a que termine el intento de conexión y capturar la tarjeta.','El nuevo producto aparece con la etiqueta Pendiente de sincronización.')
slot(4,'Pendiente conservado al reabrir','Cerrar completamente la app y abrirla otra vez sin conexión. Capturar el mismo producto y su etiqueta de pendiente.','El alta permanece guardada y no depende de mantener la app abierta.')

page();h('7 Evidencias de sincronización')
slot(5,'Reconexión y producto sincronizado','Encender PharmaSoft, recuperar la conexión y pulsar Sincronizar. Capturar el mismo producto; volver a sincronizar para comprobar que no se repite.','Desaparece la marca de pendiente y no aparece una segunda copia local.')
slot(6,'Producto registrado en PharmaSoft','En Swagger, autorizarse y ejecutar GET /api/v1/productos. Localizar Prueba Offline 01 en la página correspondiente y capturar nombre e identificador. No mostrar el token.','El servidor contiene el mismo producto con un ID positivo. Verlo solo en la app no acredita la sincronización.')

page();h('8 Evidencias de pruebas e iOS')
slot(7,'Pruebas automáticas aprobadas','Ejecutar el comando de pruebas de la página 2. Capturar el reporte HTML o el panel de pruebas con el total y sin fallos; si es necesario, añadir otra imagen con los siete casos offline.','Se ejecutan las pruebas y el resultado no presenta fallos. El total verificado en esta versión es 26.')
slot(8,'Listado sin conexión en iOS','En una Mac con Xcode, ejecutar la app, iniciar sesión y sincronizar con red. Cerrar, cortar la conexión al backend y reabrir. Capturar el listado y aviso en iOS.','La lectura offline funciona también en iOS. La compilación por sí sola no sustituye esta captura.')

page();h('9 Evidencias del repositorio y documentación')
slot(9,'Rama y commits','Capturar la rama y el historial de Git, en Android Studio o en el repositorio remoto. Deben verse los mensajes y fechas de los commits de la práctica.','La rama sigue el nombre solicitado y hay commits reales distribuidos durante el trabajo.')
slot(10,'README actualizado','Capturar la sección Persistencia offline first del README, con explicación de pendientes, orden de sincronización y ejecución de pruebas.','La documentación explica el comportamiento implementado y cómo comprobarlo.')

page();h('10 Registro final de comprobación')
p('Completar después de ejecutar el ciclo real y colocar las capturas. No marcar como verificada una prueba que solo se haya compilado.')
checks=[
'El esquema SQLDelight compila y genera PharmaDb.',
'Los drivers están registrados en Android, iOS y pruebas.',
'La capa local no depende de Ktor ni de DTO remotos.',
'El repositorio expone observar mediante Flow y sincronizar.',
'El ViewModel observa la base y no recarga manualmente la lista después de cada operación.',
'La app muestra productos con PharmaSoft apagado.',
'Un producto creado sin red queda marcado como pendiente.',
'La sincronización sube pendientes antes de descargar.',
'El producto aparece en PharmaSoft tras reconectar con un ID positivo.',
'Hay al menos tres pruebas compartidas y todas pasan.'
]
for i,t in enumerate(checks,1):p(f'{i}. {t}\n    Resultado: [ ] Sí   [ ] No   Observación: __________________________')
sub('Datos del entorno de las capturas')
p('Android y versión del emulador o dispositivo: ____________________________')
p('iOS y versión del simulador o dispositivo: _______________________________')
p('Nombre de quien realizó la comprobación iOS: ___________________________')
p('Nombre del producto de prueba e ID asignado por PharmaSoft: ______________')
p('Enlace de la rama publicada: __________________________________________')
sub('Conclusión de la práctica')
p('La implementación utiliza la base local como fuente de datos de la interfaz y conserva las altas pendientes para enviarlas al servidor. Las pruebas automáticas verifican los escenarios de red, ausencia de red y reconexión. Las capturas incorporadas deben demostrar el ciclo completo y el funcionamiento en ambas plataformas.')
p('Incidencias encontradas y solución aplicada: ______________________________\n___________________________________________________________________\n___________________________________________________________________')
Path('output/doc').mkdir(parents=True,exist_ok=True)
for border in list(D.styles['Title'].element.xpath('./w:pPr/w:pBdr')): border.getparent().remove(border)
D.save('output/doc/S11_Entregable_Offline_First_Editable.docx')
print('DOCX generado')

