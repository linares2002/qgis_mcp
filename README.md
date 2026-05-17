# QGIS MCP

Conecta Claude AI a QGIS a través del Model Context Protocol (MCP), permitiendo a Claude interactuar y controlar QGIS directamente.

## Acknowledgements
Este proyecto está basado en el trabajo de **Juan José Santos** ([@jjsantos01](https://github.com/jjsantos01)).  
Repositorio original: [jjsantos01/qgis_mcp](https://github.com/jjsantos01/qgis_mcp).  

---

## Requisitos previos

- [QGIS 3.X](https://qgis.org/) instalado
- [Claude Desktop](https://claude.ai/download) instalado
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado

---

## 1. Archivos del servidor

Clona este repositorio para obtener los archivos necesarios:

```bash
git clone https://github.com/TU_USUARIO/qgis_mcp.git
cd qgis_mcp
```

> **¿No tienes Git?** Descarga el repositorio como ZIP desde GitHub (`Code` → `Download ZIP`), descomprímelo y renombra la carpeta a `qgis_mcp`.

La carpeta debe contener estos 2 archivos:

- `qgis_mcp_server.py`
- `pyproject.toml` con este contenido:

```toml
[project]
name = "qgis-mcp"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = [
    "mcp[cli]>=1.3.0",
]
```

---

## 2. Instalar dependencias

Desde la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
uv sync
```

Esto creará el entorno virtual `.venv` e instalará todas las dependencias automáticamente.

---

## 3. Configurar Claude Desktop

Edita el archivo de configuración de Claude Desktop:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Añade lo siguiente, ajustando la ruta a tu carpeta del proyecto:

```json
{
    "mcpServers": {
        "qgis": {
            "command": "uv",
            "args": [
                "--directory",
                "/RUTA/ABSOLUTA/A/qgis_mcp",
                "run",
                "qgis_mcp_server.py"
            ]
        }
    }
}
```

Cierra y vuelve a abrir Claude Desktop para que tome los cambios.

---

## 4. Uso

Cada vez que quieras usarlo:

1. Abre QGIS → `Plugins` → `QGIS MCP` → **Start Server**
2. Abre Claude Desktop — el servidor MCP arranca automáticamente en segundo plano gracias a la configuración del paso 3. Verás el ícono 🔨 con las herramientas de QGIS disponibles.

### Probar el servidor manualmente

Si quieres verificar que el servidor funciona sin usar Claude Desktop:

```bash
uv run qgis_mcp_server.py
```

En uso normal no es necesario — Claude Desktop lo gestiona automáticamente.

---

## Herramientas disponibles

Una vez conectado, Claude tendrá acceso a las siguientes herramientas:

| Herramienta | Descripción |
|---|---|
| `ping` | Comprueba la conectividad con el servidor |
| `get_qgis_info` | Obtiene información de la instalación de QGIS |
| `load_project` | Carga un proyecto QGIS desde una ruta |
| `create_new_project` | Crea un nuevo proyecto y lo guarda |
| `get_project_info` | Obtiene información del proyecto actual |
| `add_vector_layer` | Añade una capa vectorial al proyecto |
| `add_raster_layer` | Añade una capa raster al proyecto |
| `get_layers` | Lista todas las capas del proyecto |
| `remove_layer` | Elimina una capa por su ID |
| `zoom_to_layer` | Hace zoom a la extensión de una capa |
| `get_layer_features` | Obtiene features de una capa vectorial |
| `execute_processing` | Ejecuta un algoritmo de procesamiento |
| `save_project` | Guarda el proyecto actual |
| `render_map` | Renderiza el mapa a un archivo de imagen |
| `execute_code` | Ejecuta código PyQGIS arbitrario |
