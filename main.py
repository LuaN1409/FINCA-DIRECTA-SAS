import pandas as pd
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

# ------------------ Rutas relativas a archivos Excel ------------------ #
pedidos = os.path.join(os.path.dirname(__file__), "data", "pedidos_granja.xlsx")
inventario = os.path.join(os.path.dirname(__file__), "data", "inventario.xlsx")
inventario_actualizado = os.path.join(os.path.dirname(__file__), "data", "inventario_actualizado.xlsx")
insumos_disponibles = os.path.join(os.path.dirname(__file__), "data", "insumos_disponibles.xlsx")
demanda = os.path.join(os.path.dirname(__file__),"data", "demanda.xlsx")
entregas = os.path.join(os.path.dirname(__file__),"data", "entregas.xlsx")
detalle_entregas = os.path.join(os.path.dirname(__file__),"data", "detalle_entregas.xlsx")
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
def cargar_excel(ruta):
    if os.path.exists(ruta):
        return pd.read_excel(ruta)
    return pd.DataFrame()

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

df_inventario = cargar_excel(inventario)
df_demanda = cargar_excel(demanda)

# Normaliza nombres
df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
df_demanda["producto_norm"] = df_demanda["producto"].astype(str).str.strip().str.lower()

# Función 1: Buscar insumo por nombre
def buscar_insumo(nombre):
    nombre = nombre.lower()
    resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre)]
    print("\nResultados de la búsqueda:")
    print(resultado[["producto", "cantidad", "ultima_actualizacion"]].to_string(index=False))

# Función 2: Mostrar lista completa de insumos
def mostrar_lista_insumos():
    print("\nInventario completo:")
    print(df_inventario[["producto", "cantidad", "ultima_actualizacion"]].to_string(index=False))

# Función 3: Generar lista de insumos listos para envío
def generar_lista_envio():
    merged = pd.merge(df_demanda, df_inventario, on="producto_norm", suffixes=("_demanda", "_inv"))
    listos = merged[merged["cantidad"] >= merged["total_cantidad"]]
    listos = listos[["producto_inv", "cantidad", "total_cantidad"]]
    listos.columns = ["producto", "cantidad_disponible", "cantidad_requerida"]

    print("\nLista de insumos listos para envío:")
    print(listos.to_string(index=False))
    return listos

# Función 4: Generar Excel con lista para envío
def exportar_lista_envio_excel(lista):
    ruta = os.path.join(os.path.dirname(inventario), "insumos_listos.xlsx")
    lista.to_excel(ruta, index=False)
    print(f"\n✅ Archivo generado: {ruta}")

# Función 5: Actualizar inventario con fecha
def actualizar_inventario():
    global df_inventario
    hoy = datetime.today().strftime("%Y-%m-%d")

    for _, row in df_demanda.iterrows():
        producto_norm = row["producto_norm"]
        cantidad_req = row["total_cantidad"]

        idx = df_inventario[df_inventario["producto_norm"] == producto_norm].index
        if not idx.empty:
            i = idx[0]
            df_inventario.at[i, "cantidad"] = max(0, df_inventario.at[i, "cantidad"] - cantidad_req)
            df_inventario.at[i, "ultima_actualizacion"] = hoy

    df_inventario.drop(columns=["producto_norm"], inplace=True)
    df_inventario.to_excel(inventario, index=False)
    print("\n📦 Inventario actualizado correctamente.")

# ------------------ Envío de correo con archivo adjunto ------------------ #
def enviar_lista_por_correo():
    archivo = os.path.join(os.path.dirname(inventario), "insumos_listos.xlsx")
    if not os.path.exists(archivo):
        print("❌ El archivo 'insumos_listos.xlsx' no existe. Primero genera la lista (opción 4).")
        return

    email_remitente = "elcoordinadordecompras@gmail.com"
    contraseña = "iocsdhwphxxhbzzp"
    destinatario = input("Correo del destinatario: ")

    mensaje = EmailMessage()
    mensaje["Subject"] = "📦 Lista de insumos listos para envío"
    mensaje["From"] = email_remitente
    mensaje["To"] = destinatario
    mensaje.set_content("Hola, adjunto encontrarás la lista de insumos que cumplen la demanda.")

    with open(archivo, "rb") as f:
        mensaje.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="insumos_listos.xlsx"
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_remitente, contraseña)
            smtp.send_message(mensaje)
            print("📧 Correo enviado exitosamente.")
    except Exception as e:
        print("❌ Error al enviar el correo:", e)

