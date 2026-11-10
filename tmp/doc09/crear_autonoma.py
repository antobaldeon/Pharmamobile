from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
D=Document(); sec=D.sections[0];sec.page_height=Cm(29.7);sec.page_width=Cm(21);sec.top_margin=sec.bottom_margin=Cm(2);sec.left_margin=sec.right_margin=Cm(2.2)
for n in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 st=D.styles[n];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
D.styles['Normal'].font.size=Pt(11);D.styles['Normal'].paragraph_format.space_after=Pt(7)
D.styles['Normal'].paragraph_format.line_spacing=1.12
D.styles['Title'].font.size=Pt(23)
D.styles['Heading 1'].font.size=Pt(16)
D.styles['Heading 2'].font.size=Pt(12)
D.core_properties.title='Informe de capacidades nativas en PharmaMobil';D.core_properties.subject='Sesión 09 expect actual y compartir productos';D.core_properties.author=''
def p(t):D.add_paragraph(t)
def h(t):D.add_heading(t,level=1)
def sub(t):D.add_heading(t,level=2)
def bullet(t):D.add_paragraph(t,style='List Bullet')
def code(t):
 r=D.add_paragraph().add_run(t);r.font.name='Consolas';r.font.size=Pt(9)
def page():D.add_page_break()
def table(headers,rows,widths=None):
 t=D.add_table(rows=1, cols=len(headers));t.autofit=False
 for i,x in enumerate(headers):t.rows[0].cells[i].text=x
 for row in rows:
  cells=t.add_row().cells
  for i,x in enumerate(row):cells[i].text=x
 for ri,row in enumerate(t.rows):
  for i,c in enumerate(row.cells):
   if widths:c.width=Cm(widths[i])
   pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
   pr.append(b)
   margins=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'90');e.set(qn('w:type'),'dxa');margins.append(e)
   pr.append(margins)
   if ri==0:
    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E7EDF2');pr.append(sh)
   for pp in c.paragraphs:
    pp.paragraph_format.space_after=Pt(3)
    for r in pp.runs:r.font.size=Pt(10);r.bold=ri==0
  trpr=row._tr.get_or_add_trPr();ns=OxmlElement('w:cantSplit');trpr.append(ns)
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
def evidence(title,description):
 sub(title);p(description)
 pp=D.add_paragraph('[Insertar captura aquí]');pp.paragraph_format.space_after=Pt(55);pp.runs[0].italic=True
 p('Dispositivo y versión del sistema: ____________________')
 p('Resultado observado: ______________________________________________')
