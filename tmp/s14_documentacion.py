from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
import hashlib

root = Path(__file__).resolve().parents[1]
out = root / 'output/doc'
out.mkdir(parents=True, exist_ok=True)
tmp = root / 'tmp/s14-documentacion'
tmp.mkdir(exist_ok=True)
d = Document()
sec = d.sections[0]
sec.page_width = Cm(21.59); sec.page_height = Cm(27.94)
sec.top_margin = sec.bottom_margin = Cm(1.65)
sec.left_margin = sec.right_margin = Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
    s = d.styles[name]; s.font.name = 'Calibri'; s.font.color.rgb = RGBColor(0,0,0)
d.styles['Normal'].font.size = Pt(10.5)
d.styles['Normal'].paragraph_format.space_after = Pt(7)
d.styles['Normal'].paragraph_format.line_spacing = 1.06
d.styles['Title'].font.size = Pt(26)
d.styles['Heading 1'].font.size = Pt(17)
d.styles['Heading 2'].font.size = Pt(12)
d.styles['Caption'].font.size = Pt(9)
for n in d.styles['Title'].element.xpath('./w:pPr/w:pBdr'): n.getparent().remove(n)
d.core_properties.author = 'Tania Antonella Baldeon Ramirez'
d.core_properties.title = 'Builds firmados y validación de PharmaMobil sesión 14'
footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('PharmaMobil | Sesión 14 | Página ').font.size = Pt(8)
field = OxmlElement('w:fldSimple'); field.set(qn('w:instr'),'PAGE'); footer._p.append(field)
def p(text='', style=None): return d.add_paragraph(text, style)
def h(text): d.add_heading(text,1)
def sub(text): d.add_heading(text,2)
def page(title): d.add_page_break(); h(title)
def code(text):
    q=p(text)
    for r in q.runs: r.font.name='Consolas'; r.font.size=Pt(9)
def table(head, rows, widths, size=9):
    t=d.add_table(rows=1, cols=len(head)); t.autofit=False; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,w in enumerate(widths): t.columns[i].width=Cm(w)
    for c,v in zip(t.rows[0].cells,head): c.text=str(v)
    for vals in rows:
        for c,v in zip(t.add_row().cells,vals): c.text=str(v)
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr(); pr.append(OxmlElement('w:cantSplit'))
        if ri==0: pr.append(OxmlElement('w:tblHeader'))
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
            for edge in ['top','bottom','left','right']:
                e=OxmlElement('w:'+edge); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9'); borders.append(e)
            cp.append(borders); margins=OxmlElement('w:tcMar')
            for edge in ['top','bottom','left','right']:
                e=OxmlElement('w:'+edge); e.set(qn('w:w'),'85'); e.set(qn('w:type'),'dxa'); margins.append(e)
            cp.append(margins); shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'DCE6F1' if ri==0 else ('F5F7F9' if ri%2==0 else 'FFFFFF')); cp.append(shade)
            for q in c.paragraphs:
                q.paragraph_format.space_after=Pt(3); q.paragraph_format.line_spacing=1.03
                for r in q.runs: r.font.size=Pt(size); r.bold=ri==0
    p()
    return t

p('Builds firmados y validación de PharmaMobil','Title')
p('Informe de la práctica 14 y documentación de instalación','Subtitle')
p('Desarrollo de Aplicaciones Móviles\nUnidad 3  Proyecto de fin de curso')
p('\nUniversidad Peruana Unión\nFacultad de Ingeniería y Arquitectura\nEscuela Profesional de Ingeniería de Sistemas')
p('\nEstudiante: Tania Antonella Baldeon Ramirez\nCódigo: 202311724\nGrupo académico: 2\nCiclo VI  Semestre 2026 2')
p('Docente: Benjamin David Reyna Barreto\nFecha: 10 de noviembre de 2026')
sub('Resultado de la práctica')
p('Se regeneraron el APK y el AAB Android firmados de PharmaMobil, versión 1.0.0, con la IP actual de la laptop. Se verificó el certificado y aprobaron las 48 pruebas automatizadas. Se crearon las categorías faltantes y se corrigieron los avisos de reintento. Las fotografías finales acreditan sesión admin, listado con IDs del servidor y alta local sin red en un teléfono Android. El cierre declara las pruebas aún no acreditadas.')
p('Este informe reúne la configuración de firma, los archivos generados, las evidencias disponibles, la guía de instalación y los criterios que faltan para cerrar la entrega. La preparación Kotlin de iOS no equivale a una aplicación firmada o instalada en iPhone.')

