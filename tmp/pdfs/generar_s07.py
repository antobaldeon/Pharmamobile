from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess, urllib.request, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'shared/src/commonMain/kotlin/pe/edu/upeu/pharmamobile'
stamp=datetime.now(ZoneInfo('America/Lima')).strftime('%d/%m/%Y %H:%M:%S (Lima)')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
try:
    with urllib.request.urlopen('http://127.0.0.1:8080/api/v1/productos?pagina=0&tamanio=20&ordenarPor=id&direccion=asc',timeout=3) as r:
        observed=f'HTTP {r.status}: '+r.read().decode()[:1500]
except Exception as e: observed=f'{type(e).__name__}: {e}'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Cover',fontSize=27,leading=33,textColor=colors.HexColor('#123c52'),spaceAfter=20))
styles.add(ParagraphStyle(name='SmallText',fontSize=8,leading=11))
styles.add(ParagraphStyle(name='CodeSmall',fontName='Courier',fontSize=7,leading=10))
styles['BodyText'].fontSize=10; styles['BodyText'].leading=15
styles['Heading1'].textColor=colors.HexColor('#123c52')
story=[]
def p(t,style='BodyText'): story.append(Paragraph(t,styles[style])); story.append(Spacer(1,8))
def title(t): p(t,'Heading1')
def table(head,rows,widths):
    vals=[[Paragraph(html.escape(str(x)),styles['SmallText']) for x in row] for row in [head]+rows]
    t=Table(vals,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dceef3')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#b6c9d0')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t);story.append(Spacer(1,12))
def code(text): story.append(Preformatted(text,styles['CodeSmall']));story.append(Spacer(1,10))
def page(): story.append(PageBreak())

