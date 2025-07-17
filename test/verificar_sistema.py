#!/usr/bin/env python3
"""
Script de verificación y corrección de errores
Sistema Finca Directa SAS v3.0
"""

import sys
import os
import subprocess

def verificar_estructura_proyecto():
    """Verificar que la estructura del proyecto sea correcta"""
    print("🏗️ Verificando estructura del proyecto...")
    
    directorios_esperados = [
        'gui',
        'core', 
        'utils',
        'data'
    ]
    
    archivos_esperados = [
        'app.py',
        'fincaDirectaGUI.py',
        'main.py',
        'gui/finca_directa_gui.py',
        'gui/__init__.py',
        'core/business_logic.py',
        'core/__init__.py',
        'utils/config.py',
        'utils/__init__.py'
    ]
    
    # Verificar directorios
    print("\n📁 Verificando directorios:")
    for dir_name in directorios_esperados:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ - No encontrado")
    
    # Verificar archivos
    print("\n📄 Verificando archivos:")
    for archivo in archivos_esperados:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - No encontrado")
    
    return True

def verificar_sintaxis_python():
    """Verificar sintaxis de archivos Python"""
    print("\n🐍 Verificando sintaxis Python...")
    
    archivos_python = [
        'app.py',
        'fincaDirectaGUI.py',
        'intento_moderno.py',
        'gui/finca_directa_gui.py',
        'core/business_logic.py',
        'utils/config.py'
    ]
    
    errores_encontrados = 0
    
    for archivo in archivos_python:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                
                # Compilar para verificar sintaxis
                compile(codigo, archivo, 'exec')
                print(f"   ✅ {archivo} - Sintaxis OK")
                
            except SyntaxError as e:
                print(f"   ❌ {archivo} - Error de sintaxis: {e}")
                errores_encontrados += 1
            except Exception as e:
                print(f"   ⚠️ {archivo} - Advertencia: {e}")
        else:
            print(f"   ⏭️ {archivo} - Archivo no encontrado")
    
    return errores_encontrados == 0

def verificar_dependencias():
    """Verificar dependencias de Python"""
    print("\n📦 Verificando dependencias...")
    
    dependencias = [
        'pandas',
        'ttkbootstrap', 
        'openpyxl',
        'tkinter'
    ]
    
    faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'tkinter':
                import tkinter
            else:
                __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - No instalado")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n💡 Para instalar dependencias faltantes:")
        print(f"   pip install {' '.join(faltantes)}")
    
    return len(faltantes) == 0

def ejecutar_pruebas():
    """Ejecutar pruebas básicas"""
    print("\n🧪 Ejecutando pruebas básicas...")
    
    try:
        # Probar importación de módulos
        sys.path.append('.')
        
        print("   🔍 Probando imports...")
        
        try:
            from utils.config import COLORES_CORPORATIVOS
            print("   ✅ utils.config importado correctamente")
        except ImportError as e:
            print(f"   ❌ Error al importar utils.config: {e}")
        
        try:
            from core.business_logic import GestorDatos
            print("   ✅ core.business_logic importado correctamente")
        except ImportError as e:
            print(f"   ❌ Error al importar core.business_logic: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en pruebas: {e}")
        return False

def sugerir_correcciones():
    """Sugerir correcciones para problemas comunes"""
    print("\n💡 Sugerencias de corrección:")
    print("   1. Verificar que ttkbootstrap esté instalado:")
    print("      pip install ttkbootstrap")
    print("   2. Verificar que pandas y openpyxl estén instalados:")
    print("      pip install pandas openpyxl")
    print("   3. Para ejecutar la aplicación:")
    print("      python app.py")
    print("   4. Alternativa si app.py no funciona:")
    print("      python fincaDirectaGUI.py")

def main():
    """Función principal del verificador"""
    print("🔧 VERIFICADOR DEL SISTEMA FINCA DIRECTA SAS")
    print("=" * 50)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Ejecutar verificaciones
    estructura_ok = verificar_estructura_proyecto()
    sintaxis_ok = verificar_sintaxis_python()
    deps_ok = verificar_dependencias()
    pruebas_ok = ejecutar_pruebas()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print(f"   📁 Estructura: {'✅ OK' if estructura_ok else '❌ Problemas'}")
    print(f"   🐍 Sintaxis: {'✅ OK' if sintaxis_ok else '❌ Errores'}")
    print(f"   📦 Dependencias: {'✅ OK' if deps_ok else '❌ Faltantes'}")
    print(f"   🧪 Pruebas: {'✅ OK' if pruebas_ok else '❌ Fallos'}")
    
    if all([estructura_ok, sintaxis_ok, deps_ok, pruebas_ok]):
        print("\n🎉 ¡Sistema verificado y listo para usar!")
        print("💻 Ejecuta: python app.py")
    else:
        print("\n⚠️ Se encontraron problemas que requieren atención")
        sugerir_correcciones()
    
    return all([estructura_ok, sintaxis_ok, deps_ok, pruebas_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