page('Contenido y alcance')
table(['Sección','Página'], [('Firma y generación de builds','3'),('Guía de instalación y sesión','4'),('Evidencias de ejecución','5'),('Matriz de pruebas','6'),('Defectos y limitaciones','7'),('Checklist de entrega','8'),('Versión y trazabilidad','9'),('Actualizaciones verificadas','10'),('Evidencia sin conexión','11'),('Cierre de la práctica','12')],[14.5,3])
sub('Objetivo')
p('Empaquetar la aplicación existente, firmarla con un certificado propio y comprobar su comportamiento fuera del entorno de desarrollo. Se mantienen autenticación, roles, CRUD de productos, persistencia local, altas pendientes y sincronización manual.')
sub('Cierre del alcance')
table(['Elemento','Decisión'],[
('Firma Android y versión release','Implementado y verificado criptográficamente.'),
('Información de diagnóstico en Productos','Retirada de la interfaz por solicitud de la estudiante; se regeneraron los builds.'),
('Duración de sesión dev','Ampliada de 1 minuto a 8 horas en PharmaSoft; token verificado.'),
('Sincronización automática al recuperar red','Limitación declarada: se pulsa Sincronizar.'),
('Idempotencia de altas remotas','Limitación declarada: comprobar el servidor antes de reenviar un resultado incierto.'),
('Cámara y ubicación','Descartadas: no pertenecen al alcance del catálogo.'),
('iOS','Configuración preparada; enlace final, firma e instalación pendientes de macOS/Xcode.')],[5.4,12.1])
p('No se presenta el emulador como sustituto de los dispositivos físicos. Los resultados de compilación y firma se registran separados de las pruebas funcionales.')

page('Firma y generación de builds')
p('Se creó un almacén JKS fuera del repositorio, con alias pharmamobil, clave RSA de 2048 bits y vigencia de 10000 días. Las credenciales se leen desde keystore.properties y se excluyen de Git junto con los archivos .jks y .keystore. No se incluyen contraseñas ni la clave privada en esta documentación.')
table(['Propiedad','Valor'], [('Versión','1.0.0  |  versionCode 1'),('Identificador Android','pe.edu.upeu.pharmamobile'),('Titular','CN=Equipo PharmaMobil, OU=Desarrollo, O=PharmaMobil, L=Lima, C=PE'),('Vencimiento del certificado','28 de marzo de 2054'),('Optimización','Minificación habilitada  |  R8 9.1.29')],[5.2,12.3])
sub('Comandos de generación')
code('.\\gradlew.bat :androidApp:assembleRelease :androidApp:bundleRelease\n  -PpharmaBackendUrl=http://10.40.30.138:8080/\n  -PpharmaAllowHttp=true --console=plain')
p('Las líneas anteriores representan un único comando de Gradle. La opción HTTP se usa para el laboratorio local. La primera herramienta R8 mostró incompatibilidad con los metadatos Kotlin 2.4; se fijó R8 9.1.29 sin desactivar la minificación.')
sub('Verificación del certificado')
code('apksigner verify --verbose --print-certs <archivo.apk>\njarsigner -verify <archivo.aab>')
p('El APK verificó correctamente con esquema v2. El AAB devolvió jar verified; ambos contienen el mismo certificado. La salida de jarsigner conserva avisos sobre certificado autofirmado, timestamp y lectura ZIP; no sustituye una validación con bundletool ni la ejecución física.')
p('Huella SHA 256 del certificado')
code('E91E0751E2960BD3D6C6C61D09068464\nF121891968C9E28AFEE2C82A78574BBB')
p('La huella está dividida visualmente en dos líneas. Evidencias textuales: docs/s14/FIRMA_APK.txt, FIRMA_AAB.txt y CERTIFICADO_AAB.txt. Falta adjuntar la captura de pantalla solicitada de la verificación. El mapa de ofuscación se conserva localmente; su subida automática a Crashlytics está deshabilitada.')

