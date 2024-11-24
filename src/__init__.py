"""
Paquete principal para la aplicación de gestión de Excel.

Este paquete incluye funcionalidades para cargar, procesar y comparar archivos Excel,
así como la interfaz gráfica de usuario (GUI).
"""

import warnings

# Ignorar advertencias de Deprecación (útil en caso de bibliotecas externas)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Importar módulos clave del paquete
try:
    from .excel_ui import ExcelLoaderUI
except ImportError:
    ExcelLoaderUI = None
    warnings.warn("ExcelLoaderUI no está disponible. Algunas funcionalidades pueden no estar completas.")

# Metadatos del paquete
__version__ = '1.0.0'
__author__ = 'Natham Bais'

# Configuración global
CONFIG = {
    "version": __version__,
    "author": __author__,
    "debug": False,
}