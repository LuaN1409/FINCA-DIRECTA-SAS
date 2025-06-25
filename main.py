import pandas as pd
import os

# Ruta al archivo Excel dentro de la carpeta 'data'
ruta = os.path.join(os.path.dirname(__file__), "data", "pedidos_granja.xlsx")

# Credenciales de usuario
usuarios = {
    "username": "j",
    "password": "j"
}

# ------------------ Clase para filtros de pedidos ------------------ #
class FiltroPedidos:
    def __init__(self, archivo):
        try:
            self.df = pd.read_excel(archivo)
            self.df['fecha'] = pd.to_datetime(self.df['fecha'], errors='coerce')
            self.df_filtrado = self.df.copy()
        except Exception as e:
            raise RuntimeError(f"Error al cargar el archivo: {e}")

    def filtrar_por_fecha(self):
        inicio = input("📅 Fecha desde (YYYY-MM-DD o ENTER para omitir): ")
        fin = input("📅 Fecha hasta (YYYY-MM-DD o ENTER para omitir): ")
        try:
            if inicio:
                inicio_dt = pd.to_datetime(inicio)
            else:
                inicio_dt = self.df['fecha'].min()
            if fin:
                fin_dt = pd.to_datetime(fin)
            else:
                fin_dt = self.df['fecha'].max()

            self.df_filtrado = self.df_filtrado[
                self.df_filtrado['fecha'].between(inicio_dt, fin_dt)
            ]

            if self.df_filtrado.empty:
                print("⚠ No se encontraron pedidos en el rango de fechas indicado.")
            else:
                print(f"✅ Pedidos filtrados desde {inicio_dt.date()} hasta {fin_dt.date()}.")
                print(f"🔍 {self.df_filtrado.shape[0]} pedidos encontrados.")
        except Exception:
            print("⚠ Formato de fecha inválido. Intenta con el formato YYYY-MM-DD.")

    def filtrar_por_cliente(self):
        nombre = input("👤 Nombre del cliente (puede ser parcial o ENTER para omitir): ")
        if nombre:
            self.df_filtrado = self.df_filtrado[
                self.df_filtrado['cliente'].str.lower().str.contains(nombre.lower(), na=False)
            ]
            if self.df_filtrado.empty:
                print(f"⚠ No se encontraron pedidos del cliente '{nombre}'.")
            else:
                print(f"🔍 {self.df_filtrado.shape[0]} pedidos coinciden con '{nombre}'.")

    def filtrar_por_producto(self):
        nombre = input("📦 Nombre del producto (puede ser parcial o ENTER para omitir): ")
        if nombre:
            self.df_filtrado = self.df_filtrado[
                self.df_filtrado['producto'].str.lower().str.contains(nombre.lower(), na=False)
            ]
            if self.df_filtrado.empty:
                print(f"⚠ No se encontraron pedidos del producto '{nombre}'.")
            else:
                print(f"🔍 {self.df_filtrado.shape[0]} pedidos coinciden con '{nombre}'.")

    def mostrar_totales(self):
        print(f"📋 Total de pedidos: {len(self.df_filtrado)}")
        if 'cantidad' in self.df_filtrado:
            try:
                total_cantidad = pd.to_numeric(self.df_filtrado['cantidad'], errors='coerce').sum()
                print(f"📦 Total productos pedidos: {total_cantidad}")
            except:
                print("⚠ Error al calcular la cantidad total.")

    def mostrar_tabla(self):
        if self.df_filtrado.empty:
            print("⚠ No hay pedidos para mostrar.")
        else:
            print("\n📄 Pedidos filtrados:")
            tabla = self.df_filtrado.copy()
            tabla.columns = [col.capitalize() for col in tabla.columns]
            for col in tabla.select_dtypes(include=['object']).columns:
                tabla[col] = tabla[col].astype(str).str.capitalize()
            print(tabla.to_string(index=False))

    def reiniciar_filtros(self):
        self.df_filtrado = self.df.copy()
        print("🔁 Filtros reiniciados.")

    def exportar_resultados(self):
        if self.df_filtrado.empty:
            print("⚠ No hay datos para exportar.")
            return

        nombre_archivo = input("💾 Nombre del archivo de salida (sin extensión): ")
        ruta_archivo = os.path.join(os.path.dirname(__file__),"data", f"{nombre_archivo}.xlsx")
        try:
            # Agrupar por tipo de producto y sumar cantidad
            resumen = self.df_filtrado.groupby('producto', as_index=False)['cantidad'].sum()
            resumen.columns = ['producto', 'total_cantidad']
            resumen.to_excel(ruta_archivo, index=False)
            print(f"✅ Resultados exportados a '{ruta_archivo}'")
        except Exception as e:
            print("❌ Error al exportar:", e)

    def mostrar_detalle_pedido(self):
        if self.df_filtrado.empty:
            print("⚠ No hay pedidos disponibles para ver detalles.")
            return
        try:
            idx = int(input(f"🔎 Ingrese el número del pedido (0 a {len(self.df_filtrado)-1}): "))
            if 0 <= idx < len(self.df_filtrado):
                print("\n📌 Detalle del pedido:")
                detalle = self.df_filtrado.iloc[idx].copy()
                for col in detalle.index:
                    if isinstance(detalle[col], str):
                        detalle[col] = detalle[col].capitalize()
                for campo, valor in detalle.items():
                    print(f"- {campo.capitalize()}: {valor}")
            else:
                print("❌ Índice fuera de rango.")
        except:
            print("❌ Entrada no válida. Ingrese un número válido.")