page('Guía de instalación y sesión')
sub('Requisitos para otro usuario')
p('Un dispositivo Android 7 o posterior, el APK firmado y acceso por red a PharmaSoft. El AAB es el archivo de entrega para la tienda y no se instala directamente. PharmaSoft debe estar encendido con su base de datos disponible.')
for text in [
'1. Transferir Baldeon_ProyectoFinal_Android.apk al teléfono. Si llega comprimido, extraerlo primero.',
'2. Abrir el archivo y permitir la instalación desde esa fuente si Android lo solicita. Instalar y abrir PharmaMobil.',
'3. Si Android informa conflicto de firma con una instalación debug, no borrar datos por impulso. Usar un equipo de prueba o respaldar antes de cambiar de instalación.',
'4. Conectar teléfono y laptop a una red que permita comunicación entre ambos. Comprobar la IPv4 de Wi Fi de Windows con ipconfig.',
'5. Este APK apunta a http://10.40.30.138:8080/. Si cambia la IP de la laptop, regenerar el APK con la nueva dirección.',
'6. Abrir en Chrome del teléfono http://10.40.30.138:8080/api/v1/productos. Una respuesta 401 sin token confirma que ese endpoint es alcanzable desde el navegador.',
'7. Iniciar sesión con las credenciales de prueba facilitadas por la autora. No incluir contraseñas ni JWT en fotografías o registros.',
'8. Completar CRUD y validaciones. Para offline, iniciar primero con red, sincronizar, desactivar conectividad, crear un registro, recuperar red y pulsar Sincronizar.',
'9. Cerrar sesión y reabrir. Debe borrarse el token y el perfil de sesión; el catálogo local se conserva según la implementación actual.']: p(text)
sub('Duración de la sesión')
p('El perfil dev de PharmaSoft tenía expiración de un minuto. Se cambió app.jwt.expiracion-minutos al valor configurable ${JWT_EXPIRACION_MINUTOS:480}, se reinició el backend y se verificó que exp menos iat equivale a 28800 segundos, es decir, ocho horas.')
p('El cambio se aplica a nuevos inicios de sesión. Un token emitido antes del ajuste conserva su vencimiento original. No hace falta reinstalar el APK por este cambio del servidor. El perfil de producción no se modificó.')
sub('Si no se puede conectar')
p('Comprobar backend, dirección, puerto y acceso desde el teléfono. Si Chrome obtiene 401 pero la app falla, registrar el fallo y revisar Logcat del teléfono por USB. En el emulador, usar la variante debug con http://10.0.2.2:8080/; el APK físico usa la IP Wi Fi actual. No concluir que la contraseña sea incorrecta ni dar por resuelto el recorrido por una respuesta del navegador.')

page('Evidencias de ejecución')
p('Las fotografías finales corresponden a la aplicación funcionando en un teléfono Android. Se conserva la imagen original y se recorta únicamente el entorno para mejorar la lectura. No se modifican los datos ni los resultados visibles.')
t=d.add_table(rows=1,cols=2);t.autofit=False
for i,(name,box) in enumerate([('01_productos_sincronizados.png',(90,0,790,1260)),('02_edicion_producto.png',(155,0,790,1280))]):
    original=root/'docs/captura/s14'/name
    target=tmp/('final-'+name)
    with Image.open(original) as im: im.crop(box).save(target)
    with Image.open(target) as im: ratio=im.width/im.height
    cell=t.cell(0,i);cell.width=Cm(8.7)
    q=cell.paragraphs[0];q.alignment=WD_ALIGN_PARAGRAPH.CENTER
    q.add_run().add_picture(str(target),height=Cm(min(13.2,8.1/ratio)))
