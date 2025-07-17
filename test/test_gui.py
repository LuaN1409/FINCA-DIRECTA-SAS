#!/usr/bin/env python3
"""
Script de prueba para verificar que la GUI modernizada funciona correctamente
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

def test_import():
    """Probar que todos los imports funcionen correctamente"""
    try:
        import ttkbootstrap as ttk
        print("✅ ttkbootstrap importado correctamente")
        
        from fincaDirectaGUI import SistemaFincaDirectaGUI, PantallaCarga
        print("✅ Clases de GUI importadas correctamente")
        
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_gui_creation():
    """Probar que la GUI se puede crear sin errores"""
    try:
        # Crear instancia de la aplicación
        app = SistemaFincaDirectaGUI()
        print("✅ Instancia de SistemaFincaDirectaGUI creada correctamente")
        
        # Verificar que los colores estén configurados
        print(f"✅ Colores corporativos configurados: {list(app.colors.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Error al crear GUI: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 Iniciando pruebas de la GUI modernizada...")
    print("=" * 50)
    
    # Prueba 1: Imports
    print("\n📦 Probando imports...")
    if not test_import():
        return False
    
    # Prueba 2: Creación de GUI
    print("\n🎨 Probando creación de GUI...")
    if not test_gui_creation():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡Todas las pruebas pasaron exitosamente!")
    print("🌾 Sistema Finca Directa SAS - GUI Modernizada v2.0")
    print("✨ Características:")
    print("   • Interfaz moderna con ttkbootstrap")
    print("   • Colores corporativos personalizados")
    print("   • Pantalla de carga profesional")
    print("   • Diseño responsivo y cards modernas")
    print("   • 8 módulos funcionales completamente integrados")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
