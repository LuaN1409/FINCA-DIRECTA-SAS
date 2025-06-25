import pandas as pd
import os

# Construimos la ruta relativa al archivo Excel dentro de la carpeta 'data'
ruta = os.path.join(os.path.dirname(__file__), "data", "pedidos_granja.xlsx")

# Diccionario con las credenciales de usuario (usuario y contraseña)
usuarios = {
    "username": "j",
    "password": "j"
}

# ------------------ Clase para filtros de pedidos ------------------ #
class FiltroPedidos:
    def __init__(self, archivo):
        try:
            # Carga el archivo Excel
            self.df = pd.read_excel(archivo)
            
            # Convierte la columna 'fecha' a tipo datetime
            self.df['fecha'] = pd.to_datetime(self.df['fecha'])

            # Crea una copia para trabajar con filtros sin dañar el original
            self.df_filtrado = self.df.copy()
        except Exception as e:
            print("❌ Error al cargar el archivo:", e)
            exit()

    def filtrar_por_fecha(self):
        inicio = input("📅 Fecha desde (YYYY-MM-DD): ")
        fin = input("📅 Fecha hasta (YYYY-MM-DD): ")
        try:
            inicio_dt = pd.to_datetime(inicio)
            fin_dt = pd.to_datetime(fin)
            
            self.df_filtrado = self.df_filtrado[
                self.df_filtrado['fecha'].between(inicio_dt, fin_dt)
            ]

            print(f"✅ Pedidos filtrados desde {inicio} hasta {fin}.")
            print(f"🔍 {self.df_filtrado.shape[0]} pedidos encontrados.")
        except Exception:
            print("⚠ Formato de fecha inválido. Intenta con el formato YYYY-MM-DD.")

    def filtrar_por_cliente(self):
        nombre = input("👤 Nombre del cliente: ")
        self.df_filtrado = self.df_filtrado[
            self.df_filtrado['cliente'].str.lower() == nombre.lower()
        ]

    def filtrar_por_producto(self):
        nombre = input("📦 Nombre del producto: ")
        self.df_filtrado = self.df_filtrado[
            self.df_filtrado['producto'].str.lower() == nombre.lower()
        ]

    def mostrar_totales(self):
        print(f"📋 Total de pedidos: {len(self.df_filtrado)}")
        print(f"📦 Total productos pedidos: {self.df_filtrado['cantidad'].sum()}")

    def mostrar_tabla(self):
        print("\n📄 Pedidos filtrados:")
        print(self.df_filtrado.to_string(index=False))

    def reiniciar_filtros(self):
        self.df_filtrado = self.df.copy()
        print("🔁 Filtros reiniciados.")

# ------------------ Autenticación ------------------ #
def iniciar_sesion():
    print("\n=== INICIO DE SESIÓN ===")
    usuario = input("👤 Usuario: ")
    contraseña = input("🔒 Contraseña: ")

    if usuario == usuarios["username"] and contraseña == usuarios["password"]:
        print("✅ Inicio de sesión exitoso")
        mostrar_menu_opciones()
    else:
        print("❌ Usuario o contraseña incorrectos. Intenta de nuevo.")
        iniciar_sesion()

# ------------------ Menú Principal ------------------ #
def mostrar_menu_opciones():
    filtro = FiltroPedidos(ruta)

    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1. Consultar demanda de pedidos")
        print("2. Opción dos (pendiente)")
        print("3. Opción tres (pendiente)")
        print("4. Opción cuatro (pendiente)")
        print("5. Opción cinco (pendiente)")
        print("6. Opción seis (pendiente)")
        print("7. Cerrar sesión")

        opcion = input("Elija una opción (1-7): ")
#dncanvanas
        match opcion:
            case "1":
                menu_consulta(filtro)
            case "2" | "3" | "4" | "5" | "6":
                print("✔ Has seleccionado una opción aún no implementada.")
            case "7":
                print("👋 Cerrando sesión...")
                break
            case _:
                print("❌ Opción incorrecta. Intenta de nuevo.")

# ------------------ Submenú: Consulta de pedidos ------------------ #
def menu_consulta(filtro):
    while True:
        print("\n== CONSULTAR DEMANDA DE PEDIDOS ==")
        print("1. Ver pedidos por fecha")
        print("2. Ver pedidos por cliente")
        print("3. Ver pedidos por producto")
        print("4. Mostrar totales")
        print("5. Mostrar tabla")
        print("6. Reiniciar filtros")
        print("7. Volver al menú anterior")

        opcion = input("Elija una opción (1-7): ")

        match opcion:
            case "1":
                filtro.filtrar_por_fecha()
            case "2":
                filtro.filtrar_por_cliente()
            case "3":
                filtro.filtrar_por_producto()
            case "4":
                filtro.mostrar_totales()
            case "5":
                filtro.mostrar_tabla()
            case "6":
                filtro.reiniciar_filtros()
            case "7":
                break
            case _:
                print("❌ Opción no válida. Intenta de nuevo.")

# ------------------ Iniciar Programa ------------------ #
if __name__ == "__main__":
    iniciar_sesion()
