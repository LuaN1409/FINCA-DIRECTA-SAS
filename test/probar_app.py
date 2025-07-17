"""
Script de prueba final para verificar app.py
"""
import subprocess
import sys
import os

def probar_app():
    """Probar que app.py funcione correctamente"""
    print("🧪 === PRUEBA FINAL DE APP.PY ===")
    print()
    
    # Verificar que app.py existe
    if not os.path.exists("app.py"):
        print("❌ app.py no encontrado")
        return False
        
    print("✅ app.py encontrado")
    
    # Verificar sintaxis
    try:
        import ast
        with open("app.py", "r", encoding="utf-8") as f:
            codigo = f.read()
        ast.parse(codigo)
        print("✅ Sintaxis de app.py válida")
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en app.py: {e}")
        return False
    
    # Verificar importaciones
    try:
        import fincaDirectaGUI
        print("✅ fincaDirectaGUI importable")
        
        # Verificar que SistemaFincaDirectaGUI tenga los métodos necesarios
        app = fincaDirectaGUI.SistemaFincaDirectaGUI()
        metodos_criticos = [
            'mostrar_login', 
            'mostrar_menu_principal',
            'menu_inventario',
            'menu_consulta_pedidos'
        ]
        
        for metodo in metodos_criticos:
            if hasattr(app, metodo):
                print(f"✅ Método {metodo} disponible")
            else:
                print(f"❌ Método {metodo} no encontrado")
                return False
                
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    
    print()
    print("🎉 === PRUEBA EXITOSA ===")
    print("📋 Instrucciones:")
    print("   1. Ejecuta: python app.py")
    print("   2. Espera la pantalla de carga")
    print("   3. Introduce credenciales:")
    print("      👤 Usuario: admin")
    print("      🔐 Contraseña: admin123")
    print("   4. Verifica que aparezcan las tarjetas modernas")
    print()
    print("🎨 Deberías ver:")
    print("   📊 Consultar Demanda de Pedidos")
    print("   📦 Consultar Inventario") 
    print("   ✅ Verificar Disponibilidad")
    print("   📥 Recepción de Insumos")
    print("   📋 Reportes de Recepción")
    print("   🛒 Reportes de Solicitudes")
    print("   🚚 Reportes Insumos Listos")
    print("   ⚙️ Configuración")
    print()
    
    return True

if __name__ == "__main__":
    print("🔍 Verificando funcionamiento de app.py...")
    if probar_app():
        print("✅ Todo listo para usar!")
    else:
        print("❌ Hay problemas que necesitan resolverse")
        input("Presiona Enter para salir...")
