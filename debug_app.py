"""
Versión de debug para diagnosticar el problema del menú
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

def debug_print(mensaje):
    """Imprimir mensaje de debug"""
    print(f"[DEBUG] {mensaje}")

def main():
    debug_print("Iniciando debug_app.py...")
    
    try:
        # Primer intento: Estructura modular
        debug_print("Intentando importar estructura modular...")
        sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
        
        from gui.finca_directa_gui import SistemaFincaDirectaGUI
        debug_print("✅ Importación modular exitosa")
        
        app = SistemaFincaDirectaGUI()
        debug_print("✅ Instancia creada correctamente")
        
        app.inicializar_aplicacion()
        debug_print("✅ Aplicación inicializada")
        
    except Exception as e:
        debug_print(f"❌ Error en estructura modular: {e}")
        
        try:
            # Segundo intento: fincaDirectaGUI.py directo
            debug_print("Intentando importar fincaDirectaGUI.py...")
            from fincaDirectaGUI import SistemaFincaDirectaGUI
            debug_print("✅ Importación de fincaDirectaGUI exitosa")
            
            app = SistemaFincaDirectaGUI()
            debug_print("✅ Instancia creada correctamente")
            
            app.inicializar_aplicacion()
            debug_print("✅ Aplicación inicializada")
            
        except Exception as e2:
            debug_print(f"❌ Error en fincaDirectaGUI: {e2}")
            
            try:
                # Tercer intento: intento_moderno.py
                debug_print("Intentando importar intento_moderno.py...")
                from intento_moderno import SistemaFincaDirectaGUI
                debug_print("✅ Importación de intento_moderno exitosa")
                
                app = SistemaFincaDirectaGUI()
                debug_print("✅ Instancia creada correctamente")
                
                app.inicializar_aplicacion()
                debug_print("✅ Aplicación inicializada")
                
            except Exception as e3:
                debug_print(f"❌ Error en intento_moderno: {e3}")
                
                # Último intento: intento.py básico
                debug_print("Intentando ejecutar intento.py básico...")
                try:
                    import intento
                    debug_print("✅ intento.py ejecutado")
                except Exception as e4:
                    debug_print(f"❌ Error en intento.py: {e4}")
                    messagebox.showerror("Error Crítico", 
                                       f"No se pudo ejecutar ninguna versión de la aplicación:\n"
                                       f"Modular: {e}\n"
                                       f"FincaDirectaGUI: {e2}\n"
                                       f"IntentoModerno: {e3}\n"
                                       f"Intento básico: {e4}")

if __name__ == "__main__":
    debug_print("=== INICIO DE DEBUG ===")
    main()
    debug_print("=== FIN DE DEBUG ===")
