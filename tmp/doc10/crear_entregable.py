from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT

out=Path('output/doc/Entregable_Sesion10_Android_Editable.docx')
d=Document();sec=d.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=Cm(1.7);sec.left_margin=sec.right_margin=Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=d.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_after=Pt(6)
d.styles['Normal'].font.size=Pt(10.5);d.styles['Normal'].paragraph_format.line_spacing=1.08
d.styles['Title'].font.size=Pt(23);d.styles['Heading 1'].font.size=Pt(15);d.styles['Heading 2'].font.size=Pt(12)
d.core_properties.author='';d.core_properties.last_modified_by='';d.core_properties.title='Autenticación JWT en PharmaMobil Android'
def p(t):return d.add_paragraph(t)
def h(t):d.add_heading(t,1)
def page():d.add_page_break()
def slot(n,title,procedure,expected,height=6):
 d.add_heading(title,2);p(procedure);p('Resultado esperado: '+expected)
 box=p('')
 box.alignment=WD_ALIGN_PARAGRAPH.CENTER
 box.paragraph_format.space_before=Pt(8);box.paragraph_format.space_after=Pt(8)
 box.paragraph_format.line_spacing=1.2
 for r in box.runs:r.font.color.rgb=RGBColor.from_string('666666');r.font.size=Pt(10)
 pr=box._p.get_or_add_pPr();shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'F2F4F7');pr.append(shade)
 spacing=pr.find(qn('w:spacing'));spacing.set(qn('w:before'),str(int(height*130)));spacing.set(qn('w:after'),str(int(height*130)))
 cap=p('Figura '+str(n)+' '+title);cap.style=d.styles['Caption']
 p('Resultado observado: [Completar después de ejecutar la prueba]')

d.add_paragraph('Autenticación JWT en PharmaMobil Android','Title')
p('Entregable de la sesión 10 de Desarrollo de Aplicaciones Móviles')
p('El informe documenta la integración de PharmaMobil con PharmaSoft y organiza la evidencia de autenticación, almacenamiento seguro y permisos en Android. La implementación cuenta con compilación correcta y 15 pruebas automatizadas aprobadas. Los resultados de ejecución en el emulador se registran junto a cada captura.')
h('1 Implementación y entorno')
p('Se incorporaron el formulario de login, los modelos y casos de uso de sesión, el almacén cifrado de Android, el plugin Auth de Ktor y la navegación según los permisos. La barra superior muestra el usuario y sus roles. Los comentarios del código usan la etiqueta Sesion 10 y describen su finalidad.')
p('Entorno de prueba: Android Studio y emulador Android. Backend local en http://localhost:8080; desde el emulador, http://10.0.2.2:8080. Oracle y PharmaSoft deben permanecer en ejecución.')
p('Emulador y versión Android: [Completar]    Fecha de ejecución: [Completar]')
t=d.add_table(rows=1,cols=3);t.alignment=WD_TABLE_ALIGNMENT.CENTER
for cell,txt in zip(t.rows[0].cells,['Usuario','Rol','Permisos relevantes']):cell.text=txt
for vals in [('admin','ADMIN','Acceso completo'),('vendedor','VENDEDOR','Productos solo lectura; clientes y ventas'),('almacen','ALMACENERO','Lectura y escritura de catálogo')]:
 for c,txt in zip(t.add_row().cells,vals):c.text=txt
for row in t.rows:
 for c in row.cells:
  c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  pr=c._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
  for edge in ['top','left','bottom','right']:
   el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
  pr.append(borders)
  for para in c.paragraphs:para.paragraph_format.space_after=Pt(5);para.paragraph_format.space_before=Pt(5)
for c in t.rows[0].cells:
 sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6F1');c._tc.get_or_add_tcPr().append(sh)
 for run in c.paragraphs[0].runs:run.bold=True
