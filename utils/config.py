"""
Configuración y utilidades del sistema
"""

import os
import sys
from datetime import datetime

# Configuración de colores corporativos
COLORES_CORPORATIVOS = {
    'primary': '#E4901D',      # Naranja
    'secondary': '#FDC304',    # Amarillo
    'success': '#5B6043',      # Verde oliva
    'light': '#FAF4DC',        # Crema
    'dark': '#2C3E50',         # Oscuro para texto
    'white': '#FFFFFF'
}

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
GUI_DIR = os.path.join(BASE_DIR, 'gui')
CORE_DIR = os.path.join(BASE_DIR, 'core')

# Información del sistema
SISTEMA_INFO = {
    'nombre': 'Sistema Finca Directa SAS',
    'version': '3.0',
    'descripcion': 'Sistema de Gestión de Insumos Agrícolas',
    'fecha_actualizacion': '2025-07-16'
}

def log_mensaje(mensaje, tipo="INFO"):
    """Función de logging simple"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {tipo}: {mensaje}")

def verificar_dependencias():
    """Verificar que las dependencias estén disponibles"""
    dependencias = {
        'pandas': False,
        'ttkbootstrap': False,
        'openpyxl': False
    }
    
    for dep in dependencias:
        try:
            __import__(dep)
            dependencias[dep] = True
        except ImportError:
            pass
    
    return dependencias

if __name__ == "__main__":
    print("🔧 Configuración del Sistema Finca Directa SAS")
    print(f"Versión: {SISTEMA_INFO['version']}")
    
    deps = verificar_dependencias()
    print("\n📦 Estado de dependencias:")
    for dep, estado in deps.items():
        status = "✅" if estado else "❌"
        print(f"  {status} {dep}")