# ------------------ Autenticación ------------------ #
def iniciar_sesion():
    while True:
        print("\n=== INICIO DE SESIÓN ===")
        usuario = input("👤 Usuario (o escriba 'salir' para terminar): ")
        if usuario.lower() == 'salir':
            return False
        contraseña = input("🔒 Contraseña: ")

        if usuario == usuarios["username"] and contraseña == usuarios["password"]:
            print("✅ Inicio de sesión exitoso")
            return True
        else:
            print("❌ Usuario o contraseña incorrectos.")

# ------------------ Menú Principal ------------------ #
def mostrar_menu_opciones():
    try:
        filtro = FiltroPedidos(ruta)
    except RuntimeError as e:
        print("❌", e)
        return

    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1. Consultar demanda de pedidos")
        print("2. Opción dos (pendiente)")
        print("3. Opción tres (pendiente)")
        print("4. Opción cuatro (pendiente)")
        print("5. Opción cinco (pendiente)")
        print("6. Opción seis (pendiente)")
        print("7. Cerrar sesión")

        opcion = input("Elija una opción (1-7 o 'salir'): ").strip().lower()

        if opcion in ['7', 'salir']:
            print("👋 Cerrando sesión...")
            break
        elif opcion == "1":
            menu_consulta(filtro)
        elif opcion in ["2", "3", "4", "5", "6"]:
            print("✔ Has seleccionado una opción aún no implementada.")
        else:
            print("❌ Opción incorrecta. Intenta de nuevo.")

# ------------------ Submenú: Consulta de pedidos ------------------ #
def menu_consulta(filtro):
    while True:
        print("\n== CONSULTAR DEMANDA DE PEDIDOS ==")
        print("1. Filtrar pedidos por fecha")
        print("2. Filtrar pedidos por producto")
        print("3. Filtrar pedidos por cliente")
        print("4. Mostrar totales")
        print("5. Mostrar tabla")
        print("6. Exportar resultados")
        print("7. Ver detalle de un pedido específico")
        print("8. Reiniciar filtros")
        print("9. Volver al menú anterior")

        opcion = input("Elija una opción (1-9 o 'salir'): ").strip().lower()

        if opcion in ['9', 'salir']:
            break
        elif opcion == "1":
            filtro.filtrar_por_fecha()
        elif opcion == "2":
            filtro.filtrar_por_producto()
        elif opcion == "3":
            filtro.filtrar_por_cliente()
        elif opcion == "4":
            filtro.mostrar_totales()
        elif opcion == "5":
            filtro.mostrar_tabla()
        elif opcion == "6":
            filtro.exportar_resultados()
        elif opcion == "7":
            filtro.mostrar_detalle_pedido()
        elif opcion == "8":
            filtro.reiniciar_filtros()
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

# ------------------ Iniciar Programa ------------------ #
if __name__ == "__main__":
    if iniciar_sesion():
        mostrar_menu_opciones()