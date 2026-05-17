#!/usr/bin/env python3
"""
QGIS MCP Server - Connects Claude to QGIS via Model Context Protocol
"""

import logging
import struct
from contextlib import asynccontextmanager
import socket
import json
from typing import AsyncIterator, Dict, Any
from mcp.server.fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("QgisMCPServer")


class QgisMCPServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to the QGIS plugin socket server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(15.0)
            return True
        except Exception as e:
            logger.error(f"Error connecting to server: {str(e)}")
            return False

    def disconnect(self):
        """Disconnect from the server"""
        if self.socket:
            self.socket.close()
            self.socket = None

    def _send(self, data: bytes):
        """Send data with a 4-byte big-endian length prefix"""
        self.socket.sendall(struct.pack('>I', len(data)) + data)

    def _recv_exactly(self, n: int) -> bytes:
        """Receive exactly n bytes"""
        buf = b''
        while len(buf) < n:
            chunk = self.socket.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("Server closed connection unexpectedly")
            buf += chunk
        return buf

    def _recv(self) -> bytes:
        """Receive a length-prefixed message"""
        raw_len = self._recv_exactly(4)
        msg_len = struct.unpack('>I', raw_len)[0]
        return self._recv_exactly(msg_len)

    def send_command(self, command_type, params=None):
        """Send a command to the QGIS plugin and get the response"""
        if not self.socket:
            logger.error("Not connected to server")
            return None

        command = {
            "type": command_type,
            "params": params or {}
        }

        try:
            self._send(json.dumps(command).encode('utf-8'))
            response_data = self._recv()
            return json.loads(response_data.decode('utf-8'))
        except Exception as e:
            logger.error(f"Error sending command: {str(e)}")
            return None


_qgis_connection = None


def get_qgis_connection():
    """Get or create a persistent QGIS connection"""
    global _qgis_connection

    if _qgis_connection is not None:
        try:
            # Check if socket is still alive
            _qgis_connection.socket.sendall(b'')
            return _qgis_connection
        except Exception as e:
            logger.warning(f"Existing connection is no longer valid: {str(e)}")
            try:
                _qgis_connection.disconnect()
            except Exception:
                pass
            _qgis_connection = None

    _qgis_connection = QgisMCPServer(host="localhost", port=9876)
    if not _qgis_connection.connect():
        logger.error("Failed to connect to QGIS")
        _qgis_connection = None
        raise Exception("Could not connect to QGIS. Make sure the QGIS plugin is running.")

    logger.info("Created new persistent connection to QGIS")
    return _qgis_connection


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("QgisMCPServer starting up")
        try:
            get_qgis_connection()
            logger.info("Successfully connected to QGIS on startup")
        except Exception as e:
            logger.warning(f"Could not connect to QGIS on startup: {str(e)}")
            logger.warning("Make sure the QGIS plugin is running before using tools")
        yield {}
    finally:
        global _qgis_connection
        if _qgis_connection:
            logger.info("Disconnecting from QGIS on shutdown")
            _qgis_connection.disconnect()
            _qgis_connection = None
        logger.info("QgisMCPServer shut down")


mcp = FastMCP(
    "Qgis_mcp",
    instructions="QGIS integration through the Model Context Protocol",
    lifespan=server_lifespan
)


@mcp.tool()
def ping(ctx: Context) -> str:
    """Simple ping command to check server connectivity"""
    qgis = get_qgis_connection()
    result = qgis.send_command("ping")
    return json.dumps(result, indent=2)


@mcp.tool()
def get_qgis_info(ctx: Context) -> str:
    """Get QGIS information"""
    qgis = get_qgis_connection()
    result = qgis.send_command("get_qgis_info")
    return json.dumps(result, indent=2)


@mcp.tool()
def load_project(ctx: Context, path: str) -> str:
    """Load a QGIS project from the specified path."""
    qgis = get_qgis_connection()
    result = qgis.send_command("load_project", {"path": path})
    return json.dumps(result, indent=2)


@mcp.tool()
def create_new_project(ctx: Context, path: str) -> str:
    """Create a new project and save it"""
    qgis = get_qgis_connection()
    result = qgis.send_command("create_new_project", {"path": path})
    return json.dumps(result, indent=2)


@mcp.tool()
def get_project_info(ctx: Context) -> str:
    """Get current project information"""
    qgis = get_qgis_connection()
    result = qgis.send_command("get_project_info")
    return json.dumps(result, indent=2)


@mcp.tool()
def add_vector_layer(ctx: Context, path: str, provider: str = "ogr", name: str = None) -> str:
    """Add a vector layer to the project."""
    qgis = get_qgis_connection()
    params = {"path": path, "provider": provider}
    if name:
        params["name"] = name
    result = qgis.send_command("add_vector_layer", params)
    return json.dumps(result, indent=2)


@mcp.tool()
def add_raster_layer(ctx: Context, path: str, provider: str = "gdal", name: str = None) -> str:
    """Add a raster layer to the project."""
    qgis = get_qgis_connection()
    params = {"path": path, "provider": provider}
    if name:
        params["name"] = name
    result = qgis.send_command("add_raster_layer", params)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_layers(ctx: Context) -> str:
    """Retrieve all layers in the current project."""
    qgis = get_qgis_connection()
    result = qgis.send_command("get_layers")
    return json.dumps(result, indent=2)


@mcp.tool()
def remove_layer(ctx: Context, layer_id: str) -> str:
    """Remove a layer from the project by its ID."""
    qgis = get_qgis_connection()
    result = qgis.send_command("remove_layer", {"layer_id": layer_id})
    return json.dumps(result, indent=2)


@mcp.tool()
def zoom_to_layer(ctx: Context, layer_id: str) -> str:
    """Zoom to the extent of a specified layer."""
    qgis = get_qgis_connection()
    result = qgis.send_command("zoom_to_layer", {"layer_id": layer_id})
    return json.dumps(result, indent=2)


@mcp.tool()
def get_layer_features(ctx: Context, layer_id: str, limit: int = 10) -> str:
    """Retrieve features from a vector layer with an optional limit."""
    qgis = get_qgis_connection()
    result = qgis.send_command("get_layer_features", {"layer_id": layer_id, "limit": limit})
    return json.dumps(result, indent=2)


@mcp.tool()
def execute_processing(ctx: Context, algorithm: str, parameters: dict) -> str:
    """Execute a processing algorithm with the given parameters."""
    qgis = get_qgis_connection()
    result = qgis.send_command("execute_processing", {"algorithm": algorithm, "parameters": parameters})
    return json.dumps(result, indent=2)


@mcp.tool()
def save_project(ctx: Context, path: str = None) -> str:
    """Save the current project to the given path, or to the current project path if not specified."""
    qgis = get_qgis_connection()
    params = {}
    if path:
        params["path"] = path
    result = qgis.send_command("save_project", params)
    return json.dumps(result, indent=2)


@mcp.tool()
def render_map(ctx: Context, path: str, width: int = 800, height: int = 600) -> str:
    """Render the current map view to an image file with the specified dimensions."""
    qgis = get_qgis_connection()
    result = qgis.send_command("render_map", {"path": path, "width": width, "height": height})
    return json.dumps(result, indent=2)


@mcp.tool()
def execute_code(ctx: Context, code: str) -> str:
    """Execute arbitrary PyQGIS code provided as a string."""
    qgis = get_qgis_connection()
    result = qgis.send_command("execute_code", {"code": code})
    return json.dumps(result, indent=2)


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
