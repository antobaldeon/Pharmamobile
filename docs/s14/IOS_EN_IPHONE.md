# Preparación para probar PharmaMobil en iPhone

Estado al 10/11/2026: la estudiante dispone de Windows y un iPhone 15 Pro Max con iOS 26.6 declarado. No dispone de Mac. El mínimo existente del proyecto es iOS 18.2, por lo que no se modificó.

## Qué quedó preparado

- Versión iOS `1.0.0`, build `1` y bundle ID estable `pe.edu.upeu.pharmamobile.PharmaMobil`. El Team ID ya no altera el identificador de la aplicación.
- Firma automática existente de Xcode, con Team ID configurable en un archivo local ignorado por Git.
- URL de PharmaSoft tomada de Info.plist, configurable sin editar Kotlin. `localhost` sirve para el simulador cuando el backend está en esa misma Mac; en un iPhone significa el propio teléfono y no alcanza la laptop Windows.
- Descripción del permiso de red local y ATS limitado a red local; no se habilitaron cargas inseguras globalmente.
- Enlace de FirebaseCore y FirebaseCrashlytics mediante Swift Package Manager. Se fijó el SDK iOS 11.8.0, correspondiente a los bindings de GitLive 2.7.0 ya usados por el proyecto, sin actualizar las bibliotecas compartidas.
- Inicialización de Firebase únicamente cuando existe el archivo iOS real `GoogleService-Info.plist`. Sin él, el módulo iOS desactiva la telemetría y conserva el catálogo, las notificaciones locales y la sincronización. El archivo Android no sirve como sustituto.

El código Kotlin para `iosArm64` compiló después de estos ajustes. Eso acredita la compilación de la biblioteca Kotlin; no valida Swift, el enlace final de Firebase, la firma Apple ni la instalación en el iPhone.

## Lo que necesita una Mac

La aplicación nativa requiere macOS con Xcode para enlazar, firmar e instalar. Windows y el iPhone por sí solos no completan ese proceso. No se generó un IPA ni se inventó un certificado Apple. Se necesita acceso a una Mac propia, prestada o remota con acceso al proceso de instalación. No se configuró ni contrató un servicio externo.

Cuando se disponga de esa Mac:

1. Copiar el proyecto con los cambios actuales. El commit base publicado no incluye los cambios locales. Instalar Xcode y un JDK compatible con Gradle (el proyecto usa JDK 21), y comprobar `JAVA_HOME`.
2. En la raíz, conceder permiso de ejecución a `gradlew` si fuera necesario: `chmod +x gradlew`. Abrir `iosApp/iosApp.xcodeproj`.
3. Copiar `iosApp/Configuration/Local.xcconfig.example` como `Local.xcconfig` en la misma carpeta. Completar `TEAM_ID` con el equipo real de Xcode y `PHARMA_BACKEND_HOST` con la IPv4 Wi-Fi de Windows. La IP observada fue `172.17.26.38`, pero debe comprobarse nuevamente con `ipconfig`.
4. En Xcode > Settings > Accounts, agregar la cuenta Apple en la propia Mac. En Signing & Capabilities, confirmar firma automática y equipo real. No enviar contraseña Apple ni claves al chat o al repositorio.
5. Resolver los paquetes SPM y comprobar el enlace nativo. Si se usará Firebase, registrar la aplicación iOS con el bundle ID real y agregar su `GoogleService-Info.plist` a `iosApp/iosApp/`; confirmar que pertenece al target. Sin ese archivo, la telemetría permanece desactivada.
6. Iniciar PharmaSoft en Windows. Mac, laptop e iPhone deben tener acceso a la misma red. Comprobar desde Safari del iPhone que `http://<IP-WINDOWS>:8080/` responde; un 404 del servidor confirma conectividad, un timeout no. La red puede aislar clientes y Windows puede bloquear el puerto.
7. Conectar el iPhone a la Mac, aceptar la confianza y habilitar Developer Mode si el sistema lo solicita. Seleccionar el iPhone físico en Xcode y ejecutar Run. Aceptar el acceso a red local cuando se solicite.
8. Si se deniega red local: Ajustes > Privacidad y seguridad > Red local > PharmaMobil. Habilitar y volver a intentar; documentar el mensaje real de la app. No registrar esa denegación como contraseña incorrecta.
9. Para la notificación local, conceder permiso, pulsar Probar notificación y enviar la app al fondo antes de los dos segundos programados. La visualización en primer plano no está implementada. En iOS, tras denegar notificaciones, la recuperación es desde Ajustes; no se presupone un segundo diálogo como en Android.
10. Completar login, CRUD, roles, modo avión, alta pendiente, recuperación de red, sincronización manual y cierre de sesión. Registrar capturas reales en el iPhone.

## Archivo de entrega

En la Mac, elegir un destino de dispositivo iOS (no simulador) y ejecutar Product > Archive. Guardar el `.xcarchive`, captura del organizador y evidencia de ejecución física. Exportar `Baldeon_ProyectoFinal_iOS.ipa` solo si el tipo de cuenta y perfil lo permiten; una cuenta gratuita no equivale a distribución ad hoc. No presentar el `.jks` Android como certificado de iOS.

La guía solicita varios dispositivos reales. Solo un iPhone disponible no acredita los dos Android exigidos en clase. Se declara esa limitación y se deja pendiente su coordinación con el docente, sin marcar el criterio como cumplido.

## Referencias

- [Requisitos de Kotlin Multiplatform para iOS](https://kotlinlang.org/docs/multiplatform/multiplatform-setup.html).
- [ATS para red local](https://developer.apple.com/documentation/bundleresources/information-property-list/nsapptransportsecurity/nsallowslocalnetworking).
- [Privacidad de red local](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy).
- [SDK nativo usado por GitLive 2.7.0](https://github.com/GitLiveApp/firebase-kotlin-sdk/blob/v2.7.0/gradle/libs.versions.toml).