def guardar_excel(df, ruta):
    try:
        df.to_excel(ruta, index=False)
    except PermissionError:
        print(f"❌ No se pudo guardar '{ruta}' porque está abierto en otro programa (como Excel).")
        print("🔁 Por favor, ciérralo y vuelve a intentarlo.")

def guardar_detalle_entrega(productos, id_entrega, ruta=detalle_entregas):
    df_detalle = cargar_excel(ruta)
    nuevas_filas = pd.DataFrame(
        [(id_entrega, nombre, cantidad) for nombre, cantidad in productos],
        columns=["id_entrega", "producto", "cantidad"]
    )
    df_detalle = pd.concat([df_detalle, nuevas_filas], ignore_index=True)
    guardar_excel(df_detalle, ruta)

def registrar_recepcion():
    print("\n--- Registrar información del pedido de los insumos recibidos ---")
    proveedor = input("Nombre del proveedor: ")
    fecha = input("Fecha de recepción (YYYY-MM-DD): ")
    numero_pedido = input("Número de pedido: ")

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        print("Fecha inválida. Debe tener formato YYYY-MM-DD.")
        return None

    cantidades_entregadas = int(input("Cantidad de productos diferentes entregados: "))
    productos = []
    for _ in range(cantidades_entregadas):
        nombre = input("Nombre del producto: ")
        cantidad = int(input(f"Cantidad de '{nombre}': "))
        productos.append((nombre, cantidad))

    df_entregas = cargar_excel(entregas)
    nuevo_id = 1 if df_entregas.empty else df_entregas['id'].max() + 1
    nueva_entrega = pd.DataFrame([[nuevo_id, proveedor, fecha, numero_pedido, cantidades_entregadas]],
                                  columns=["id", "proveedor", "fecha", "numero_pedido", "cantidades_entregadas"])
    df_entregas = pd.concat([df_entregas, nueva_entrega], ignore_index=True)
    guardar_excel(df_entregas, entregas)

    guardar_detalle_entrega(productos, nuevo_id)  # <-- nuevo: guardar detalle productos

    return productos

def validar_campos(productos):
    print("\n--- Validar campos de ingreso de datos ---")
    for nombre, cantidad in productos:
        if not nombre or cantidad <= 0:
            print(f"Error: Producto '{nombre}' tiene datos inválidos.")
            return False
    print("Todos los campos son válidos.")
    return True

def verificar_insumos(productos):
    print("\n--- Verificar cantidad y calidad del insumo ---")
    validados = []
    for nombre, cantidad in productos:
        estado = input(f"Producto '{nombre}' ({cantidad} unidades). ¿Está Conforme? (s/n): ").lower()
        if estado == 's':
            validados.append((nombre, cantidad))
    return validados

def ingresar_inventario(productos_validados):
    print("\n--- Ingresar insumos conformes al inventario ---")
    df_inv = cargar_excel(inventario)

    # Crear columnas si están ausentes
    if df_inv.empty or 'producto' not in df_inv.columns or 'cantidad' not in df_inv.columns:
        df_inv = pd.DataFrame(columns=["producto", "cantidad", "ultima_actualizacion"])

    # Asegurar que 'ultima_actualizacion' existe
    if 'ultima_actualizacion' not in df_inv.columns:
        df_inv['ultima_actualizacion'] = None

    # Normalizar para evitar duplicados por mayúsculas
    df_inv['producto_normalizado'] = df_inv['producto'].astype(str).str.strip().str.lower()
    hoy = datetime.today().strftime('%Y-%m-%d')

    for nombre, cantidad in productos_validados:
        nombre_original = nombre.strip()
        nombre_normalizado = nombre_original.lower()

        if nombre_normalizado in df_inv['producto_normalizado'].values:
            index = df_inv[df_inv['producto_normalizado'] == nombre_normalizado].index[0]
            df_inv.at[index, 'cantidad'] += cantidad
            df_inv.at[index, 'ultima_actualizacion'] = hoy
        else:
            nueva_fila = pd.DataFrame([[nombre_original, cantidad, hoy]], columns=["producto", "cantidad", "ultima_actualizacion"])
            df_inv = pd.concat([df_inv, nueva_fila], ignore_index=True)

    #Eliminar ultima columna
    df_inv = df_inv.drop(columns=["producto_normalizado"])
    guardar_excel(df_inv, inventario)
    print("Inventario actualizado correctamente.")

