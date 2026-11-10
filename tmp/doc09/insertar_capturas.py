from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
src=Path('output/doc/S09_ActividadAutonoma_Editable.docx')
d=Document(src)
# Retirar secciones de evidencia vacías y conservar el informe hasta la sección 6.
paras=list(d.paragraphs);start=next(i for i,p in enumerate(paras) if p.text=='6 Evidencias de Android')
for p in paras[start:]:
 p._element.getparent().remove(p._element)
for p in d.paragraphs:
 t=p.text
 if 'Las capturas se incorporarán después' in t:p.text=t.replace('Las capturas se incorporarán después de ejecutar la aplicación.','Se obtuvieron capturas reales del emulador Android el 9 de octubre de 2026.')
 if t.startswith('Producto utilizado:'):p.text='Producto utilizado: Dologran. Precio numérico: 2.50. Stock: 20.'
 if t.startswith('Texto exacto mostrado'):p.text='Texto exacto mostrado en Android: S/\u00a02.50 (espacio no separable U+00A0 entre el símbolo y el importe).'
 if t.startswith('Dispositivo y versión de Android:'):p.text='Emulador: sdk_gphone16k_x86_64. Android 17.'
 if '[Pegar aquí el mensaje real' in t:p.text='Expected formatearSoles has no actual declaration in module <commonMain> for JVM'
 if 'El resultado literal de Android se registrará' in t:p.text=t.replace('El resultado literal de Android se registrará junto a su captura.','Android mostró S/\u00a02.50 para Dologran, con espacio no separable después del símbolo.')
 if 'Hasta ejecutar esa comprobación no se afirma' in t:p.text=t.replace('Hasta ejecutar esa comprobación no se afirma un texto de error concreto.','La comprobación real produjo: Expected formatearSoles has no actual declaration in module <commonMain> for JVM.').replace('Esta entrega reserva un espacio para pegar el mensaje literal y su captura.','La salida original de consola se guarda en docs/evidencias_s09/04_error_actual.txt.')
for i,(name,title,caption) in enumerate([
('01_precio_android.png','6 Precio formateado en Android','Dologran aparece con precio S/ 2.50 y stock 20. Captura directa del emulador.'),
('02_compartir_android.png','7 Compartir producto en Android','El selector nativo muestra Dologran — S/ 2.50 — Stock: 20. Se comprobó la apertura; no se envió el mensaje a un destinatario.'),
('03_acerca_android.png','8 Información del dispositivo en Android','La pantalla Acerca de muestra sistema operativo Android y versión 17.')]):
 if i:d.add_page_break()
 d.add_heading(title,1)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.add_run().add_picture(str(Path('docs/evidencias_s09')/name),height=Cm(18))
 d.add_paragraph(caption)
 d.add_paragraph('Dispositivo: sdk_gphone16k_x86_64 | Android 17 | Captura del 9 de octubre de 2026')
d.add_page_break();d.add_heading('9 Error real por ausencia de actual',1)
d.add_paragraph('Se retiró temporalmente la implementación Android de formatearSoles y se ejecutó gradlew.bat :shared:compileAndroidMain --console=plain. El compilador devolvió código 1. La implementación original fue restaurada inmediatamente después.')
log=Path('docs/evidencias_s09/04_error_actual.txt').read_text(encoding='utf-8',errors='replace')
lines=[s.strip() for s in log.splitlines() if s.strip()]
error=next(s for s in lines if 'Expected formatearSoles' in s)
p=d.add_paragraph();r=p.add_run(error);r.font.name='Consolas';r.font.size=Pt(9)
d.add_paragraph('Registro completo: docs/evidencias_s09/04_error_actual.txt. Este texto es la salida real guardada del compilador, no una captura visual de la terminal.')
d.add_heading('10 Repositorio y entrega',1)
d.add_paragraph('Rama: https://github.com/antobaldeon/Pharmamobile/tree/feature/expect-actual')
d.add_paragraph('Enlaces a los commits de esta actividad: __________________________________')
d.add_paragraph('El README incorpora el inventario en Código específico de plataforma. Completar nombre y enlaces de los nuevos commits antes de exportar a S09_ActividadAutonoma_Apellidos.pdf.')
d.add_paragraph('La implementación de iOS se mantiene pendiente de compilación y ejecución en macOS. Sus capturas no se incluyen en este documento.')
d.add_heading('11 Conclusión y referencias',1)
d.add_paragraph('Las capturas verifican en Android el precio formateado, la apertura del selector de compartir y la información del dispositivo. El error provocado confirma que la declaración expect requiere una implementación actual para el destino compilado. El archivo fue restaurado para mantener operativo el proyecto.')
d.add_paragraph('Referencia: Actividad Autónoma N.º 09 y Guía Práctica N.º 09 de Desarrollo de Aplicaciones Móviles, 6 de octubre de 2026. Código fuente de PharmaMobil.')
out=Path('output/doc/S09_ActividadAutonoma_ConCapturasAndroid.docx');d.save(out)
from zipfile import ZipFile
z=ZipFile(out);assert z.testzip() is None
print('Imágenes incrustadas:',len([n for n in z.namelist() if n.startswith('word/media/')]))
