from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from zipfile import ZipFile

items=[
('521cc86e-bea5-4e59-bfe6-8b64b7abeb7b','Token expirado','2026-10-18T08:23:30.657489300','El token ha expirado. Inicie sesión nuevamente','La solicitud GET a la ruta protegida de productos, configurada con Bearer Token, recibió HTTP 401. El servidor identificó la expiración de la credencial.','El backend rechazó el token expirado e impidió acceder al listado de productos. Para continuar es necesario iniciar sesión nuevamente y obtener una credencial vigente.'),
('8f551101-c086-494a-a564-b41e033f84b6','Token inválido','2026-10-18T08:24:02.883091400','El token no es válido','La solicitud GET de productos recibió HTTP 401 con un mensaje que identifica el token como inválido. El campo del token se muestra oculto en Postman.','El backend rechazó la credencial inválida y mantuvo protegido el recurso. La captura acredita el rechazo; no permite identificar por sí sola qué carácter o parte del token se modificó.'),
('10216ad0-fec7-4d5a-8fdd-d8f28e3b7bbe','Solicitud sin autenticación reconocida','2026-10-18T08:31:27.519024600','Debe iniciar sesión para acceder a este recurso','La petición GET de productos muestra HTTP 401 Unauthorized. En la tabla visible de Headers no aparece una cabecera Authorization y el servidor solicita iniciar sesión.','La petición no fue reconocida como autenticada y no obtuvo acceso a los productos. El mensaje confirma que el recurso exige una sesión válida. La captura no muestra el contenido de los seis encabezados ocultos.'),
('c01eebb3-bbea-4392-82e6-a8a4369cca35','Prefijo bearer en minúscula','2026-10-18T08:39:14.629428800','Debe iniciar sesión para acceder a este recurso','En Headers aparece Authorization con el prefijo bearer en minúscula. La respuesta de la ruta protegida es HTTP 401 Unauthorized y solicita iniciar sesión.','En esta implementación, el prefijo bearer en minúscula no autentica la solicitud. El servidor la rechaza como anónima; debe utilizarse el esquema Bearer que reconoce el backend.')]
d=Document();s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7);s.top_margin=s.bottom_margin=Cm(1.6);s.left_margin=s.right_margin=Cm(1.8)
for n in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=d.styles[n];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0);st.paragraph_format.space_after=Pt(6)
d.styles['Normal'].font.size=Pt(10);d.styles['Normal'].paragraph_format.line_spacing=1.05
d.styles['Title'].font.size=Pt(24);d.styles['Heading 1'].font.size=Pt(16);d.styles['Caption'].font.size=Pt(9)
d.core_properties.author='';d.core_properties.last_modified_by='';d.core_properties.title='Validación de tokens JWT en PharmaSoft'
d.add_paragraph('Validación de tokens JWT en PharmaSoft','Title')
d.add_paragraph('Actividad autónoma 10 Evidencias del backend','Subtitle')
d.add_paragraph('Las cuatro pruebas documentadas recibieron HTTP 401 al consultar el recurso protegido de productos. Las respuestas distinguen entre token expirado, token inválido y solicitud sin autenticación reconocida. Las capturas corresponden a peticiones ejecutadas en Postman el 18 de octubre de 2026.')
d.add_heading('Resumen de resultados',1)
t=d.add_table(rows=1,cols=3)
for c,txt in zip(t.rows[0].cells,['Evidencia','HTTP','Resultado']):c.text=txt
for _,title,_,message,_,_ in items:
 for c,txt in zip(t.add_row().cells,[title,'401',message]):c.text=txt
for i,row in enumerate(t.rows):
 for c in row.cells:
  pr=c._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
  for edge in ['top','left','bottom','right']:
   el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
  pr.append(borders)
  if i==0:
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6F1');pr.append(sh)
   for r in c.paragraphs[0].runs:r.bold=True
  for p in c.paragraphs:p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(5)
d.add_heading('Conclusión general',1)
d.add_paragraph('Las respuestas observadas muestran que PharmaSoft no permite consultar productos con una credencial expirada, inválida o no reconocida. El código 401 mantiene protegido el recurso y el campo message diferencia la causa del rechazo. Estos resultados comprueban el control de autenticación del backend.')
d.add_heading('Alcance de las evidencias',1)
d.add_paragraph('Las imágenes muestran las respuestas de Postman. No acreditan por sí solas el regreso al login, la eliminación del token o la conservación del estado en la interfaz Android. Esas comprobaciones requieren evidencia adicional de la aplicación. Tampoco se incluye una operación protegida con token válido ni la prueba de usuario deshabilitado.')
d.add_paragraph('Recurso evaluado: GET http://localhost:8080/api/v1/productos. Las fechas de cada evidencia se transcriben del campo timestamp; la respuesta no indica zona horaria.')
for i,(ident,title,date,message,observation,conclusion) in enumerate(items,1):
 d.add_page_break();d.add_heading(f'{i} {title}',1)
 d.add_paragraph('Petición: GET http://localhost:8080/api/v1/productos')
 d.add_paragraph('Fecha y hora del servidor: '+date)
 d.add_paragraph('Código recibido: 401 Unauthorized')
 p=d.add_paragraph();p.add_run('Mensaje literal: ').bold=True;p.add_run(message)
 img=Path('C:/Users/tania/AppData/Local/Temp')/f'codex-clipboard-{ident}.png'
 assert img.exists(),img
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(img),height=Cm(16.0))
 d.add_paragraph(f'Figura {i} {title} en Postman','Caption')
 p=d.add_paragraph();p.add_run('Resultado observado. ').bold=True;p.add_run(observation)
 p=d.add_paragraph();p.add_run('Conclusión. ').bold=True;p.add_run(conclusion)
out=Path('output/doc/S10_ActividadAutonoma_ConEvidencias_Postman.docx');d.save(out)
with ZipFile(out) as z:assert z.testzip() is None;assert len([n for n in z.namelist() if n.startswith('word/media/')])==4
print(out.resolve())
