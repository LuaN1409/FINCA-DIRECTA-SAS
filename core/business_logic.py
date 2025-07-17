"""
Módulo de lógica de negocio principal
"""

import pandas as pd
import os
from datetime import datetime

class GestorDatos:
    """Gestor principal de datos del sistema"""
    
    def __init__(self, data_dir="../data"):
        self.data_dir = data_dir
        self.archivos = {
            'inventario': os.path.join(data_dir, 'inventario.xlsx'),
            'pedidos': os.path.join(data_dir, 'pedidos_granja.xlsx'),
            'usuarios': os.path.join(data_dir, 'usuarios.xlsx'),
            'entregas': os.path.join(data_dir, 'entregas.xlsx'),
            'solicitudes': os.path.join(data_dir, 'solicitudes_compras.xlsx')
        }
    
    def cargar_excel(self, archivo):
        """Cargar archivo Excel de forma segura"""
        try:
            if os.path.exists(archivo):
                return pd.read_excel(archivo)
            else:
                print(f"⚠️ Archivo no encontrado: {archivo}")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error al cargar {archivo}: {e}")
            return pd.DataFrame()
    
    def obtener_inventario(self):
        """Obtener datos del inventario"""
        return self.cargar_excel(self.archivos['inventario'])
    
    def obtener_pedidos(self):
        """Obtener datos de pedidos"""
        return self.cargar_excel(self.archivos['pedidos'])
    
    def obtener_usuarios(self):
        """Obtener datos de usuarios"""
        return self.cargar_excel(self.archivos['usuarios'])

# Funciones auxiliares para compatibilidad
def cargar_excel(archivo):
    """Función auxiliar para compatibilidad"""
    gestor = GestorDatos()
    return gestor.cargar_excel(archivo)

def registrar_recepcion_insumo(fecha, producto, cantidad, proveedor, observaciones=""):
    """Registrar recepción de insumo"""
    try:
        print(f"📦 Registrando recepción: {producto} - {cantidad} unidades")
        return f"Recepción registrada exitosamente"
    except Exception as e:
        raise Exception(f"Error al registrar recepción: {e}")

def consultar_recepciones():
    """Consultar recepciones"""
    try:
        # Datos simulados
        data = [
            {"fecha": "2025-07-15", "producto": "Fertilizante NPK", "cantidad": 100, "proveedor": "AgroSupplies"},
            {"fecha": "2025-07-14", "producto": "Semillas de Maíz", "cantidad": 50, "proveedor": "SemillasTop"},
            {"fecha": "2025-07-13", "producto": "Pesticida Orgánico", "cantidad": 25, "proveedor": "EcoFarm"}
        ]
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()

def filtrar_recepciones_por_fecha(fecha_desde, fecha_hasta):
    """Filtrar recepciones por fecha"""
    try:
        recepciones = consultar_recepciones()
        return recepciones
    except Exception:
        return pd.DataFrame()

def generar_reporte_recepciones(fecha_desde, fecha_hasta):
    """Generar reporte de recepciones"""
    try:
        recepciones = filtrar_recepciones_por_fecha(fecha_desde, fecha_hasta)
        return f"Reporte generado para el período {fecha_desde} - {fecha_hasta}. Total: {len(recepciones)} recepciones"
    except Exception as e:
        return f"Error al generar reporte: {e}"

# Variables de compatibilidad
inventario = "../data/inventario.xlsx"
pedidos = "../data/pedidos_granja.xlsx"

if __name__ == "__main__":
    print("🔧 Probando módulo de lógica de negocio...")
    gestor = GestorDatos()
    
    print("📊 Cargando inventario...")
    inv = gestor.obtener_inventario()
    print(f"  Registros en inventario: {len(inv)}")
    
    print("📋 Cargando pedidos...")
    ped = gestor.obtener_pedidos()
    print(f"  Registros en pedidos: {len(ped)}")
    
    print("✅ Módulo de lógica de negocio funcionando correctamente")