p('UNIVERSIDAD PERUANA UNIÓN','Heading2');p('Desarrollo de Aplicaciones Móviles | Sesión 07','Heading3')
story.append(Spacer(1,35));p('Endpoints, DTO y pruebas de conexión','Cover')
p('Proyecto PharmaMobil','Heading1')
p('<b>Autoría:</b> Antonella Baldeon (nombre obtenido del último commit; confirmar nombre completo).')
p('<b>Fecha de elaboración:</b> '+stamp)
p('<b>Modalidad:</b> individual sobre el proyecto de pareja.')
p('<b>Repositorio:</b> https://github.com/antobaldeon/Pharmamobile')
p('<b>Rama:</b> feature/ktor-client')
p('<b>Commit del código analizado:</b> '+commit)
story.append(Spacer(1,25))
p('<b>Estado: documentación parcial verificable.</b> Se documenta el código existente. Las pruebas móviles, el JSON real del servidor y sus capturas permanecen pendientes. Este informe no constituye una entrega completa de la actividad.')
page();title('1. Catálogo de endpoints')
p('<b>Recurso principal:</b> productos. <b>URL base configurada:</b> http://10.0.2.2:8080/. <b>Versión:</b> v1, según la ruta api/v1/productos.')
p('10.0.2.2 corresponde al acceso al equipo anfitrión desde el emulador Android. La configuración compartida utiliza esa misma dirección; la conectividad iOS requiere revisión.')
p('El cliente implementa únicamente el listado paginado. Las otras cuatro rutas son propuestas para el CRUD y deben contrastarse con el contrato del backend. No se presentan como endpoints ejecutados.')
table(['Método / ruta','Parámetros','Respuesta / errores','Estado'],[
['GET /api/v1/productos','pagina=0; tamanio=20; ordenarPor=id; direccion=asc','PaginaProductosDto. Código HTTP y errores no verificados contra servidor.','Implementado; servidor no disponible'],
['GET /api/v1/productos/{id}','id en ruta','ProductoDto propuesto; 200 / 400 / 404 por confirmar.','Propuesto'],
['POST /api/v1/productos','Cuerpo JSON por confirmar','Creación; 201 / 400 por confirmar.','Propuesto; registro remoto no implementado'],
['PUT /api/v1/productos/{id}','id + cuerpo JSON por confirmar','Actualización; 200 / 400 / 404 por confirmar.','Propuesto'],
['DELETE /api/v1/productos/{id}','id en ruta','Eliminación; 200 o 204 / 404 por confirmar.','Propuesto']], [115,125,165,90])
p('<b>Paginación:</b> ProductoRepositoryImpl inicia pagina=0, acumula contenido y solicita páginas adicionales hasta que ultima sea true.')
title('Consulta implementada')
code((BASE/'data/remote/ProductoApi.kt').read_text(encoding='utf-8'))
page();title('2. Diccionario de DTO')
p('Los siete campos declarados son obligatorios, no anulables y no tienen valor por defecto. Los nombres JSON coinciden con los nombres Kotlin; no se usa @SerialName.')
table(['DTO / campo JSON','Tipo Kotlin','Obligatorio','Defecto','Correspondencia'],[
['ProductoDto.id','Long','Sí','Sin valor','Producto.id'],
['ProductoDto.nombre','String','Sí','Sin valor','Producto.nombre'],
['ProductoDto.precio','Double','Sí','Sin valor','Producto.precio'],
['ProductoDto.stock','Int','Sí','Sin valor','Producto.stock'],
['ProductoDto.estado','Boolean','Sí','Sin valor','Producto.activo'],
['PaginaProductosDto.contenido','List<ProductoDto>','Sí','Sin valor','Lista de Producto vía toDomain()'],
['PaginaProductosDto.ultima','Boolean','Sí','Sin valor','Control de paginación; sin campo de dominio']], [140,105,60,65,125])
title('Código de los DTO')
code((BASE/'data/remote/dto/ProductosDto.kt').read_text(encoding='utf-8'))
p('<b>JSON real:</b> pendiente. El servidor no respondió en la revisión local. No se incluye un JSON inventado como evidencia de respuesta.')
page();title('3. Bitácora de pruebas de conexión')
p('Los cinco escenarios siguientes son un protocolo pendiente de ejecución móvil. No se registran resultados observados ni capturas ficticias.')
table(['ID / escenario','Pasos y resultado esperado','Estado observado'],[
['P01 - Respuesta exitosa','Iniciar backend y app; abrir productos y recargar. Esperado: HTTP 200 y lista visible.','No ejecutado en Android/iOS; sin dispositivo conectado.'],
['P02 - Recurso inexistente','Confirmar ruta por ID; solicitar un ID inexistente. Esperado: 404, ClientRequestException y mensaje controlado.','Pendiente; cliente actual no tiene consulta por ID.'],
['P03 - Sin conexión','Activar modo avión antes de recargar. Esperado: excepción de E/S capturada y mensaje visible.','Pendiente; no se activó modo avión ni se ejecutó app.'],
['P04 - Timeout','Configurar temporalmente requestTimeoutMillis=1 y recargar; restaurar 15000. Esperado: HttpRequestTimeoutException y UI responsiva.','Pendiente; configuración original conservada.'],
['P05 - Campo desconocido','Usar una respuesta con campo extra no declarado en DTO; comparar ignoreUnknownKeys=true y false. Esperado: éxito con true y error de serialización con false.','Pendiente; no hay JSON real ni ejecución Ktor.']], [105,260,130])
p('<b>Para completar cada registro:</b> fecha y hora, Android o iOS, pasos exactos, resultado esperado, resultado observado, captura de pantalla y conclusión de una línea.')
p('<b>Mensajes de error actuales:</b> ProductoViewModel usa error.message o “No se pudieron cargar los productos”. No existen mensajes específicos por tipo de error en el código revisado; el mensaje real visible debe comprobarse en ejecución.')
title('Comprobación auxiliar real del entorno')
p('Fecha: '+stamp+'. Plataforma: Windows, equipo anfitrión. Esta comprobación no sustituye ninguna prueba móvil ni un registro de Ktor.')
p('Petición HTTP auxiliar: http://127.0.0.1:8080/api/v1/productos?pagina=0&amp;tamanio=20&amp;ordenarPor=id&amp;direccion=asc')
p('<b>Resultado observado:</b> '+html.escape(observed))
page();title('4. Evidencias y repositorio')
table(['Evidencia solicitada','Resultado de revisión / pendiente'],[
['Registro completo de Ktor','Logging usa LogLevel.HEADERS; no registra cuerpos completos. Pendiente ejecutar y capturar petición/respuesta completas.'],
['App ejecutada en Android','adb devices no encontró dispositivos conectados. Captura pendiente.'],
['App ejecutada en iOS','Hay código iosMain con motor Darwin. No se ejecutó simulador iOS; requiere macOS/Xcode. Captura pendiente.'],
['Repositorio','https://github.com/antobaldeon/Pharmamobile'],
['Rama','feature/ktor-client'],
['Commit del código documentado',commit],
['README','Se añadió sección Conectividad REST. La modificación local aún requiere commit y publicación.']], [160,335])
p('<b>Enlace al commit:</b> https://github.com/antobaldeon/Pharmamobile/commit/'+commit)
p('El hash se comprobó localmente. No se verificó accesibilidad remota del enlace. El PDF y la actualización del README no forman parte de ese commit previo.')
title('Evidencia de implementación: configuración Ktor')
p('Extracto literal de data/remote/HttpClientFactory.kt. Es evidencia del código, no captura de ejecución.')
code('''expectSuccess = true
Json {
    ignoreUnknownKeys = true
    isLenient = true
    encodeDefaults = true
}
level = LogLevel.HEADERS
install(HttpTimeout) {
    requestTimeoutMillis = 15_000
    connectTimeoutMillis = 10_000
}''')
page();title('5. Lista de cotejo y cierre')
table(['Requisito','Estado'],[
['PDF con portada','Generado; confirmar nombre completo de la estudiante.'],
['Cinco endpoints verificados','Pendiente: solo listado implementado, sin respuesta del backend.'],
['Todos los campos DTO','Documentados a partir del código.'],
['JSON real y código DTO','Código incluido; JSON real pendiente.'],
['Cinco pruebas con capturas','Pendientes.'],
['Mensaje visible por cada error','Pendiente verificación en app.'],
['Capturas Android e iOS','Pendientes.'],
['README Conectividad REST','Actualizado localmente.'],
['Commit accesible en rama requerida','Hash y rama comprobados localmente; publicación por comprobar.']], [335,160])
p('<b>Pasos para terminar:</b> iniciar el backend, revisar Swagger y confirmar el CRUD; ejecutar Android e iOS; registrar los cinco escenarios con sus capturas; insertar el JSON real y los registros completos; confirmar autoría; guardar y publicar el commit correspondiente.')
p('<b>Fuente de requisitos:</b> Actividad Autónoma N.º 07, Documentación de endpoints, DTO y pruebas de conexión, Universidad Peruana Unión, semestre 2026-2.')
p('<b>Alcance de revisión:</b> archivos Kotlin y repositorio local de PharmaMobil. No se alteró la lógica de la aplicación para simular resultados.')
def footer(c,d):
    c.setStrokeColor(colors.HexColor('#b6c9d0'));c.line(40,42,555,42)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#526775'));c.drawString(40,28,'PharmaMobil | Sesión 07 | Documentación parcial verificable');c.drawRightString(555,28,str(d.page))
dest=OUT/'S07_ActividadAutonoma_Baldeon.pdf'
SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=55,title='S07 - PharmaMobil: endpoints, DTO y pruebas',author='Antonella Baldeon').build(story,onFirstPage=footer,onLaterPages=footer)
print(dest)
