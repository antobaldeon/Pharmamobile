from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from zipfile import ZipFile

out=Path('output/doc/S10_ActividadAutonoma_Android_Editable.docx');out.parent.mkdir(parents=True,exist_ok=True)
d=Document();sec=d.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=Cm(1.7);sec.left_margin=sec.right_margin=Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=d.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_after=Pt(6)
 st.paragraph_format.line_spacing=1.08
 for border in st.element.xpath('.//w:pBdr'):border.getparent().remove(border)
d.styles['Normal'].font.size=Pt(10.5);d.styles['Title'].font.size=Pt(25)
d.styles['Heading 1'].font.size=Pt(16);d.styles['Heading 2'].font.size=Pt(12)
d.styles['Caption'].font.size=Pt(9)
d.core_properties.author='';d.core_properties.last_modified_by='';d.core_properties.title='Validación de sesión JWT en PharmaMobil Android'
def p(t='',style=None):return d.add_paragraph(t,style)
def h(t):d.add_heading(t,1)
def h2(t):d.add_heading(t,2)
def page(t):d.add_page_break();h(t)
def blank(label,height):
 p(label,'Caption')
 para=p('');para.paragraph_format.keep_with_next=True
 para.paragraph_format.space_before=Pt(height*28.346/2)
 para.paragraph_format.space_after=Pt(height*28.346/2)
 para.paragraph_format.line_spacing=1
 para.paragraph_format.space_after=Pt(height*28.346/2)
 # Blank editable paragraph reserves space without inserting a fake screenshot.
 pr=para._p.get_or_add_pPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'F5F6F8');pr.append(sh)
def field(label,lines=1):
 pp=p();pp.add_run(label+' ').bold=True;pp.add_run('________________________________________________')
 for _ in range(lines-1):p('________________________________________________________________')
def table(headers,rows,widths=None):
 t=d.add_table(rows=1,cols=len(headers));t.autofit=False
 if widths:
  for col,w in zip(t.columns,widths):col.width=Cm(w)
 for c,txt in zip(t.rows[0].cells,headers):c.text=txt
 for row in rows:
  for c,txt in zip(t.add_row().cells,row):c.text=txt
 for i,row in enumerate(t.rows):
  for j,c in enumerate(row.cells):
   if widths:c.width=Cm(widths[j])
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=c._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
   pr.append(borders)
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6F1' if i==0 else ('FFFFFF' if i%2 else 'F5F7FA'));pr.append(sh)
   for para in c.paragraphs:
    para.paragraph_format.space_before=Pt(5);para.paragraph_format.space_after=Pt(5)
    for run in para.runs:run.font.size=Pt(10);run.bold=i==0
  trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
 return t

p('Validación de sesión JWT en PharmaMobil Android','Title')
p('Actividad autónoma 10','Subtitle')
p('Desarrollo de Aplicaciones Móviles')
p('Este informe organiza la validación de expiración, almacenamiento y cierre de sesión de PharmaMobil sobre PharmaSoft. Incluye la bitácora de seis escenarios, tres comprobaciones de almacenamiento, cuatro efectos del cierre y una matriz de permisos con tres usuarios. Los campos de resultados se completan con la ejecución real en Android.')
h('1 Entorno y preparación')
field('Fecha de ejecución');field('Emulador y versión de Android');field('Rama del repositorio');field('Enlace a la rama')
p('Preparación: iniciar Oracle y PharmaSoft, ejecutar PharmaMobil en debug y abrir Pruebas Sesion 10. Desde el emulador, la dirección del backend es http://10.0.2.2:8080. La bitácora conserva la fecha en UTC; indicar la zona horaria usada al transcribirla.')
table(['Usuario','Rol','Acceso principal'],[['admin','ADMIN','Todos los permisos'],['vendedor','VENDEDOR','Catálogo de lectura, clientes y ventas'],['almacen','ALMACENERO','Catálogo de lectura y escritura']],[3,4,10])
h2('Organización de evidencias')
p('Cada escenario requiere código HTTP recibido, mensaje literal del campo message, observación de la interfaz y captura. Un resultado esperado no sustituye el resultado observado. No incluir tokens completos ni contraseñas en las capturas.')
p('La evidencia se obtiene desde el propio proyecto. Ante un fallo, registrar el hallazgo y el commit de la corrección. Las conclusiones se redactan después de observar cada prueba.')

