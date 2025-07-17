"""
Script para verificar los métodos de la clase SistemaFincaDirectaGUI
"""
import sys

# Importar la clase
from fincaDirectaGUI import SistemaFincaDirectaGUI

# Crear una instancia
app = SistemaFincaDirectaGUI()

# Verificar qué métodos tiene la instancia
metodos_requeridos = [
    'menu_consulta_pedidos',
    'menu_inventario_completo', 
    'menu_verificar_disponibilidad_completo',
    'menu_recepcion_insumos',
    'menu_reportes_recepcion',
    'menu_reportes_solicitudes',
    'menu_reportes_insumos_listos',
    'mostrar_configuracion'
]

print("=== VERIFICACIÓN DE MÉTODOS ===")
for metodo in metodos_requeridos:
    if hasattr(app, metodo):
        print(f"✅ {metodo}: EXISTE")
    else:
        print(f"❌ {metodo}: NO EXISTE")

# Verificar todos los métodos disponibles que empiecen con 'menu_'
print("\n=== MÉTODOS 'menu_' DISPONIBLES ===")
todos_metodos = [m for m in dir(app) if m.startswith('menu_')]
for metodo in todos_metodos:
    print(f"📋 {metodo}")

print(f"\n=== INFORMACIÓN DE LA CLASE ===")
print(f"Clase: {app.__class__.__name__}")
print(f"Módulo: {app.__class__.__module__}")
print(f"Total de atributos: {len(dir(app))}")
