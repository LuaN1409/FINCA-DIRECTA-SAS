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
        # Importar directamente fincaDirectaGUI.py
        debug_print("Importando aplicación principal...")
        from fincaDirectaGUI import SistemaFincaDirectaGUI
        debug_print("✅ Importación exitosa")
        
        app = SistemaFincaDirectaGUI()
        debug_print("✅ Instancia creada correctamente")
        
        app.inicializar_aplicacion()
        debug_print("✅ Aplicación inicializada correctamente")
        
    except Exception as e:
        debug_print(f"❌ Error al iniciar aplicación: {e}")
        
        # Mostrar mensaje de error
        print("\n❌ ERROR AL INICIAR:")
        print(f"   Error: {e}")
        print("\n💡 Sugerencias:")
        print("   1. Verifica que fincaDirectaGUI.py esté en el directorio")
        print("   2. Verifica que main.py esté disponible")
        print("   3. Ejecuta: python fincaDirectaGUI.py directamente")
        
        try:
            messagebox.showerror("Error Crítico", 
                               f"No se pudo ejecutar la aplicación.\n\n"
                               f"Error: {str(e)}\n\n"
                               f"Verifica que todos los archivos estén presentes.")
        except:
            pass
        
        input("Presiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    debug_print("=== INICIO DE APP ===")
    main()
    debug_print("=== FIN DE APP ===")