# Variable global para almacenar el resultado del filtro actual
reporte_filtrado = pd.DataFrame()

# 1. FILTRAR POR FECHAS
def filtrar_por_fechas():
    global reporte_filtrado
    df_entregas = pd.read_excel(entregas)
    if df_entregas.empty:
        print("No hay entregas registradas.")
        return

    fecha_ini = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    try:
        df_entregas['fecha'] = pd.to_datetime(df_entregas['fecha'])
        ini = pd.to_datetime(fecha_ini)
        fin = pd.to_datetime(fecha_fin)
    except:
        print("❌ Formato de fecha inválido.")
        return

    reporte_filtrado = df_entregas[(df_entregas['fecha'] >= ini) & (df_entregas['fecha'] <= fin)]
    if reporte_filtrado.empty:
        print("🔍 No hay entregas en ese rango de fechas.")
    else:
        print("\n📄 Reportes disponibles:")
        for i, row in reporte_filtrado.iterrows():
            print(f"{row['id']}. Pedido {row['numero_pedido']} | {row['fecha'].strftime('%Y-%m-%d')} | Proveedor: {row['proveedor']}")

# 2. SELECCIONAR REPORTE ESPECIFICO
def seleccionar_reporte():
    global reporte_filtrado
    if reporte_filtrado.empty:
        print("❌ Primero debes filtrar por fechas.")
        return

    id_sel = input("Ingrese el ID del reporte que desea ver: ")
    if not id_sel.isdigit():
        print("❌ ID inválido.")
        return
    id_sel = int(id_sel)

    df_detalle = pd.read_excel(detalle_entregas)
    if id_sel not in reporte_filtrado['id'].values:
        print("❌ El ID seleccionado no pertenece al filtro actual.")
        return

    info = reporte_filtrado[reporte_filtrado['id'] == id_sel].iloc[0]
    detalle = df_detalle[df_detalle['id_entrega'] == id_sel]

    print("\n📦 Detalle del reporte seleccionado:")
    print(f"Proveedor: {info['proveedor']}")
    print(f"Fecha de entrega: {info['fecha'].strftime('%Y-%m-%d')}")
    print(f"Número de pedido: {info['numero_pedido']}")
    print(f"Cantidad de productos diferentes: {info['cantidades_entregadas']}")
    print("\nProductos entregados:")

    if "conforme" not in detalle.columns:
        detalle["conforme"] = True  # Por compatibilidad, se asume conforme si no está

    for _, row in detalle.iterrows():
        estado = "✅ Conforme" if row["conforme"] else "❌ No conforme"
        print(f" - {row['producto']}: {row['cantidad']} unidades → {estado}")

    # Guardar como Excel limpio para descarga con estado legible
    salida = detalle.copy()
    salida.insert(0, "Proveedor", info['proveedor'])
    salida.insert(1, "Fecha", info['fecha'].strftime('%Y-%m-%d'))
    salida.insert(2, "Pedido", info['numero_pedido'])
    salida['conformidad'] = salida['conforme'].apply(lambda x: "Conforme" if x else "No conforme")
    salida = salida[["Proveedor", "Fecha", "Pedido", "producto", "cantidad", "conformidad"]]

    nombre_archivo = os.path.join(os.path.dirname(entregas), f"reporte_pedido_{id_sel}.xlsx")
    salida.to_excel(nombre_archivo, index=False)
    print(f"\n✅ El reporte ha sido generado como '{nombre_archivo}'.")

