# src/__init__.py
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
# Puedes importar el módulo main si deseas que esté disponible al importar el paquete src
from .excel_ui import ExcelLoaderUI

# O inicializar algunas variables globales si es necesario
__version__ = '1.0.0'
__author__ = 'Natham Bais'