p('Figura 1 a la izquierda. Productos disponibles con ID del servidor: Paracetamol 1, chiquitolina 2 y hola 3. La captura acredita lectura de registros sincronizados; no demuestra por sí sola ausencia de duplicados.', 'Caption')
p('Figura 2 a la derecha. Sesión admin en Android y formulario de edición de hola con precio 12.3, stock 23 y categoría 2. Acredita la carga de los datos para editar; no confirma que se haya pulsado Guardar cambios ni su respuesta.', 'Caption')
sub('Resultados observables')
p('El bloqueo inicial de login ya no está presente en estas evidencias: se observa la sesión admin y el catálogo en el teléfono. Paracetamol y chiquitolina, que aparecían pendientes durante el diagnóstico, se muestran ahora con IDs positivos. La fotografía del modo avión se incluye en la página 11.')
p('Modelo y versión de Android no registrados. Las capturas muestran también textos con caracteres mal codificados; se declara este defecto visual en el cierre.')

page('Matriz de pruebas')
p('Se diferencia el emulador, la prueba parcial en Android físico y el segundo dispositivo requerido. Un paso pendiente no se marca como aprobado por estar implementado en el código.')
table(['Prueba','Emulador','Android físico','Segundo equipo'],[
('Instalación y apertura','Apertura observada','Apertura observada en foto','Pendiente'),
('Login correcto','Sesión admin observada','Sesión admin observada','Pendiente'),
('Login incorrecto','Sin evidencia actual','Pendiente','Pendiente'),
('Listado y alta sincronizada','Listado observado','IDs del servidor 1, 2 y 3 visibles','Pendiente'),
('Edición y eliminación','Sin evidencia completa','Edición cargada; guardado y eliminación pendientes','Pendiente'),
('Roles y rechazo HTTP 403','Sin evidencia completa','Pendiente de evidencia','Pendiente'),
('Lectura y alta en modo avión','Hay pruebas unitarias','Modo avión, catálogo y guardado local observados','Pendiente'),
('Recuperación y sincronización','Hay pruebas unitarias','Paracetamol y chiquitolina con ID positivo; falta secuencia completa','Pendiente'),
('Tres estados de notificaciones','Capturas previas S13; no release actual','Pendiente','Pendiente'),
('Cerrar sesión y reabrir','Sin evidencia del ciclo actual','Pendiente de evidencia','Pendiente'),
('Serialización e inyección release','Build correcto; ejecución no acreditada','Login y listado observados; resto pendiente','Pendiente')],[5.2,4.1,4.6,3.6],8.7)
sub('Pruebas automatizadas')
p('La suite Android Host ejecutó 48 pruebas con cero fallos, cero errores y cero omitidas. Incluye autenticación, mensajes de validación, persistencia local, migración SQLDelight, clasificación de permisos y reintentos de envío. Este resultado no sustituye el recorrido en el APK minificado.')
code('.\\gradlew.bat :shared:testAndroidHostTest --console=plain')
p('Reporte local: shared/build/reports/tests/testAndroidHostTest/index.html. La práctica solicita dos dispositivos reales y la actividad autónoma agrega un tercero. No se dispone de resultados completos que permitan cerrar esos criterios.')

