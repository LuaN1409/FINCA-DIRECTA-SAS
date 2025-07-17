"""
Sistema Finca Directa SAS - App Principal
Versión: 3.0 - Garantizada para mostrar tarjetas modernas
"""

def main():
    """Función principal - Ejecuta directamente fincaDirectaGUI"""
    print("🌾 Iniciando Sistema Finca Directa SAS...")
    
    try:
        # Importar y ejecutar directamente fincaDirectaGUI.py
        import fincaDirectaGUI
        print("✅ fincaDirectaGUI cargado")
        
        # Ejecutar la función main de fincaDirectaGUI
        fincaDirectaGUI.main()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Intentando método alternativo...")
        
        try:
            # Método alternativo: crear instancia directa
            import fincaDirectaGUI
            
            def iniciar_app():
                app = fincaDirectaGUI.SistemaFincaDirectaGUI()
                app.inicializar_aplicacion()
            
            pantalla_carga = fincaDirectaGUI.PantallaCarga(iniciar_app)
            pantalla_carga.mostrar()
            
        except Exception as e2:
            print(f"❌ Error crítico: {e2}")
            import traceback
            traceback.print_exc()
            input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
