Eres un asistente experto en QGIS operando sobre Windows a través del plugin MCP. Ejecuta cada paso en orden, confirma el resultado antes de continuar y devuelve un mensaje de estado tras cada acción. Si algún paso falla, detente y describe el error antes de seguir.

PASO 1: VERIFICACIÓN DE CONECTIVIDAD

Lanza un ping al servidor MCP de QGIS para confirmar que el plugin está activo y responde correctamente. Muestra el resultado del ping e indica si la conexión es exitosa o no.

PASO 2: CREAR Y GUARDAR PROYECTO

Crea un nuevo proyecto QGIS llamado "proyecto" y guárdalo en la siguiente ruta:

C:\Users\mange\Documents\Cursos\INTRODUCCIÓN A LOS SISTEMAS DE INFORMACIÓN GEOGRÁFICA\proyecto\proyecto.qgz

Confirma la ruta completa y el nombre del fichero generado.

PASO 3: CARGAR CAPA VECTORIAL

Añade la capa de demarcaciones hidrográficas ubicada en:

C:\Users\mange\Documents\Cursos\INTRODUCCIÓN A LOS SISTEMAS DE INFORMACIÓN GEOGRÁFICA\proyecto\Ejercicios\DemarcacionesHidrograficas

Detecta automáticamente el archivo .shp presente en ese directorio y cárgalo como capa vectorial en el proyecto. Confirma el nombre de la capa y el número de entidades cargadas.

PASO 4: IMPORTAR TABLA CSV

Añade el archivo Embalses.csv ubicado en:

C:\Users\mange\Documents\Cursos\INTRODUCCIÓN A LOS SISTEMAS DE INFORMACIÓN GEOGRÁFICA\proyecto\Ejercicios\Embalses.csv

como capa de texto delimitado usando PyQGIS directamente (execute_code) con los siguientes pasos:

Construye la URI con estos parámetros:
- type=csv
- delimiter=; (delimitador literal)
- geomType=none (sin geometría, solo tabla de atributos)
- useHeader=yes (primera fila como cabecera)
- trimFields=yes
- encoding=UTF-8
- Espacios en la ruta codificados como %20

Confirma: nombre de los campos detectados, número de campos y número de registros.

PASO 5: UNIÓN DE TABLAS (JOIN)

Realiza una unión de atributos (join) entre la tabla importada "Embalses" y la capa vectorial DemarcacionesHidrograficas.

Tabla origen: Embalses
Capa destino: DemarcacionesHidrograficas

Campo de unión identificado:
- Origen: ID
- Destino: COD_DEMAR
- Método: Normalización y mapeo directo

PASO 6: SIMBOLOGÍA Y ETIQUETAS

Aplica a la capa DemarcacionesHidrograficas.shp la siguiente configuración:

1. Simbología: estilo graduado (coropletas) basado en el campo Per_embal (porcentaje de capacidad embalsada a 1 de octubre de 2018). Usa una rampa de color progresiva (de azul muy claro a azul oscuro) con un número de clases adecuado (5 recomendado).

2. Etiquetas: activa las etiquetas mostrando el valor del porcentaje con un decimal y el símbolo % junto al nombre de la cuenca si está disponible.

Confirma los rangos de clasificación aplicados y el número de clases generadas.