page('Defectos y limitaciones')
sub('D01 Fallo de login en Android físico')
p('Dispositivo: Android físico, modelo y versión sin registrar. Severidad inicial: alta. Estado: cerrado para el bloqueo de acceso observado; la nueva figura 2 muestra la sesión admin activa.')
p('Pasos: 1. Instalar el APK firmado. 2. Abrir la app. 3. Introducir las credenciales de prueba. 4. Pulsar Ingresar. Resultado esperado: sesión iniciada y catálogo disponible. Resultado obtenido: No se pudo conectar con el servidor.')
p('Diagnóstico realizado: el navegador del teléfono alcanza el endpoint y obtiene 401 sin token; el backend también valida el login desde la laptop. Se revisó que el APK firmado incluye la IP de la laptop, INTERNET y HTTP habilitado. La primera incidencia física no cuenta con Logcat ni prueba de cierre. En un envío posterior se verificó que la IP Wi Fi de la laptop había cambiado; se corrigieron los builds y la configuración del emulador. Las figuras 1 y 2 ya acreditan sesión activa y listado en el teléfono; la figura 1 muestra los IDs definitivos de Paracetamol y chiquitolina. No se dispone del Logcat de la incidencia inicial. Ver las páginas 10 y 11.')
sub('D02 Sesión de desarrollo demasiado corta')
p('Severidad: media. Estado: corregido en configuración y verificado mediante token. La expiración se amplió de un minuto a ocho horas en el perfil dev. Falta corroborar la experiencia de uso prolongada en el teléfono; no se simularon ocho horas de ejecución.')
sub('Preparación de iOS')
p('Se configuraron versión 1.0.0, build 1, bundle ID estable, Team ID local, URL de backend, descripción de red local y dependencias nativas Firebase en Xcode. El código Kotlin iosArm64 compiló; Info.plist y las referencias internas del proyecto pasaron revisión estructural.')
p('La estudiante dispone de Windows y un iPhone 15 Pro Max con iOS 26.6 declarado. No se ejecutó Xcode, no se validó Swift ni el enlace final de los paquetes, no se firmó una app Apple y no se generó IPA o archivo Xcode. Se requiere acceso a macOS con Xcode y un equipo Apple real. La configuración Kotlin no se presenta como evidencia de instalación en iPhone.')
sub('Otras limitaciones declaradas')
p('La sincronización se inicia manualmente. Una respuesta perdida tras aceptar un POST puede producir duplicados al reenviar. El catálogo permanece local al cerrar sesión y no se ha definido aislamiento por usuario. Se requiere repetir las pruebas de permisos porque su bloque de prueba se retiró de Productos. El respaldo de la clave fuera de la laptop sigue pendiente.')

page('Checklist de entrega')
table(['Criterio','Estado'],[
('Alcance existente y limitaciones documentados','Documentado'),
('APK y AAB release generados con minificación','Verificado'),
('Firma y huella del certificado verificadas','Verificado en salida textual'),
('Captura de pantalla de la verificación de firma','Pendiente'),
('Clave y contraseñas fuera del repositorio','Verificado'),
('Respaldo seguro fuera de la laptop','Pendiente'),
('Debug compila sin credenciales de firma','Verificado'),
('Release bloquea la falta de credenciales','Verificado'),
('48 pruebas automatizadas sin fallos','Verificado'),
('Recorrido completo del APK minificado','Pendiente'),
('Dos dispositivos físicos durante la práctica','Pendiente'),
('Tercer dispositivo para la actividad autónoma','Pendiente'),
('Defectos con pasos gravedad y estado','Documentado'),
('iOS firmado o evidencia real de su proceso','Preparación y limitación documentadas; sin archivo'),
('Guía probada por un compañero','Pendiente'),
('Commit del código y etiqueta v1.0-final','Código registrado; etiqueta no creada')],[11.4,6.1])
sub('Uso de la guía por un compañero')
p('Entregar el APK y la sección de instalación. El compañero debe registrar fecha, dispositivo y resultado sin asistencia directa. No se consigna como validada esta actividad hasta recibir su prueba real.')
sub('Criterio de cierre')
p('Conservar la evidencia de cierre de D01, completar la matriz y la captura de firma, y respaldar la clave. Generar los archivos definitivos desde ese commit, verificar su firma y recién entonces etiquetar v1.0-final. Los builds se entregan el 16 de noviembre de 2026 y la sustentación es el 17.')

