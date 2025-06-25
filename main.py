import pandas as pd
import os
import smtplib
from email.message import EmailMessage

# ------------------ Rutas relativas a archivos Excel ------------------ #
pedidos = os.path.join(os.path.dirname(__file__), "data", "pedidos_granja.xlsx")
inventario = os.path.join(os.path.dirname(__file__), "data", "inventario.xlsx")
inventario_actualizado = os.path.join(os.path.dirname(__file__), "data", "inventario_actualizado.xlsx")
insumos_disponibles = os.path.join(os.path.dirname(__file__), "data", "insumos_disponibles.xlsx")
demanda = os.path.join(os.path.dirname(__file__),"data", "demanda.xlsx")
# ------------------ Credenciales de usuario ------------------ #
usuarios = {
    "username": "j",
    "password": "j"
}

# ------------------ Configuración del servidor de correo ------------------ #
SMTP_SERVER  = 'smtp.gmail.com'
SMTP_PORT    = 587
EMAIL_USER   = os.getenv('EMAIL_USER')   # Variable de entorno para mayor seguridad
EMAIL_PASS   = os.getenv('EMAIL_PASS')
LEADER_EMAIL = 'jmarquezco@unal.edu.co'  # Destinatario fijo

# ------------------ Clase para gestionar filtros de pedidos ------------------ #
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

       
        try:
            # Agrupar por tipo de producto y sumar cantidad
            resumen = self.df_filtrado.groupby('producto', as_index=False)['cantidad'].sum()
            resumen.columns = ['producto', 'total_cantidad']
            resumen.to_excel(demanda, index=False)
            print(f"✅ Resultados exportados a '{demanda}'")
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
# ------------------ Funciones relacionadas con el inventario ------------------ #
def cargar_inventario():
    df = pd.read_excel(inventario)
    columnas_requeridas = {'Insumo', 'Cantidad Disponible', 'Última Actualización'}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(f"Faltan columnas: {columnas_requeridas - set(df.columns)}")
    df['Última Actualización'] = pd.to_datetime(df['Última Actualización'])
    return df

def buscar_insumo(df):
    insumo = input("Nombre del insumo a buscar: ").strip()
    resultado = df[df['Insumo'].str.lower() == insumo.lower()]
    if resultado.empty:
        print("→ Insumo no encontrado.")
    else:
        print(resultado[['Insumo', 'Cantidad Disponible', 'Última Actualización']].to_string(index=False))

def ver_insumos_disponibles(df):
    if 'Cantidad Demandada' not in df.columns:
        print("No existe 'Cantidad Demandada'.")
        return
    disponibles = df[df['Cantidad Disponible'] >= df['Cantidad Demandada']]
    if disponibles.empty:
        print("→ No hay insumos disponibles según demanda.")
    else:
        print("\nInsumos disponibles para envío:")
        print(disponibles[['Insumo', 'Cantidad Disponible', 'Cantidad Demandada']].to_string(index=False))

def actualizar_insumo(df):
    insumo = input("Insumo a enviar: ").strip()
    try:
        cantidad = int(input("Cantidad a enviar: ").strip())
    except ValueError:
        print("→ Ingresa un número válido.")
        return df
    mask = df['Insumo'].str.lower() == insumo.lower()
    if not mask.any():
        print("→ Insumo no encontrado.")
        return df
    idx = df.index[mask][0]
    if cantidad > df.at[idx, 'Cantidad Disponible']:
        print("→ Cantidad supera la disponibilidad.")
        return df
    df.at[idx, 'Cantidad Disponible'] -= cantidad
    print(f"→ {insumo} provisionalmente descontado ({cantidad}).")
    return df

def confirmar_y_guardar(df):
    confirmacion = input("Confirma actualización? (Aceptar para guardar): ").strip()
    if confirmacion.lower() == 'aceptar':
        df.to_excel(inventario_actualizado, index=False)
        print(f"✅ Inventario guardado en '{inventario_actualizado}'.")
    else:
        print("❌ Actualización cancelada.")

