"""
Script de verificación final del sistema Finca Directa SAS
"""
import sys
import os

def verificar_sistema():
    """Verificar que todo el sistema esté funcionando correctamente"""
    print("🌾 === VERIFICACIÓN FINAL DEL SISTEMA FINCA DIRECTA SAS ===")
    print()
    
    # 1. Verificar entorno Python
    print("1️⃣ Verificando entorno Python...")
    print(f"   ✅ Python {sys.version}")
    print()
    
    # 2. Verificar dependencias
    print("2️⃣ Verificando dependencias...")
    dependencias = ['pandas', 'openpyxl', 'ttkbootstrap']
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   ✅ {dep}: Instalado correctamente")
        except ImportError:
            print(f"   ❌ {dep}: No instalado")
    print()
    
    # 3. Verificar archivos principales
    print("3️⃣ Verificando archivos principales...")
    archivos = [
        'main.py',
        'fincaDirectaGUI.py', 
        'app.py',
        'data/usuarios.xlsx',
        'data/inventario.xlsx'
    ]
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}: Existe")
        else:
            print(f"   ❌ {archivo}: No encontrado")
    print()
    
    # 4. Verificar estructura modular
    print("4️⃣ Verificando estructura modular...")
    carpetas = ['gui', 'core', 'utils']
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            print(f"   ✅ {carpeta}/: Existe")
        else:
            print(f"   ❌ {carpeta}/: No encontrada")
    print()
    
    # 5. Verificar importaciones
    print("5️⃣ Verificando importaciones...")
    try:
        from fincaDirectaGUI import SistemaFincaDirectaGUI
        print("   ✅ fincaDirectaGUI: Importación exitosa")
        
        # Verificar métodos críticos
        app = SistemaFincaDirectaGUI()
        metodos = ['menu_inventario', 'menu_consulta_pedidos', 'mostrar_login']
        for metodo in metodos:
            if hasattr(app, metodo):
                print(f"   ✅ {metodo}: Método disponible")
            else:
                print(f"   ❌ {metodo}: Método no encontrado")
                
    except Exception as e:
        print(f"   ❌ Error de importación: {e}")
    print()
    
    # 6. Verificar archivos de datos
    print("6️⃣ Verificando archivos de datos...")
    data_files = os.listdir('data') if os.path.exists('data') else []
    print(f"   📁 Archivos en data/: {len(data_files)}")
    for file in data_files[:5]:  # Mostrar solo los primeros 5
        print(f"   📄 {file}")
    if len(data_files) > 5:
        print(f"   📄 ... y {len(data_files) - 5} archivos más")
    print()
    
    print("🎉 === VERIFICACIÓN COMPLETADA ===")
    print("💡 Para ejecutar la aplicación:")
    print("   🚀 Opción 1: python app.py")
    print("   🚀 Opción 2: python fincaDirectaGUI.py")
    print("   👤 Usuario de prueba: admin / admin123")
    print()

if __name__ == "__main__":
    verificar_sistema()