scenarios=[
('Token válido','Iniciar sesión y ejecutar una operación permitida, como listar productos. En el panel, pulsar 1 Token valido.','200 y operación completada.','No requiere modificación temporal del backend.'),
('Token expirado','Configurar app.jwt.expiracion-minutos en 1 en el perfil dev, reiniciar el backend, iniciar una sesión nueva y esperar más de 60 segundos. Pulsar 2 Token expirado.','401. Mensaje esperado de la guía: El token ha expirado. Inicie sesión nuevamente.','Restaurar expiracion-minutos a 60 y reiniciar al finalizar.'),
('Token alterado','Iniciar sesión y pulsar 3 Token alterado. La herramienta cambia un carácter del token guardado, limpia la caché Bearer y consulta productos.','401. Mensaje esperado de la guía: El token no es válido.','La sesión inválida debe eliminarse. Iniciar sesión de nuevo para continuar.'),
('Sin cabecera','Con una sesión previamente utilizada, pulsar 4 Sin cabecera. Se cierra la sesión y se consulta la ruta protegida con el mismo cliente HTTP, sin token.','401. Mensaje esperado de la guía: Debe iniciar sesión para acceder a este recurso.','Comprobar que no permanece el token ni en el almacén ni en la caché.'),
('Prefijo incorrecto','Iniciar sesión y pulsar 5 Prefijo bearer minuscula. La petición de diagnóstico envía bearer en minúscula en lugar de Bearer.','401. El backend del proyecto trata la petición como anónima.','Registrar el mensaje literal recibido, no asumir que coincide sin verificarlo.'),
('Usuario deshabilitado','Iniciar sesión como almacen. Con la sesión abierta, cambiar estado a false en Oracle y confirmar el cambio. Sin repetir el login, pulsar 6 Usuario deshabilitado.','401. Mensaje esperado de la guía: El usuario está deshabilitado.','Reactivar al usuario con estado = true y confirmar el cambio al terminar.')]
for i,(name,steps,expected,restore) in enumerate(scenarios,1):
 page(f'2 Bitácora escenario {i} {name}')
 field('Fecha y hora con zona horaria');p('Plataforma: Android');field('Usuario y rol')
 h2('Procedimiento');p(steps);p('Resultado esperado: '+expected)
 field('Pasos adicionales o datos usados',2)
 field('Código HTTP recibido');field('Mensaje literal del campo message',2)
 field('Qué vio el usuario en pantalla',2)
 if i in (2,6):field('La app detectó la invalidación y volvió al login Sí o No')
 blank(f'Figura {i} Evidencia Android del escenario {i}',6)
 field('Conclusión propia',2);field('Commit de corrección si corresponde')
 p('Restauración o control: '+restore)

page('3 Evidencia del almacenamiento seguro')
p('Las tres comprobaciones son independientes y requieren captura propia.')
h2('3 1 Archivo cifrado')
p('Inspeccionar Device Explorer: data/data/pe.edu.upeu.pharmamobile/shared_prefs/sesion_segura.xml. Las claves y valores del token deben estar cifrados.')
blank('Figura 7 Archivo del almacén cifrado en Android',3.2);field('Resultado observado')
h2('3 2 Registro sin filtración del token')
p('En Logcat filtrar message:KTOR y recargar Productos con sesión activa. Authorization debe mostrarse saneada con asteriscos, sin el JWT completo.')
blank('Figura 8 Authorization saneada en Logcat',3.2);field('Resultado observado')
h2('3 3 Persistencia después de reabrir')
p('Iniciar sesión, cerrar completamente la app sin pulsar Cerrar sesión y volver a abrirla antes del vencimiento. Debe recuperar la identidad sin pedir credenciales.')
blank('Figura 9 Sesión recuperada al reabrir Android',3.2);field('Resultado observado')