# ------------------ Envío de correo con archivo adjunto ------------------ #
def enviar_correo(msg: EmailMessage):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

def generar_y_enviar_lista(df):
    if 'Cantidad Demandada' not in df.columns:
        print("No existe 'Cantidad Demandada'.")
        return
    disponibles = df[df['Cantidad Disponible'] >= df['Cantidad Demandada']]
    if disponibles.empty:
        print("→ No hay insumos que enviar.")
        return

    # Guardar Excel
    disponibles.to_excel(insumos_disponibles, index=False)
    print(f"✅ '{insumos_disponibles}' generado.")

    # Preparar correo
    msg = EmailMessage()
    msg['Subject'] = 'Lista de Insumos Disponibles'
    msg['From']    = EMAIL_USER
    msg['To']      = LEADER_EMAIL
    msg.set_content("Adjunto encontrarás el listado de insumos disponibles para envío.")

    with open(insumos_disponibles, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=os.path.basename(insumos_disponibles)
        )

    try:
        enviar_correo(msg)
        print(f"✉️ Enviado a {LEADER_EMAIL}")
    except Exception as e:
        print("Error al enviar correo:", e)

# ------------------ Autenticación de usuario ------------------ #
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

# ------------------ Menú principal ------------------ #
def mostrar_menu_opciones():
    try:
        filtro = FiltroPedidos(pedidos)
    except RuntimeError as e:
        print("❌", e)
        return

    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1. Consultar demanda de pedidos")
        print("2. Gestionar inventario")
        print("3. Opción tres (pendiente)")
        print("4. Opción cuatro (pendiente)")
        print("5. Opción cinco (pendiente)")
        print("6. Opción seis (pendiente)")
        print("7. Cerrar sesión")

        opcion = input("Elija una opción (1-7): ")
        match opcion:
            case "1":
                menu_consulta(filtro)
            case "2":
                menu_inventario()
            case "3" | "4" | "5" | "6":
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

# ------------------ Submenú: Gestión de inventario ------------------ #
def menu_inventario():
    try:
        df = cargar_inventario()
    except Exception as e:
        print("Error al cargar inventario:", e)
        return

    while True:
        print("\n== GESTIÓN DE INVENTARIO ==")
        print("1. Buscar insumo")
        print("2. Ver lista de insumos disponibles")
        print("3. Actualizar insumo (provisional)")
        print("4. Confirmar y guardar cambios")
        print("5. Volver al menú anterior")

        opcion = input("Elija una opción (1-5): ").strip()

        match opcion:
            case '1':
                buscar_insumo(df)
            case '2':
                submenu_insumos(df)
            case '3':
                df = actualizar_insumo(df)
            case '4':
                confirmar_y_guardar(df)
            case '5':
                break
            case _:
                print("❌ Opción inválida. Intenta de nuevo.")

# ------------------ Submenú: Insumos ------------------ #
def submenu_insumos(df):
    while True:
        print("\n== INSUMOS DISPONIBLES ==")
        print("1. Ver insumos que cumplen con la demanda")
        print("2. Enviar por correo lista de insumos")
        print("3. Volver al menú anterior")

        opcion = input("Elija una opción (1-3): ").strip()

        match opcion:
            case '1':
                ver_insumos_disponibles(df)
            case '2':
                generar_y_enviar_lista(df)
            case '3':
                break
            case _:
                print("❌ Opción inválida. Intenta de nuevo.")

# ------------------ Punto de entrada ------------------ #
if __name__ == "__main__":
    if iniciar_sesion():
        mostrar_menu_opciones()

        #1. Buscar Insumos (listo)
        #2. Mostrar lista de insumos (Producto Cantidad)
        #3. Generar lista de insumos listos para envio (Filtro de la tabla de demanda)
        #4. Enviar lista de insumos listos (configurarlo para q sea una opcion unica)
        #5. Actualizar inventario (Se le resta la lista de insumos enviados a la lista de insumos)