D.core_properties.title='Actividad autónoma 09 de PharmaMobil'
D.add_paragraph('Actividad autónoma 09 de PharmaMobil',style='Title')
D.add_paragraph('Diferencias de implementación entre Android e iOS',style='Subtitle')
p('Desarrollo de Aplicaciones Móviles | Ciclo VI | Semestre 2026 2')
p('Estudiante: __________________________________________________')
p('Integrante de apoyo: ___________________________________________')
p('Docente: Mg. Reyna Barreto Benjamin David')
p('Fecha: 6 de octubre de 2026')
p('Rama: feature/expect-actual')
p('Repositorio: https://github.com/antobaldeon/Pharmamobile')
p('Enlace a la rama: https://github.com/antobaldeon/Pharmamobile/tree/feature/expect-actual')
h('1 Propósito y alcance')
p('Esta actividad documenta las capacidades nativas incorporadas a PharmaMobil y explica por qué Android e iOS requieren implementaciones distintas. Se incluyen el inventario, el análisis comparativo, la tercera capacidad de información del dispositivo y las secciones para completar las evidencias de Android.')
p('La compilación debug de Android y las pruebas automatizadas de shared finalizaron con BUILD SUCCESSFUL. Las capturas se incorporarán después de ejecutar la aplicación. El código de iOS está implementado, pero no se ha compilado ni ejecutado en macOS; por ello no se presentan resultados observados ni capturas de esa plataforma.')
h('2 Capacidades incorporadas')
bullet('Formato de moneda peruana mediante formatearSoles con expect y actual.')
bullet('Compartir nombre, precio y stock mediante Compartidor y sus implementaciones nativas.')
bullet('Mostrar sistema operativo y versión mediante InfoDispositivo en la pantalla Acerca de.')
p('El README contiene la sección Código específico de plataforma. El informe conserva la comparación técnica de iOS, aunque sus evidencias de ejecución quedan pendientes.')
page();h('3 Inventario de capacidades nativas')
p('Base de las rutas: shared/src/<source set>/kotlin/pe/edu/upeu/pharmamobile/. Cada ruta indicada se completa con commonMain, androidMain o iosMain según corresponda.')
sub('Formato de moneda')
code('expect fun formatearSoles(valor: Double): String')
p('commonMain: platform/Formato.kt. Android actual: androidMain/platform/Formato.android.kt, con java.text.NumberFormat y java.util.Locale. iOS actual: iosMain/platform/Formato.ios.kt, con NSNumberFormatter, NSLocale y moneda PEN.')
sub('Información del dispositivo')
code('expect class InfoDispositivo() {\n    val sistema: String\n    val version: String\n}')
p('commonMain: platform/InfoDispositivo.kt. Android actual: androidMain/platform/InfoDispositivo.kt; sistema Android y versión Build.VERSION.RELEASE. iOS actual: iosMain/platform/InfoDispositivo.kt; UIDevice.currentDevice.systemName y systemVersion.')
sub('Identificación de plataforma heredada')
code('expect fun getPlatform(): Platform')
p('commonMain: Platform.kt. Android actual: androidMain/Platform.android.kt, con Build.VERSION.SDK_INT. iOS actual: iosMain/Platform.ios.kt, con UIDevice.systemName y systemVersion. Esta función existe junto a la nueva capacidad; Acerca de utiliza InfoDispositivo.')
sub('Módulo de inyección')
code('expect val platformModule: Module')
p('commonMain: di/AppModule.kt. Android actual: androidMain/di/PlatformModule.android.kt; registra OkHttp y CompartidorAndroid con androidContext. iOS actual: iosMain/di/PlatformModule.ios.kt; registra Darwin y CompartidorIos. module pertenece a Koin; las dependencias registradas varían por plataforma.')
sub('Dirección del backend')
code('expect val backendBaseUrl: String')
p('commonMain: di/AppModule.kt. Actual en di/PlatformModule.android.kt y di/PlatformModule.ios.kt. Android usa http://10.0.2.2:8080/; iOS usa http://localhost:8080/. Son valores de configuración para emulador y simulador, sin API nativa adicional.')
sub('Compartir producto mediante interfaz')
code('interface Compartidor { fun compartir(texto: String) }')
p('Contrato: commonMain/domain/platform/Compartidor.kt. Android: androidMain/platform/CompartidorAndroid.kt, con Intent.ACTION_SEND. iOS: iosMain/platform/CompartidorIos.kt, con UIActivityViewController. No es una declaración expect: las implementaciones se seleccionan mediante Koin.')
page();h('4 Informe comparativo')
essay=[
('Formato de moneda en ambas plataformas','En PharmaMobil, commonMain/platform/Formato.kt declara formatearSoles y cada plataforma aporta su actual. Android utiliza NumberFormat.getCurrencyInstance con Locale es PE, mientras iOS configura NSNumberFormatter con NSLocale es_PE y currencyCode PEN. La región representa la misma intención, pero las bibliotecas y sus datos regionales pertenecen a entornos diferentes. Por ello pueden variar los espacios, el símbolo o los separadores según el sistema y su versión. Para comparar correctamente se debe utilizar el mismo producto y precio. ProductoUi.toUi prepara precioFormateado antes de dibujar la pantalla; Producto conserva precio como Double. El resultado literal de Android se registrará junto a su captura. El resultado de iOS permanece pendiente de ejecución; no se atribuye a Foundation una salida que no ha sido observada.'),
('Context de Android y controlador de iOS','CompartidorAndroid recibe Context en su constructor porque necesita solicitar al sistema que inicie una actividad. PlatformModule.android.kt obtiene androidContext de Koin; MainApplication lo registra al inicializar la aplicación. La clase crea un Intent ACTION_SEND, agrega el texto con EXTRA_TEXT y abre un selector. Como el contexto corresponde a la aplicación, el selector incluye FLAG_ACTIVITY_NEW_TASK. CompartidorIos no recibe Context porque UIKit organiza la presentación mediante ventanas y controladores. La implementación busca una UIWindowScene activa, una ventana principal y el controlador visible para presentar UIActivityViewController. Además configura el popover para iPad. Ambos lados necesitan un punto de acceso al entorno nativo; la diferencia es el modelo de componentes y cómo se obtiene ese acceso. La ausencia de Context en iOS no implica ausencia de dependencias del sistema.'),
('Expect actual e inyección de dependencias','El formato usa expect/actual porque expone una utilidad pequeña que debe estar disponible con la misma firma en todos los destinos. El compilador vincula cada declaración con su implementación. Si se reemplazara por una interfaz FormateadorMoneda, sería necesario crear implementaciones y registrarlas en Koin, además de inyectarlas en quienes preparan los datos. Esa alternativa facilitaría sustituir el formato en pruebas y permitiría recibir dependencias por constructor, a cambio de más elementos que configurar. Compartidor ya aplica esta estrategia porque Android necesita Context y una prueba puede usar un compartidor falso. DetalleProductoViewModel solicita el contrato y no conoce Intent ni UIKit. La elección del proyecto combina una función expect para el formato, una clase expect para información del dispositivo y una interfaz inyectada para compartir, según la complejidad de cada capacidad.'),
('Consecuencia de una implementación actual ausente','Si falta el actual requerido por el destino que se está compilando, la declaración expect no puede completarse y el compilador informa el problema. En este proyecto puede demostrarse comentando temporalmente formatearSoles en androidMain/platform/Formato.android.kt y ejecutando la tarea de compilación Android. El comentario debe abarcar la función completa y restaurarse después del experimento. Comentar únicamente el actual de iOS no demuestra el error mediante una compilación exclusiva de Android: la verificación debe corresponder al destino afectado. Esta entrega reserva un espacio para pegar el mensaje literal y su captura. Hasta ejecutar esa comprobación no se afirma un texto de error concreto. Tras restaurar el archivo debe repetirse la compilación para comprobar que el proyecto vuelve a quedar operativo.'),
('Lógica que debe permanecer en código común','Una regla concreta que debe seguir en commonMain es requiereReposicion de domain/model/Producto.kt, que considera bajo stock cuando la cantidad es menor o igual a cinco. El criterio depende del inventario y no de Android ni de iOS. También RegistrarProductoUseCase exige nombre, precio positivo y stock entero no negativo. Duplicar esas decisiones en los source sets permitiría que una plataforma aceptara productos que la otra rechaza y obligaría a mantener dos versiones de la misma regla. Lo que debe separarse es el acceso a APIs exclusivas del sistema, como Build, UIDevice y los mecanismos de compartir. AcercaScreen consulta InfoDispositivo sin importar esas APIs. Esta separación permite reutilizar las reglas, conservar la interfaz común y concentrar las diferencias técnicas en implementaciones nativas identificables.')]
for title,body in essay:sub(title);p(body)
print('Palabras del análisis:',sum(len(body.split()) for _,body in essay))
page();h('5 Tercera capacidad y validación')
sub('Información del dispositivo en Acerca de')
p('Se creó InfoDispositivo como clase expect con las propiedades sistema y version. Los dos actual tienen el mismo paquete y firma, pero utilizan fuentes distintas: Build.VERSION.RELEASE en Android y UIDevice en iOS. No se trata de devolver un valor fijo común a ambas plataformas.')
p('presentation/acerca/AcercaScreen.kt crea la información con remember y muestra sus propiedades. App.kt agrega el destino Acerca de al menú y a los diseños de navegación existentes. navigation/screen.kt declara Screen.Acerca. La capacidad está conectada a la interfaz y puede abrirse desde la aplicación.')
sub('Verificación automatizada realizada')
code('gradlew.bat :androidApp:assembleDebug\n            :shared:testAndroidHostTest --console=plain')
p('Resultado: BUILD SUCCESSFUL. La verificación cubrió compilación Android y pruebas automatizadas. No acredita por sí sola que se haya abierto el selector en un dispositivo. La revisión de commonMain no encontró importaciones nativas android. ni platform.; las importaciones del paquete propio pharmamobile.platform corresponden a contratos comunes.')
sub('Procedimiento para obtener el error de compilación')
bullet('Guardar el contenido de Formato.android.kt y comentar temporalmente la función actual completa.')
bullet('Ejecutar gradlew.bat :shared:compileAndroidMain --console=plain.')
bullet('Copiar el mensaje literal y capturar la consola con el archivo y error visibles.')
bullet('Restaurar la función y ejecutar nuevamente la compilación antes de guardar los cambios.')
sub('Mensaje literal obtenido')
p('[Pegar aquí el mensaje real del compilador después del experimento]')
sub('Resultado literal del formato Android')
p('Producto utilizado: ____________________  Precio numérico: __________')
p('Texto exacto mostrado en Android: __________________________________')
p('Dispositivo y versión de Android: ___________________________________')
p('iOS: implementación presente; resultado literal y ejecución pendientes en macOS con Xcode.')
page();h('6 Evidencias de Android')
evidence('Figura 1 Precio formateado en Android','Abrir Productos y capturar el listado con nombre y precio en soles. Utilizar el producto indicado en la sección de resultados literales.')
evidence('Figura 2 Compartir un producto en Android','Abrir Ver detalle y pulsar Compartir. Capturar el selector nativo; si el selector no muestra el contenido, añadir una captura del borrador en la aplicación receptora con nombre, precio y stock visibles.')
evidence('Figura 3 Información del dispositivo en Android','Abrir Acerca de y capturar el sistema operativo y la versión mostrados por la nueva capacidad.')
page();h('7 Evidencia del compilador y repositorio')
evidence('Figura 4 Error por ausencia de actual','Insertar la captura real de la compilación Android con la implementación temporalmente comentada. Restaurar el código después de obtenerla.')
sub('Commits de la actividad autónoma')
p('Commit del inventario y README: _____________________________________')
p('Commit del informe comparativo: ____________________________________')
p('Commit de la tercera capacidad: _____________________________________')
p('Commit de las evidencias: ___________________________________________')
p('Verificación de publicación: abrir el enlace de la rama y confirmar que los commits de esta actividad estén disponibles. Los commits de la práctica anterior no sustituyen los nuevos cambios de la actividad autónoma.')
h('8 Conclusiones')
p('PharmaMobil comparte modelos, reglas y presentación, mientras separa las implementaciones que dependen del sistema operativo. La tercera capacidad muestra información del dispositivo desde un destino accesible en el menú. La compilación y las pruebas de Android fueron satisfactorias; las evidencias manuales se incorporarán en las secciones señaladas. La implementación de iOS debe verificarse posteriormente en macOS.')
h('9 Referencias y entrega')
p('Actividad Autónoma N.º 09, Diferencias por plataforma y evidencia en iOS y Android. Desarrollo de Aplicaciones Móviles, sesión del 6 de octubre de 2026.')
p('Guía Práctica de Laboratorio N.º 09, Capacidades nativas con expect/actual en PharmaMobil. Código fuente de PharmaMobil, rama feature/expect-actual.')
p('Completar nombre, resultados literales, capturas y enlaces de commits. Exportar como S09_ActividadAutonoma_Apellidos.pdf. Entrega en aula virtual hasta el 12 de octubre de 2026 a las 23:59, con el enlace de la rama en el comentario.')
p('Las evidencias de iOS siguen pendientes respecto de los requisitos de la actividad. Si las obtiene un compañero con Mac, registrar su nombre y el dispositivo utilizado.')
D.save('output/doc/S09_ActividadAutonoma_Editable.docx')
