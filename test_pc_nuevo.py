"""
Script de prueba para simular un PC sin dependencias
Simula la instalación automática de dependencias
"""

import sys
import os

# Temporalmente "ocultar" ttkbootstrap para simular que no está instalado
original_modules = sys.modules.copy()

def simular_pc_nuevo():
    """Simular un PC nuevo sin dependencias"""
    
    # Remover módulos para simular que no están instalados
    modules_to_remove = []
    for module_name in sys.modules:
        if any(dep in module_name for dep in ['ttkbootstrap', 'pandas', 'openpyxl']):
            modules_to_remove.append(module_name)
    
    for module in modules_to_remove:
        if module in sys.modules:
            del sys.modules[module]
    
    print("🧪 === SIMULACIÓN PC NUEVO ===")
    print("🖥️ Simulando PC sin dependencias instaladas...")
    print()
    
    # Ahora importar y ejecutar app
    try:
        import app
        app.main()
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        
    # Restaurar módulos
    sys.modules.update(original_modules)

if __name__ == "__main__":
    simular_pc_nuevo()