page('Versión y trazabilidad')
table(['Dato','Valor'], [('Android','pe.edu.upeu.pharmamobile'),('Versión y código','1.0.0 y 1'),('APK','Baldeon_ProyectoFinal_Android.apk'),('AAB','Baldeon_ProyectoFinal_Android.aab'),('Rama local','feature/builds-14'),('Commit del código','96b8d8dabd6aaec2e20b29672eb117c6729faf74'),('Etiqueta final','Pendiente; no creada')],[4.5,13])
p('Se usó Baldeon en los nombres de entrega por indicación de la estudiante. La rama se creó desde feature/integrador-13 porque no existía develop local. El código quedó registrado en el commit indicado; estas evidencias y el informe de cierre se incorporan después. La IP y la habilitación HTTP son parámetros de build documentados. No se crea la etiqueta final mientras existan criterios de entrega sin completar.')
sub('Hashes SHA 256 de los archivos actuales')
for ext in ['apk','aab']:
    f=root/f'output/android/s14/Baldeon_ProyectoFinal_Android.{ext}'
    digest=hashlib.sha256(f.read_bytes()).hexdigest().upper()
    p(f.name+'  |  '+f'{f.stat().st_size:,}'.replace(',',' ')+' bytes')
    code(digest[:32]+'\n'+digest[32:])
p('Estos hashes identifican archivos y son distintos de la huella del certificado. El mapa R8 se conserva junto a los builds para interpretar errores ofuscados.')
sub('Repositorio')
p('https://github.com/antobaldeon/Pharmamobile/tree/feature/builds-14')
p('Commit local del código\n96b8d8dabd6aaec2e20b29672eb117c6729faf74\nNo se ha confirmado su publicación en GitHub.')
sub('Referencias y evidencias')
p('Guía Práctica 14 Mejoras finales firma y generación de builds AAB e IPA, páginas 9 a 11. Diapositivas de sesión 14, páginas 9, 14, 17 y 18. Capturas aportadas por la estudiante durante esta sesión. Salidas locales de compilación y verificación conservadas en docs/s14 y tmp/s14-regenerar.log.')
p('Guías complementarias del proyecto: docs/s14/BUILD_E_INSTALACION.md y docs/s14/IOS_EN_IPHONE.md. Fecha de corte del informe: 10 de noviembre de 2026.')

page('Actualizaciones verificadas')
sub('D03 Categorías inexistentes y reintentos')
p('El servidor respondió HTTP 200 con lista vacía al consultar categorías. La creación del producto era rechazada porque referenciaba una categoría inexistente. A solicitud de la estudiante se crearon Medicamentos con ID 1 y Analgésicos con ID 2, ambas activas. No se borraron ni se duplicaron los productos locales pendientes.')
p('Se corrigió la presentación del bloqueo: un error permanente usaba el límite interno 5 como marca de detención, aunque no hubieran ocurrido cinco llamadas. Ahora se muestra Envío detenido y se ofrece Corregir producto. Al editar o volver a operar se limpian los avisos obsoletos; si el servidor vuelve a rechazar, se conserva el nuevo error real.')
p('Estado: corregido; la fotografía final muestra Paracetamol con ID del servidor 1 y chiquitolina con ID 2. Dos pruebas de regresión verifican el reenvío correcto y la edición sin perder los datos. La suite actual suma 48 pruebas sin fallos.')
sub('D04 Dirección de servidor desactualizada')
p('La IPv4 Wi Fi cambió de 172.17.26.38 a 10.40.30.138. La app seguía apuntando a la dirección anterior y el producto Chiquitolina quedó pendiente por falta de conexión. La dirección antigua agotó el tiempo de espera y la actual respondió HTTP 401 en el endpoint protegido.')
p('Se regeneraron y verificaron APK y AAB firmados con http://10.40.30.138:8080/. La variante debug se compiló por separado con http://10.0.2.2:8080/ y se instaló en el emulador conservando datos. Esta dirección especial del emulador no depende de la IPv4 Wi Fi. Estado: corregido para los productos observados; el teléfono muestra registros con ID definitivo. Si cambia otra vez la IP de la laptop, el APK físico requiere actualizar su configuración.')
sub('Cómo continuar sin duplicar registros')
p('Actualizar la instalación con el nuevo APK, sin desinstalar ni borrar datos. Mantener PharmaSoft encendido y el teléfono en una red que alcance la laptop. Para el producto pendiente, corregir el ID de categoría si corresponde y comprobar que no exista ya en el servidor antes de confirmar un único reenvío. No crear otra copia del mismo producto.')
p('Evidencia original: capturas aportadas de Paracetamol rechazado y Chiquitolina pendiente. Las nuevas fotografías confirman IDs definitivos para Paracetamol y chiquitolina. No se marca el recorrido completo como aprobado porque faltan otras operaciones y dispositivos. Logs de los ajustes: tmp/s14-corregir-reintentos.log y tmp/s14-cambio-ip.log. Los hashes de la página 9 corresponden a los archivos regenerados actuales.')

