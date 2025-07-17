"""
Sistema Finca Directa SAS - Launcher Principal
Versión: 3.0 - Con instalación automática de dependencias
Descripción: Ejecuta la aplicación con instalación automática de dependencias para funcionar en cualquier PC
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess
import importlib

def instalar_dependencia(paquete):
    """Instalar una dependencia usando pip"""
    try:
        print(f"📦 Instalando {paquete}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {paquete} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar {paquete}: {e}")
        return False

def verificar_e_instalar_dependencias():
    """Verificar e instalar dependencias automáticamente"""
    dependencias = {
        'pandas': 'pandas>=1.5.0',
        'openpyxl': 'openpyxl>=3.0.0', 
        'ttkbootstrap': 'ttkbootstrap>=1.10.0'
    }
    
    dependencias_faltantes = []
    
    print("🔍 Verificando dependencias...")
    
    for modulo, paquete in dependencias.items():
        try:
            importlib.import_module(modulo)
            print(f"✅ {modulo}: Disponible")
        except ImportError:
            print(f"❌ {modulo}: No encontrado")
            dependencias_faltantes.append(paquete)
    
    if dependencias_faltantes:
        print(f"📋 Dependencias faltantes: {len(dependencias_faltantes)}")
        print("🚀 Instalando dependencias automáticamente...")
        
        # Intentar instalar desde requirements.txt primero
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        if os.path.exists(requirements_path):
            try:
                print("📄 Instalando desde requirements.txt...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
                print("✅ Dependencias instaladas desde requirements.txt")
                return True
            except subprocess.CalledProcessError:
                print("⚠️ Error al instalar desde requirements.txt, instalando individualmente...")
        
        # Instalar individualmente si falla requirements.txt
        for paquete in dependencias_faltantes:
            if not instalar_dependencia(paquete):
                print(f"❌ No se pudo instalar {paquete}")
                return False
        
        print("✅ Todas las dependencias instaladas correctamente")
    else:
        print("✅ Todas las dependencias están disponibles")
    
    return True

def debug_print(mensaje):
    """Imprimir mensaje de debug"""
    print(f"[APP] {mensaje}")

def main():
    """Función principal del sistema - Con instalación automática de dependencias"""
    print("🌾 === SISTEMA FINCA DIRECTA SAS ===")
    print("📋 Verificando e instalando dependencias...")
    
    # Verificar e instalar dependencias automáticamente
    if not verificar_e_instalar_dependencias():
        print("❌ Error al instalar dependencias")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    print("\n🚀 Iniciando aplicación...")
    debug_print("Iniciando Sistema Finca Directa SAS...")
    
    try:
        # Primer intento: Estructura modular (igual que debug_app.py)
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
                # Tercer intento: intento_moderno.py (si existe)
                debug_print("Intentando importar intento_moderno.py...")
                from intento_moderno import SistemaFincaDirectaGUI
                debug_print("✅ Importación de intento_moderno exitosa")
                
                app = SistemaFincaDirectaGUI()
                debug_print("✅ Instancia creada correctamente")
                
                app.inicializar_aplicacion()
                debug_print("✅ Aplicación inicializada")
                
            except Exception as e3:
                debug_print(f"❌ Error en intento_moderno: {e3}")
                
                # Último intento: intento.py básico (si existe)
                debug_print("Intentando ejecutar intento.py básico...")
                try:
                    import intento
                    debug_print("✅ intento.py ejecutado")
                except Exception as e4:
                    debug_print(f"❌ Error en intento.py: {e4}")
                    
                    # Mostrar mensaje de error final
                    print("\n❌ ERROR CRÍTICO:")
                    print(f"   Modular: {e}")
                    print(f"   FincaDirectaGUI: {e2}")
                    print(f"   IntentoModerno: {e3}")
                    print(f"   Intento básico: {e4}")
                    print("\n💡 Sugerencias:")
                    print("   1. Verifica que fincaDirectaGUI.py esté en el directorio")
                    print("   2. Verifica que main.py esté disponible")
                    print("   3. Ejecuta: python fincaDirectaGUI.py directamente")
                    
                    try:
                        messagebox.showerror("Error Crítico", 
                                           f"No se pudo ejecutar ninguna versión de la aplicación.\n\n"
                                           f"Errores encontrados:\n"
                                           f"• Modular: {str(e)[:50]}...\n"
                                           f"• FincaDirectaGUI: {str(e2)[:50]}...\n"
                                           f"• IntentoModerno: {str(e3)[:50]}...\n"
                                           f"• Intento básico: {str(e4)[:50]}...")
                    except:
                        pass
                    
                    input("Presiona Enter para salir...")
                    sys.exit(1)

if __name__ == "__main__":
    debug_print("=== INICIO DE APP ===")
    main()
    debug_print("=== FIN DE APP ===")
