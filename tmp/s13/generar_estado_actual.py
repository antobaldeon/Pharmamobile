from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

root = Path(__file__).resolve().parents[2]
source = (root / 'docs/s13-autonoma/EVIDENCIAS.md').read_text(encoding='utf-8')
styles = getSampleStyleSheet()
styles['Normal'].fontSize = 10
styles['Normal'].leading = 14
styles['Normal'].spaceAfter = 8
styles['Heading1'].textColor = colors.HexColor('#164b58')
styles['Heading2'].textColor = colors.HexColor('#164b58')
styles['BodyText'].fontSize = 8
styles['BodyText'].leading = 11
story = []

def p(text, style='Normal'):
    text = escape(text.replace('`', ''))
    story.append(Paragraph(text, styles[style]))

def table(rows, widths):
    cells = [[Paragraph(escape(c.replace('`', '')), styles['BodyText']) for c in row] for row in rows]
    t = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e4eef0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#afc3c8')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

def rows(section):
    return [[c.strip() for c in line.strip().strip('|').split('|')] for line in section.splitlines()
            if line.startswith('|') and not re.match(r'^\|[\s:|-]+$', line)]

def page(title):
    story.append(PageBreak())
    p(title, 'Heading1')

def image(name, height):
    path = root / 'docs/captura/s13' / name
    img = Image(str(path))
    img.drawWidth *= height / img.drawHeight
    img.drawHeight = height
    story.append(img)

p('Actividad autónoma 13', 'Title')
p('Flujo completo y evidencias por plataforma', 'Heading1')
story.append(Spacer(1, 35))
p('PharmaMobil sobre PharmaSoft', 'Heading2')
p('Universidad Peruana Unión<br/>Desarrollo de Aplicaciones Móviles'.replace('<br/>', ' - '))
p('Estudiante: Tania Antonella Baldeon Ramirez')
p('Código: 202311724 | Grupo: 2 | Ciclo VI | Semestre 2026-2')
p('Docente: Benjamin David Reyna Barreto')
p('Fecha de revisión: 10 de noviembre de 2026')
story.append(Spacer(1, 35))
p('INFORME PARCIAL', 'Heading2')
p('Incluye el estado revisado del código y capturas previas del proyecto. El recorrido completo aún requiere ejecución y capturas. No se presenta como entrega final acreditada.')

page('Índice y verificación')
table([['Contenido', 'Página'], ['A. Primera apertura y operación', '3'], ['A. Sincronización y cierre', '4'], ['B. Plataformas', '5'], ['C. Permisos', '6'], ['D. Ficha de integración', '7'], ['Repositorio y cierre', '8']], [420, 84])
p('La actividad exige documentar diez pasos, comparar plataformas, registrar los estados de permisos y tomar decisiones sobre los huecos de integración.')
p('La implementación previa ya contiene almacenamiento seguro, autenticación, persistencia SQLDelight, altas pendientes, contadores, fecha de sincronización y permiso de notificaciones. Esta revisión no añade funcionalidades ajenas a la guía.')
verification = root / 'docs/s13-autonoma/VERIFICACION.md'
if verification.exists():
    for line in verification.read_text(encoding='utf-8').splitlines():
        if line.startswith('- '): p(line[2:])
p('Las pruebas automatizadas no sustituyen capturas de la aplicación. Las evidencias previas no se fechan como si fueran de esta revisión.')

flow = rows(source.split('## A.')[1].split('## B.')[0])
page('A. Primera apertura y operación')
table([flow[0]] + flow[1:6], [32, 302, 170])
p('Cada paso necesita una captura recortada y un pie con el estado observado. No mostrar JWT ni contraseñas. Usar una instalación de prueba sin borrar datos del dispositivo habitual.')
page('A. Sincronización, errores y cierre')
table([flow[0]] + flow[6:], [32, 302, 170])
p('La sincronización requiere pulsar Sincronizar. Antes de reenviar una petición cuyo resultado es incierto, comprobar en el servidor si el registro ya existe.')
p('La validación debe venir del servidor. Confirmar las restricciones vigentes antes del ensayo. En el vencimiento del token, consultar la duración real; un fallo de red no demuestra HTTP 401.')

page('B. Evidencias por plataforma')
table(rows(source.split('## B.')[1].split('## C.')[0]), [90, 207, 207])
p('Estado de iOS', 'Heading2')
p(source.split('### Límite de iOS\n\n')[1].split('## C.')[0].strip())

page('C. Bitácora de notificaciones')
permission_rows = rows(source.split('## C.')[1].split('## D.')[0])
table([r[:3] for r in permission_rows], [95, 195, 214])
imgs = []
for name in ['01_permiso_denegado.png', '02_permiso_permanente.png', '03_permiso_concedido.png']:
    img = Image(str(root / 'docs/captura/s13' / name))
    ratio = min(155 / img.drawWidth, 240 / img.drawHeight)
    img.drawWidth *= ratio
    img.drawHeight *= ratio
    imgs.append(img)
story.append(Table([imgs], colWidths=[168]*3))
p('Figuras 1 a 3. Capturas previas: denegado, denegado para siempre y concedido. No corresponden a una nueva ejecución del 10 de noviembre.', 'BodyText')
p('Falta registrar versión del sistema, texto del diálogo y número real de solicitudes. INTERNET es un permiso normal, sin diálogo. En Android anterior a 13, la recuperación de notificaciones deshabilitadas se realiza desde Ajustes.')

page('D. Ficha de integración')
table(rows(source.split('## D.')[1].split('## Repositorio')[0]), [110, 45, 65, 86, 198])
p('Las fechas indicadas como objetivo o revisión no acreditan que el hueco esté resuelto. El permiso está implementado; el recorrido nuevo y las capturas pendientes siguen abiertos.')

page('Repositorio y cierre')
for line in source.split('## Repositorio y entrega')[1].splitlines():
    if line.startswith('- '): p(line[2:])
p('Criterio para cerrar el informe', 'Heading2')
p('Completar las capturas de los diez pasos y sus estados, repetir los permisos, fundamentar iOS y actualizar el commit evaluado. Mantener identificada cualquier limitación. Después exportar con el nombre final solicitado.')
p('Referencia: Actividad Autónoma N.º 13, Documentar el flujo completo y las evidencias por plataforma. Guía proporcionada por la estudiante.')

out = root / 'output/pdf/Baldeon_Tania_Sesion13_Evidencias_EstadoActual.pdf'
out.parent.mkdir(parents=True, exist_ok=True)
def footer(canvas, doc):
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#52666b'))
    canvas.drawString(54, 32, 'PharmaMobil | Sesión 13 | Informe parcial | 10/11/2026')
    canvas.drawRightString(558, 32, str(doc.page))
SimpleDocTemplate(str(out), pagesize=letter, rightMargin=54, leftMargin=54, topMargin=45, bottomMargin=50,
                  title='PharmaMobil - Actividad autónoma 13 - Estado actual', author='Tania Antonella Baldeon Ramirez').build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
