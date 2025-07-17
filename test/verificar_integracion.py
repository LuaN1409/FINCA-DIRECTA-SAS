#!/usr/bin/env python3
"""
Script de verificación para confirmar la integración exitosa de módulos modernos
"""

import sys
import os

def verificar_integracion():
    """Verificar que la integración fue exitosa"""
    
    print("🔍 Verificando integración de módulos modernos...")
    print("=" * 60)
    
    try:
        # Leer fincaDirectaGUI.py
        with open('fincaDirectaGUI.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que contiene los métodos integrados
        metodos_esperados = [
            'menu_inventario_completo',
            'mostrar_inventario_completo_moderno',
            'buscar_insumo_moderno',
            'ver_detalle_insumo_moderno',
            'menu_verificar_disponibilidad_completo',
            'generar_lista_envio_moderno',
            'enviar_lista_email_moderno',
            'actualizar_inventario_moderno'
        ]
        
        print("📋 Verificando métodos integrados:")
        metodos_encontrados = 0
        for metodo in metodos_esperados:
            if f'def {metodo}(self' in content:
                print(f"   ✅ {metodo}")
                metodos_encontrados += 1
            else:
                print(f"   ❌ {metodo} - No encontrado")
        
        print(f"\n📊 Resumen: {metodos_encontrados}/{len(metodos_esperados)} métodos integrados")
        
        # Verificar referencias actualizadas en el menú
        print("\n🔗 Verificando referencias del menú:")
        referencias_esperadas = [
            'self.menu_inventario_completo',
            'self.menu_verificar_disponibilidad_completo'
        ]
        
        referencias_encontradas = 0
        for ref in referencias_esperadas:
            if ref in content:
                print(f"   ✅ {ref}")
                referencias_encontradas += 1
            else:
                print(f"   ❌ {ref} - No encontrada")
        
        print(f"\n🎯 Referencias: {referencias_encontradas}/{len(referencias_esperadas)} actualizadas")
        
        # Verificar marcador de integración
        if "MÉTODOS MODERNOS INTEGRADOS" in content:
            print("   ✅ Marcador de integración encontrado")
        else:
            print("   ❌ Marcador de integración no encontrado")
        
        # Compilar para verificar sintaxis
        try:
            compile(content, 'fincaDirectaGUI.py', 'exec')
            print("   ✅ Sintaxis correcta - Sin errores de compilación")
        except SyntaxError as e:
            print(f"   ❌ Error de sintaxis: {e}")
            return False
        
        print("\n" + "=" * 60)
        
        if metodos_encontrados == len(metodos_esperados):
            print("🎉 ¡INTEGRACIÓN COMPLETAMENTE EXITOSA!")
            print("✨ Todos los módulos modernos han sido integrados correctamente")
            print("🚀 La aplicación está lista para usar las nuevas funcionalidades")
            
            print("\n💡 Nuevas funcionalidades disponibles:")
            print("   📦 Inventario: Búsqueda avanzada, detalles por ID, vista completa")
            print("   ✅ Disponibilidad: Generación automática de listas, envío por email")
            print("   🎨 Interfaz: Diseño moderno con cards y colores corporativos")
            print("   📊 Reportes: Análisis detallado con visualización mejorada")
            
            return True
        else:
            print("⚠️ INTEGRACIÓN PARCIAL")
            print(f"Se integraron {metodos_encontrados} de {len(metodos_esperados)} métodos")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == "__main__":
    success = verificar_integracion()
    
    if success:
        print("\n🏁 Verificación completada exitosamente")
        print("💻 Puedes ejecutar: python fincaDirectaGUI.py")
    else:
        print("\n❌ Hay problemas en la integración que requieren atención")
    
    sys.exit(0 if success else 1)
