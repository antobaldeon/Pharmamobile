# Práctica 14: alcance y pruebas

Fecha: 10/11/2026. Se conserva el alcance de PharmaMobil existente: autenticación, catálogo de productos, roles, persistencia local, altas pendientes, sincronización manual y notificaciones locales. No se incorporan funciones, librerías, rediseños ni cambios de esquema.

## Cierre de la ficha de sesión 13

| Hueco de sesión 13 | Clasificación | Resolución o limitación |
| --- | --- | --- |
| Permiso y salida a Ajustes | Cerrado en código | Ya implementado; hay capturas previas. Su recorrido en el APK release debe repetirse. |
| Diez pasos Android y reinstalación | Se valida hoy | Requiere backend accesible y dispositivos; aún sin evidencia nueva. |
| Firma y paquetes release | Se cierra hoy | Configuración de firma local, AAB y APK, minificación y verificación del certificado. |
| Recorrido y archivo iOS | Preparado; limitación declarada | La estudiante retomó iOS: solo dispone de Windows y un iPhone. Se prepara configuración y se comprueba Kotlin; enlace, firma e instalación requieren Mac/Xcode. Ver IOS_EN_IPHONE.md. |
| Reenvío de POST sin idempotencia | Limitación declarada | Una respuesta perdida puede duplicar un alta. Requiere un contrato de idempotencia en PharmaSoft y pruebas; no se cambia en esta sesión. Verificar el servidor antes de reenviar. |
| Catálogo conservado tras cerrar sesión | Limitación declarada | El token y perfil se borran; el catálogo local permanece compartido. Definir política por usuario y probarla antes de modificar persistencia. |
| Sincronización al recuperar señal | Limitación declarada | El usuario pulsa Sincronizar. No hay observador automático de conectividad. |
| Cámara y ubicación | Descartado | No pertenecen al alcance del catálogo; quedan fuera de la entrega. |

## Matriz de pruebas del APK release

Registrar en cada columna marca, modelo y versión real. Se necesitan dos dispositivos físicos distintos durante la práctica; el tercero corresponde a la actividad autónoma. Un emulador no sustituye esas evidencias.

| Recorrido | Dispositivo 1: pendiente | Dispositivo 2: pendiente | Evidencia esperada |
| --- | --- | --- | --- |
| Instalación desde APK, IDE desconectado | Sin ejecutar | Sin ejecutar | Nombre/icono correctos y apertura sin fallos. |
| Login válido, inválido y falta de red | Sin ejecutar | Sin ejecutar | Distingue credenciales de conectividad. |
| Crear, listar, editar y eliminar | Sin ejecutar | Sin ejecutar | CRUD completo y validación por campo. |
| Operación sin privilegios | Sin ejecutar | Sin ejecutar | Rechazo del servidor; conserva sesión. |
| Modo avión: abrir, leer y crear | Sin ejecutar | Sin ejecutar | Datos locales, ID provisional y pendiente. |
| Recuperar conexión y sincronizar | Sin ejecutar | Sin ejecutar | Envío sin duplicados e ID definitivo; sincronización manual. |
| Conceder, denegar y denegar definitivamente | Sin ejecutar | Sin ejecutar | Tres estados y recuperación desde Ajustes. |
| Cerrar sesión y reabrir | Sin ejecutar | Sin ejecutar | Token y perfil borrados; documentar catálogo conservado. |
| Serialización e inyección con minificación | Sin ejecutar | Sin ejecutar | Login, primera consulta y todas las pantallas sin fallos release. |

## Registro de defectos

Dispositivo disponible declarado: iPhone 15 Pro Max, iOS 26.6. El recorrido físico está pendiente de compilar e instalar desde macOS. No se dispone de teléfonos Android para acreditar las dos columnas anteriores; no se sustituyen por resultados inventados ni por la mera compilación Kotlin.

No se registran pruebas no ejecutadas como defectos observados. Para cada defecto real, completar:

| Campo | Valor |
| --- | --- |
| Identificador | D-XX |
| Dispositivo y versión | Marca, modelo y sistema |
| Pasos | Secuencia numerada desde apertura |
| Resultado esperado | Comportamiento definido |
| Resultado obtenido | Mensaje y captura recortada |
| Severidad | Alta: bloquea; media: estorba; baja: cosmético |
| Estado | Corregido, pendiente o descartado con motivo |

## Git

Se creó `feature/builds-14` desde `feature/integrador-13`: no existe `develop` local y hay cambios previos sin commit. Se conservan esos cambios sin atribuirles commits nuevos. La guía exige un commit por paso y fusionar en develop antes del build final; esa secuencia aún debe completarse con los cambios revisados del equipo. No se crea `v1.0-final` mientras falten pruebas y el commit definitivo del build.