page('4 Verificación del cierre de sesión completo')
p('Ejecutar los cuatro controles en este orden. Cerrar sesión implica borrar la credencial, olvidar la caché y limpiar la interfaz.')
checks=[('Token eliminado del almacén','Inspeccionar el archivo antes y después. La entrada JWT debe desaparecer; pueden permanecer metadatos del cifrado.'),('Cliente HTTP sin token en caché','Después de una petición válida, cerrar sesión y lanzar Sin cabecera. La siguiente petición protegida debe salir sin Authorization y recibir 401.'),('Estado de interfaz limpio','El login no debe mostrar el usuario, la contraseña ni datos de la sesión anterior.'),('Sin regreso a una pantalla autenticada','Pulsar Atrás de Android después del cierre. No debe volver al listado autenticado.')]
for n,(title,how) in enumerate(checks,1):
 h2(f'4 {n} {title}');p(how);field('Resultado observado y referencia de captura')
blank('Figura 10 Almacén después de cerrar sesión',4)
blank('Figura 11 Petición sin token y login limpio después del cierre',4)
field('Conclusión sobre los cuatro efectos',2)

page('5 Matriz de permisos por rol')
p('Completar las 18 celdas con dos datos: HTTP real y si la interfaz ofrecía la acción en modo normal. Usar el modo sondeo solo para obtener respuestas de operaciones que normalmente se ocultan.')
ops=['Listar productos','Registrar producto','Listar clientes','Registrar venta','Ver reportes','Consultar auth me']
table(['Operación','admin','vendedor','almacen'],[[op,'HTTP: ____\nOfrecida: ____','HTTP: ____\nOfrecida: ____','HTTP: ____\nOfrecida: ____'] for op in ops],[5.2,3.9,3.9,4])
p('Ofrecida: Sí o No. Para registrar productos o ventas, usar IDs existentes y datos válidos. Un error de validación o negocio no sustituye la respuesta esperada de una operación autorizada. Los registros y las ventas crean datos reales.')
blank('Figura 12 Evidencia de la matriz con admin',2.8)
blank('Figura 13 Evidencia de la matriz con vendedor',2.8)
blank('Figura 14 Evidencia de la matriz con almacen',2.8)
field('Hallazgos de permisos o diferencias con la interfaz',2)

page('6 Conclusiones y control de entrega')
h2('Conclusiones')
field('Comportamiento frente a tokens inválidos o expirados',3)
field('Protección del token y persistencia',3)
field('Cierre de sesión y permisos por rol',3)
h2('Restauración del entorno')
p('☐ Se restauró app.jwt.expiracion-minutos a 60 y se reinició PharmaSoft.')
p('☐ Se reactivó el usuario deshabilitado con estado = true y se confirmó el cambio.')
p('☐ Se ocultaron tokens y datos sensibles en todas las capturas.')
h2('Repositorio y comprobación final')
field('Enlace a la rama');field('Commits de implementación y correcciones',2)
p('☐ Seis escenarios con HTTP, message literal, pantalla, captura y conclusión.')
p('☐ Tres comprobaciones de almacenamiento seguro con captura.')
p('☐ Cuatro efectos del cierre de sesión verificados.')
p('☐ Matriz de seis operaciones con los tres usuarios, HTTP y acción ofrecida.')
p('☐ Enlaces a la rama y commits accesibles.')
p('☐ Documento revisado y exportado como S10_ActividadAutonoma_Apellidos.pdf.')
p('Entrega indicada por la actividad: lunes 19 de octubre de 2026, hasta las 23:59 de Lima, en el aula virtual. Adjuntar el PDF y el enlace a la rama en el comentario.')
p('Referencia: Actividad Autónoma 10 Validación de expiración, almacenamiento y cierre de sesión, Desarrollo de Aplicaciones Móviles, sesión del 13 de octubre de 2026.')
d.save(out)
with ZipFile(out) as z:
 assert z.testzip() is None
 assert not any(n.startswith('word/media/') for n in z.namelist())
text='\n'.join(pp.text for pp in d.paragraphs)
assert 'iOS' not in text and 'IOS' not in text
assert d.core_properties.author==''
assert sum(1 for pp in d.paragraphs if pp.text.startswith('Figura '))==14
print(out.resolve());print('14 espacios de capturas; seis escenarios; matriz de 18 celdas; sin datos del estudiante.')
