"""
GUI Principal - Sistema Finca Directa SAS
Versión Organizada y Modular
"""

import sys
import os

# Agregar paths necesarios
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    # Importar la clase principal desde fincaDirectaGUI.py
    from fincaDirectaGUI import SistemaFincaDirectaGUI, PantallaCarga, main as main_original
    print("✅ Importación exitosa desde fincaDirectaGUI")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    raise ImportError(f"No se pudo importar SistemaFincaDirectaGUI: {e}")

def iniciar_aplicacion():
    """Iniciar la aplicación con la misma lógica que fincaDirectaGUI.py"""
    try:
        # Usar la función main original de fincaDirectaGUI.py
        main_original()
    except Exception as e:
        print(f"❌ Error al ejecutar aplicación: {e}")
        
        # Método de respaldo
        try:
            def callback_iniciar_app():
                app = SistemaFincaDirectaGUI()
                app.inicializar_aplicacion()
            
            pantalla_carga = PantallaCarga(callback_iniciar_app)
            pantalla_carga.mostrar()
            
        except Exception as e2:
            print(f"❌ Error crítico: {e2}")
            raise

if __name__ == "__main__":
    iniciar_aplicacion()
