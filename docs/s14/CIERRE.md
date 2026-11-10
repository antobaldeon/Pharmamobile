# Cierre documental de la práctica 14

Fecha: 10 de noviembre de 2026. Las fotografías finales aportadas actualizan los estados anteriores de diagnóstico.

## Evidencias añadidas

- `docs/captura/s14/01_productos_sincronizados.png`: Android físico con Paracetamol ID del servidor 1, chiquitolina ID 2 y hola ID 3.
- `docs/captura/s14/02_edicion_producto.png`: sesión admin y formulario de edición cargado para hola, precio 12.3, stock 23 y categoría 2. No acredita por sí sola la respuesta al guardar.
- `docs/captura/s14/03_alta_sin_conexion.png`: modo avión, catálogo visible, mensaje de guardado local y envío pendiente con error de conexión. El ID local y la posterior sincronización de ese nuevo registro no son visibles.

Las imágenes originales se conservaron. En el informe solo se recortó el entorno para facilitar la lectura.

## Estado de cierre

El acceso físico ya se observa con sesión admin activa. Paracetamol y chiquitolina, antes pendientes, aparecen con IDs definitivos. Se documentan las correcciones de categorías faltantes, avisos persistentes y dirección de red. Los builds firmados, la verificación del certificado y las 48 pruebas aprobadas se mantienen como resultados técnicos comprobados.

La práctica tiene evidencia física parcial, no un recorrido completo acreditado. Siguen pendientes la eliminación, el guardado final de la edición, los rechazos por rol, el ciclo de cierre/reapertura, los permisos, el segundo y tercer dispositivos, la captura visual de firma, el respaldo de la clave y la instalación iOS. No se crea la etiqueta final ni se afirma ausencia de duplicados.

Se detecta además D05, de severidad baja: caracteres incorrectos en etiquetas de sesión, edición y separador de precio/stock. Las fotografías lo muestran; no se marca como corregido.

## Informe final

- Word editable: `output/doc/Baldeon_Tania_Sesion14_Documentacion_Final.docx`.
- PDF: `output/doc/Baldeon_Tania_Sesion14_Informe_Final.pdf`.

El cierre corresponde a la documentación y las evidencias actuales; conserva explícitos los criterios que faltan por demostrar. El código está registrado en el commit `96b8d8d`; este cierre añade documentación y fotografías, sin modificar la aplicación.