# 3. DESCARGAR REPORTE
# (En consola ya se guarda automáticamente, aquí solo avisamos)
def descargar_reporte():
    carpeta = os.path.dirname(entregas)
    archivos = [f for f in os.listdir(carpeta) if f.startswith("reporte_pedido_") and f.endswith(".xlsx")]
    if not archivos:
        print("❌ No hay reporte generado para descargar. Primero selecciona uno.")
    else:
        print("📥 Reportes disponibles en la carpeta 'data/':")
        for archivo in archivos:
            print(" -", archivo)

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
        print("3. Recepcion de insumos")
        print("4. Reportes de recepción de insumos")
        print("5. Opción cinco (pendiente)")
        print("6. Opción seis (pendiente)")
        print("7. Cerrar sesión")

        opcion = input("Elija una opción (1-7): ")
        match opcion:
            case "1":
                menu_consulta(filtro)
            case "2":
                menu_inventario()
            case "3":
                menu_recepcion()
            case "4":
                menu_reportes()
            case "5" | "6":
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
        print("9. Volver al menú principal")

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
    while True:
        print("\n== GESTIONAR INVENTARIO ==")
        print("1. Buscar insumo por nombre")
        print("2. Mostrar lista completa de insumos")
        print("3. Generar lista de insumos listos para envío")
        print("4. Exportar lista de insumos listos a Excel")
        print("5. Actualizar inventario con demanda")
        print("6. Enviar lista por correo")
        print("7. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
    
        if opcion == "1":
            nombre = input("Ingrese el nombre del insumo: ")
            buscar_insumo(nombre)
        elif opcion == "2":
            mostrar_lista_insumos()
        elif opcion == "3":
            lista_envio = generar_lista_envio()
        elif opcion == "4":
            try:
                exportar_lista_envio_excel(lista_envio)
            except NameError:
                print("Primero debe generar la lista con la opción 3.")
        elif opcion == "5":
            actualizar_inventario()
        elif opcion == "6":
            enviar_lista_por_correo()
        elif opcion == "7":
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

# ------------------ Submenú: Recepcion de insumos ------------------ #
def menu_recepcion():
    productos = []
    while True:
        print("\n=== RECEPCION DE INSUMOS ===")
        print("1. Registrar información del pedido")
        print("2. Validar campos de ingreso de datos")
        print("3. Verificar cantidad y calidad del insumo")
        print("4. Ingresar insumos conformes al inventario")
        print("5. Volver al menú principal")
        opcion = input("Elija una opción (1-5): ")

        if opcion == "1":
            productos = registrar_recepcion() or []
        elif opcion == "2":
            if not validar_campos(productos):
                productos = []  # borra productos inválidos
        elif opcion == "3":
            productos = verificar_insumos(productos)
        elif opcion == "4":
            ingresar_inventario(productos)
            productos = []
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

# ------------------ Submenú: Reportes de recepcion de insumos ------------------ #
def menu_reportes():
    while True:
        print("\n=== REPORTES DE RECEPCION DE INSUMOS ===")
        print("1. Filtrar por fechas")
        print("2. Seleccionar reporte específico")
        print("3. Descargar reporte")
        print("4. Volver al menú principal")
        op = input("Seleccione una opción: ")
        if op == "1":
            filtrar_por_fechas()
        elif op == "2":
            seleccionar_reporte()
        elif op == "3":
            descargar_reporte()
        elif op == "4":
            break
        else:
            print("❌ Opción inválida")
# ------------------ Punto de entrada ------------------ #

if __name__ == "__main__":
    if iniciar_sesion():
        mostrar_menu_opciones()

        #1. Buscar Insumos por nombre(listo)
        #2. Mostrar lista de insumos (producto | cantidad | ultima_actualizacion)
        #3. Generar lista de insumos listos para envio (Son todos los productos de la lista de demanda que su cantidad es menor a la de la cantidad de la lista de insumos)
        #4. Enviar lista de insumos listos (debe generar un archivo descargable en Excel con la lista generada y enviarlo automáticamente al correo configurado del líder de Producción)
        #5. Actualizar inventario (Se le resta la lista de los insumos de demanda a la lista de insumos)