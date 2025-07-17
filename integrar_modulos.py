"""
Script para integrar los módulos modernos en fincaDirectaGUI.py
"""

import sys
import os

"""
Script para integrar los módulos modernos en fincaDirectaGUI.py
"""

import sys
import os
import re

def extraer_metodos_modernos():
    """Extraer métodos de modulos_modernos.py"""
    
    with open('modulos_modernos.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar todos los métodos que empiezan con 'def ' y tienen 'self'
    methods = []
    lines = content.split('\n')
    current_method = []
    in_method = False
    indent_level = 0
    
    for line in lines:
        if line.startswith('def ') and '(self' in line:
            # Guardar método anterior si existe
            if current_method:
                methods.append('\n'.join(current_method))
            
            # Iniciar nuevo método
            current_method = [line]
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            
        elif in_method:
            # Si encontramos otra función o línea sin indentación apropiada
            if line.startswith('def ') or (line.strip() and not line.startswith(' ') and not line.startswith('\t')):
                # Terminar método actual a menos que sea otro método
                if line.startswith('def ') and '(self' in line:
                    methods.append('\n'.join(current_method))
                    current_method = [line]
                    indent_level = len(line) - len(line.lstrip())
                else:
                    methods.append('\n'.join(current_method))
                    current_method = []
                    in_method = False
            else:
                # Agregar línea al método actual
                current_method.append(line)
    
    # Agregar último método
    if current_method:
        methods.append('\n'.join(current_method))
    
    return methods

def integrar_en_finca_directa():
    """Integrar métodos en fincaDirectaGUI.py"""
    
    print("� Iniciando integración automática...")
    
    # Extraer métodos modernos
    methods = extraer_metodos_modernos()
    print(f"📦 Extraídos {len(methods)} métodos modernos")
    
    for i, method in enumerate(methods):
        first_line = method.split('\n')[0]
        method_name = first_line.split('(')[0].replace('def ', '').strip()
        print(f"   {i+1}. {method_name}")
    
    # Leer fincaDirectaGUI.py
    with open('fincaDirectaGUI.py', 'r', encoding='utf-8') as f:
        gui_content = f.read()
    
    # Encontrar el final de la clase SistemaFincaDirectaGUI
    # Buscar la última línea de método de la clase
    lines = gui_content.split('\n')
    insert_position = len(lines)
    
    # Buscar el mejor lugar para insertar (antes de la función main o al final de la clase)
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith('def main(') or line.startswith('if __name__'):
            insert_position = i
            break
        elif line.startswith('def ') and 'self' in line and not line.strip().startswith('#'):
            # Encontrar el final de este método
            j = i + 1
            while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
                j += 1
            insert_position = j
            break
    
    # Preparar métodos para insertar
    methods_to_insert = []
    for method in methods:
        method_lines = method.split('\n')
        # Asegurar indentación correcta (4 espacios)
        indented_method = []
        for line in method_lines:
            if line.strip():  # Si no está vacía
                indented_method.append('    ' + line)
            else:
                indented_method.append('')
        methods_to_insert.extend(indented_method)
        methods_to_insert.append('')  # Línea vacía entre métodos
    
    # Insertar métodos
    new_lines = lines[:insert_position] + ['', '    # ==================== MÉTODOS MODERNOS INTEGRADOS ====================', ''] + methods_to_insert + lines[insert_position:]
    
    # Escribir archivo actualizado
    with open('fincaDirectaGUI.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"\n✅ Integración completada exitosamente!")
    print(f"📝 Se agregaron {len(methods)} métodos modernos a fincaDirectaGUI.py")
    print(f"📍 Métodos insertados en la línea {insert_position}")
    
    return True

def integrar_modulos():
    """Función principal de integración"""
    try:
        return integrar_en_finca_directa()
    except Exception as e:
        print(f"❌ Error durante la integración: {e}")
        return False

if __name__ == "__main__":
    print("� Integrando módulos modernos en fincaDirectaGUI.py...")
    print("=" * 60)
    
    success = integrar_modulos()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 ¡Integración completada exitosamente!")
        print("🚀 fincaDirectaGUI.py ahora incluye todos los métodos modernos")
        print("💡 Puedes ejecutar la aplicación para probar los nuevos módulos")
    else:
        print("\n❌ La integración falló. Revisa los errores anteriores.")