page('Evidencia sin conexión')
p('La tercera fotografía muestra el icono de modo avión, la sesión admin y datos del catálogo visibles. También muestra el mensaje Producto guardado y un envío fallido con un intento. Esto acredita conservación local y notificación del fallo de red; no acredita envío exitoso mientras el dispositivo está desconectado.')
img=root/'docs/captura/s14/03_alta_sin_conexion.png'
with Image.open(img) as im: im.crop((130,20,780,1260)).save(tmp/'offline-final.png')
q=p();q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q.add_run().add_picture(str(tmp/'offline-final.png'),height=Cm(14.8))
p('Figura 3. Alta local sin conexión y catálogo previamente guardado. La app conserva el registro y ofrece corregir o confirmar su reenvío. El ID local del nuevo registro no es visible en esta fotografía.', 'Caption')
p('La falta de conexión es deliberada en esta prueba. Al recuperar la red debe comprobarse el servidor antes de reenviar. La sincronización de este último registro aún no se acredita con una captura posterior.')

page('Cierre de la práctica')
sub('Resultados alcanzados')
p('Se entrega la documentación de PharmaMobil con APK y AAB Android firmados, certificado verificado, versión 1.0.0 y 48 pruebas automatizadas aprobadas. Las evidencias finales muestran una sesión admin en Android físico, catálogo con IDs positivos, apertura del formulario de edición y guardado local con modo avión.')
p('Los rechazos por categorías inexistentes se atendieron creando Medicamentos 1 y Analgésicos 2. Se corrigieron los mensajes persistentes de reintento y la dirección de red de los builds. Paracetamol y chiquitolina se observan posteriormente con IDs definitivos. La sesión dev se amplió a ocho horas y se comprobó mediante el token.')
sub('Aspectos que permanecen declarados')
p('No se cuenta con evidencia suficiente de eliminación, guardado final de la edición, rechazo por rol, cierre y reapertura de sesión, todos los estados de permisos ni ausencia de duplicados. El nuevo registro creado en modo avión requiere evidencia posterior de sincronización. No se acreditan un segundo y un tercer dispositivo físico, la captura visual de firma ni el respaldo de la clave fuera de la laptop.')
p('iOS queda con preparación y compilación Kotlin, sin archivo firmado o instalación, por falta de macOS/Xcode. La sincronización es manual y la idempotencia de POST sigue pendiente. Estos límites se conservan en la matriz y el checklist.')
sub('D05 Textos con caracteres incorrectos')
p('Severidad: baja. Estado: pendiente. En las fotografías se observan textos como Cancelar edición y Cerrar sesión con caracteres mal codificados, además del separador de precio y stock. No impide la lectura del catálogo, pero requiere corregir la codificación y volver a verificar la interfaz. No se presenta como resuelto.')
sub('Conclusión')
p('Se cierra este informe con evidencias reales de los avances y con las limitaciones identificadas. El producto Android ya dispone de builds distribuibles y pruebas físicas parciales. El cierre documental no equivale a aprobar criterios que todavía no se han demostrado; estos deben completarse antes de la entrega y sustentación.')
p('Evidencias finales conservadas en docs/captura/s14. La clave privada, sus contraseñas y los tokens no forman parte de este informe. Fecha de cierre documental: 10 de noviembre de 2026.')

path=out/'Baldeon_Tania_Sesion14_Documentacion_Final.docx' 
d.save(path)
print(path)