h('2 Inicio de sesión')
slot(1,'Pantalla de login Android','Abrir la app sin sesión guardada e ingresar las credenciales de uno de los usuarios de prueba.','Se muestran usuario, contraseña y el botón Ingresar. El login correcto abre Productos.',3)
page();h('3 Interfaz y permisos por usuario')
slot(2,'Administrador','Ingresar con admin y Admin123. Abrir Productos.','La barra muestra Bienvenido admin y ADMIN; están disponibles registrar, editar y eliminar.',4)
slot(3,'Vendedor','Cerrar sesión e ingresar con vendedor y Vendedor123.','La barra identifica VENDEDOR; el catálogo se puede consultar, pero no aparecen los controles de escritura.',4)
slot(4,'Almacenero','Cerrar sesión e ingresar con almacen y Almacen123.','La barra identifica ALMACENERO; se permite escribir en catálogo y el menú no ofrece Clientes ni Pedidos.',4)
page();h('4 CRUD autenticado y persistencia')
slot(5,'Operación de productos con sesión activa','Con admin o almacen, registrar un producto usando una categoría existente y verificar que aparece en el listado.','El servidor acepta la operación autenticada y la app muestra el producto registrado.',6)
slot(6,'Sesión guardada después de reabrir','Iniciar sesión, cerrar completamente la app sin pulsar Cerrar sesión y volver a abrirla antes de que expire el token.','La app consulta auth me y entra a Productos sin pedir credenciales; conserva usuario y roles.',6)
p('Comprobación de cierre explícito: pulsar Cerrar sesión y volver a abrir la app. Debe mostrarse el login. Resultado observado: [Completar].')
page();h('5 Respuestas de autenticación y autorización')
slot(7,'Respuesta 401 y regreso al login','Usar una sesión expirada y pulsar Recargar en Productos. Para una prueba breve, configurar temporalmente la expiración del backend en 1 minuto, reiniciarlo e iniciar una sesión nueva. Restaurar luego 60 minutos.','Se borra el token y se muestra el login con el aviso de sesión expirada.',6)
slot(8,'Respuesta 403 y conservación de sesión','Provocar una petición a una ruta sin permiso desde la app. Esta prueba requiere una acción temporal de diagnóstico porque la interfaz oculta las acciones no autorizadas.','La app muestra falta de permisos y mantiene la sesión; una consulta permitida sigue funcionando.',6)
p('Un resultado 403 de Postman verifica el backend, pero no sustituye esta evidencia de la interfaz Android.')
page();h('6 Registro seguro y validación')
slot(9,'Authorization oculto en Logcat','Ejecutar la variante debug. En Android Studio abrir Logcat, seleccionar el emulador y filtrar KTOR. Entrar a Productos y pulsar Recargar.','La cabecera Authorization aparece saneada; no se ve el JWT completo ni la contraseña.',7)
h('7 Comprobaciones de entrega')
for text in ['Login con los tres usuarios y saludo con rol','CRUD autenticado en Android','Persistencia tras cerrar y reabrir','Cierre explícito de sesión','401 con aviso y regreso al login','403 con mensaje y sesión conservada','Authorization oculto en Logcat','README actualizado con Autenticación y usuarios de prueba']:
 p('☐ '+text)
p('Repositorio y rama de entrega: [Completar enlace a feature/auth-jwt-apellido]')
p('Enlaces a los commits de la sesión: [Completar]')
h('8 Verificación automatizada')
p('La compilación Android generó el APK debug. Se ejecutaron 15 pruebas sin fallos, incluidas cuatro de autenticación: login sin token anterior y limpieza de caché Bearer; recuperación de identidad mediante auth me; diferencia entre 403 y 401; y credenciales inválidas. Estas pruebas no sustituyen las capturas del emulador.')
p('Referencia: Guía Práctica de Laboratorio 10 Autenticación JWT y almacenamiento seguro en PharmaMobil, 13 de octubre de 2026.')
d.save(out)
print(out.resolve())
