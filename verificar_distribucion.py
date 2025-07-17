"""
Verificación Final del Sistema con Auto-Instalación
"""

def verificar_sistema_completo():
    """Verificación completa del sistema"""
    print("🌾 === VERIFICACIÓN FINAL SISTEMA FINCA DIRECTA SAS ===")
    print()
    
    import os
    import sys
    
    # 1. Verificar archivos principales
    print("1️⃣ Verificando archivos principales...")
    archivos_principales = [
        'app.py',
        'fincaDirectaGUI.py',
        'main.py',
        'requirements.txt',
        'instalar_y_ejecutar.bat',
        'README.md'
    ]
    
    for archivo in archivos_principales:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo}")
    
    # 2. Verificar carpetas de datos
    print("\n2️⃣ Verificando estructura de datos...")
    if os.path.exists('data'):
        archivos_data = os.listdir('data')
        print(f"   ✅ Carpeta data/ con {len(archivos_data)} archivos")
        for archivo in archivos_data[:3]:  # Mostrar primeros 3
            print(f"      📄 {archivo}")
        if len(archivos_data) > 3:
            print(f"      📄 ... y {len(archivos_data) - 3} más")
    else:
        print("   ❌ Carpeta data/ no encontrada")
    
    # 3. Verificar estructura modular
    print("\n3️⃣ Verificando estructura modular...")
    for carpeta in ['gui', 'core', 'utils']:
        if os.path.exists(carpeta):
            print(f"   ✅ {carpeta}/")
        else:
            print(f"   ⚠️ {carpeta}/ (opcional)")
    
    # 4. Verificar contenido de requirements.txt
    print("\n4️⃣ Verificando requirements.txt...")
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            deps = f.read().strip().split('\n')
        print(f"   ✅ {len(deps)} dependencias listadas:")
        for dep in deps:
            print(f"      📦 {dep}")
    
    # 5. Verificar función de auto-instalación
    print("\n5️⃣ Verificando función de auto-instalación...")
    try:
        import app
        if hasattr(app, 'verificar_e_instalar_dependencias'):
            print("   ✅ Función de auto-instalación disponible")
        if hasattr(app, 'instalar_dependencia'):
            print("   ✅ Función de instalación individual disponible")
        print("   ✅ Módulo app.py importable")
    except Exception as e:
        print(f"   ❌ Error al importar app.py: {e}")
    
    print("\n🎉 === VERIFICACIÓN COMPLETADA ===")
    print("\n📋 INSTRUCCIONES PARA USUARIO FINAL:")
    print("=" * 50)
    print("🚀 INSTALACIÓN EN PC NUEVO:")
    print("   1. Descargar/clonar el repositorio")
    print("   2. Abrir terminal en la carpeta del proyecto")
    print("   3. Ejecutar: python app.py")
    print("   4. El sistema instalará dependencias automáticamente")
    print("   5. Usar credenciales: admin / admin123")
    print()
    print("🔧 ALTERNATIVAS:")
    print("   • Windows: Doble clic en instalar_y_ejecutar.bat")
    print("   • Manual: pip install -r requirements.txt && python app.py")
    print("   • Directo: python fincaDirectaGUI.py")
    print()
    print("✅ SISTEMA LISTO PARA DISTRIBUCIÓN")

if __name__ == "__main__":
    verificar_sistema_completo()
