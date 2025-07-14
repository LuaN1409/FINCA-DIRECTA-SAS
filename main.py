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
                print("📦 ID de pedido:")
                print(self.df_filtrado['id'].to_string(index=False))
        except Exception:
            print("⚠ Formato de fecha inválido. Intenta con el formato YYYY-MM-DD.")

    def filtrar_por_producto(self):
        nombre = input("📦 Nombre del producto (puede ser parcial o ENTER para omitir): ")
        if nombre:
            self.df_filtrado = self.df_filtrado[
                self.df_filtrado['producto'].str.lower().str.contains(nombre.lower(), na=False)
            ]
            if self.df_filtrado.empty:
                print(f"⚠ No se encontraron pedidos del producto '{nombre}'.")
            else:
                print(f"🔍 Pedidos con producto '{nombre}':")
                print("📦 ID de pedido:")
                print(self.df_filtrado['id'].to_string(index=False))

    def filtrar_combinado(self):
        nombre = input("📦 Nombre del producto: ")
        inicio = input("📅 Fecha desde (YYYY-MM-DD o ENTER para omitir): ")
        fin = input("📅 Fecha hasta (YYYY-MM-DD o ENTER para omitir): ")
        try:
            df_temp = self.df.copy()
            if nombre:
                df_temp = df_temp[df_temp['producto'].str.lower().str.contains(nombre.lower(), na=False)]

            if inicio:
                inicio_dt = pd.to_datetime(inicio)
            else:
                inicio_dt = df_temp['fecha'].min()
            if fin:
                fin_dt = pd.to_datetime(fin)
            else:
                fin_dt = df_temp['fecha'].max()

            df_temp = df_temp[df_temp['fecha'].between(inicio_dt, fin_dt)]
            self.df_filtrado = df_temp

            if self.df_filtrado.empty:
                print("⚠ No se encontraron pedidos con ese producto y rango de fechas.")
            else:
                print(f"🔍 Pedidos con '{nombre}' entre {inicio_dt.date()} y {fin_dt.date()}:")
                print(self.df_filtrado['id'].to_string(index=False))
        except Exception:
            print("⚠ Error al aplicar filtros combinados.")

    def mostrar_detalle_pedido(self):
        if self.df_filtrado.empty:
            print("⚠ No hay pedidos disponibles para ver detalles.")
            return
        try:
            numero = input("🔎 Ingrese el ID del pedido a consultar: ")
            detalle = self.df_filtrado[self.df_filtrado['id'].astype(str) == numero]
            if not detalle.empty:
                print("\n📌 Detalle del pedido:")
                fila = detalle.iloc[0].copy()
                for campo, valor in fila.items():
                    if campo == "id":
                        print(f"- ID: {valor}")
                    else:
                        print(f"- {campo.capitalize()}: {valor}")
            else:
                print("❌ ID de pedido no encontrado en los filtrados.")
        except:
            print("❌ Entrada no válida. Ingrese un número correcto.")

    def reiniciar_filtros(self):
        self.df_filtrado = self.df.copy()
        print("🔁 Filtros reiniciados.")

    def exportar_resultados(self):
        if self.df_filtrado.empty:
            print("⚠ No hay datos para exportar.")
            return
        try:
            resumen = self.df_filtrado.groupby('producto', as_index=False)['cantidad'].sum()
            resumen.columns = ['producto', 'total_cantidad']
            resumen.to_excel(demanda, index=False)
            print(f"✅ Resultados exportados a '{demanda}'")
            self.reiniciar_filtros()
        except PermissionError:
            print(f"❌ No se pudo exportar '{demanda}' porque está abierto en otro programa (como Excel).")
            print("🔁 Por favor, ciérralo y vuelve a intentarlo.")
        except Exception as e:
            print("❌ Error al exportar:", e)

df_inventario = cargar_excel(inventario)
df_demanda = cargar_excel(demanda)

# Normaliza nombres
df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
df_demanda["producto_norm"] = df_demanda["producto"].astype(str).str.strip().str.lower()

# Función 1: Buscar insumo por nombre
def buscar_insumo(nombre):
    df_inventario = cargar_excel(inventario)
    df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
    nombre = nombre.lower()
    resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre)]
    if resultado.empty:
        print("❌ No se encontraron insumos con ese nombre.")
    else:
        print("\nResultado de la búsqueda:")
        print(resultado[["producto", "cantidad", "ultima_actualizacion"]].to_string(index=False))

# Función 2: Mostrar lista completa de insumos (solo id 0-17, nombre y cantidad)
def mostrar_lista_insumos():
    df_inventario = cargar_excel(inventario)
    print("\nInventario completo:")
    print(df_inventario.loc[0:17, ["producto", "cantidad"]].to_string(index=True))

# Función 3: Ver detalle por ID
def ver_detalle_insumo():
    df_inventario = cargar_excel(inventario)
    try:
        idx = int(input("🔍 Ingrese el ID del insumo (0-17): "))
        if 0 <= idx <= 17 and idx < len(df_inventario):
            fila = df_inventario.loc[idx]
            print("\n📦 Detalle del insumo:")
            print(f"Producto: {fila['producto']}")
            print(f"Cantidad: {fila['cantidad']}")
            print(f"Última actualización: {fila['ultima_actualizacion']}")
        else:
            print("❌ ID fuera de rango.")
    except:
        print("❌ Entrada inválida. Ingrese un número entero.")


def obtener_lista_insumos_listos():
    df_inventario = cargar_excel(inventario)
    df_demanda = cargar_excel(demanda)

    df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
    df_demanda["producto_norm"] = df_demanda["producto"].astype(str).str.strip().str.lower()

    merged = pd.merge(df_demanda, df_inventario, on="producto_norm", suffixes=("_demanda", "_inv"))
    listos = merged[merged["cantidad"] >= merged["total_cantidad"]]
    listos = listos[["producto_inv", "total_cantidad"]]
    listos.columns = ["producto", "cantidad_a_enviar"]
    return listos


# Función 4: Generar lista de insumos listos para envío (sin exportar ni enviar)
def generar_lista_envio():
    lista = obtener_lista_insumos_listos()
    return lista

# Función 5: Exportar lista y enviar por Gmail (correo fijo)
def enviar_lista_insumos():
    lista = obtener_lista_insumos_listos()  # Esta ya NO imprime nada
    if lista.empty:
        print("❌ No hay insumos que cumplan con la demanda.")
        return

    ruta = os.path.join(os.path.dirname(inventario), "insumos_listos.xlsx")
    lista.to_excel(ruta, index=False)
    print(f"\n✅ Archivo generado: {ruta}")

    # Enviar por correo
    archivo = ruta
    email_remitente = "elcoordinadordecompras@gmail.com"
    contraseña = "iocsdhwphxxhbzzp"
    destinatario = "jarinconb8@gmail.com"

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

# Función 6: Actualizar inventario con fecha
def actualizar_inventario():
    df_inventario = cargar_excel(inventario)
    df_demanda = cargar_excel(demanda)
    df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
    df_demanda["producto_norm"] = df_demanda["producto"].astype(str).str.strip().str.lower()

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
        estado = input(f"Producto '{nombre}' ({cantidad} unidades). ¿Está Conforme? (Conforme/No conforme): ").strip().lower()
        if estado == 'conforme':
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
    print("✅ Inventario actualizado correctamente.")


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
    detalle = df_detalle[df_detalle['id_entrega'] == id_sel].copy()  # <-- Añade .copy()
    if "conforme" not in detalle.columns:
        detalle["conforme"] = True  # Por compatibilidad, se asume conforme si no está

    for _, row in detalle.iterrows():
        estado = "✅ Conforme" if row["conforme"] else "❌ No conforme"

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

# ------------------ Inicio de Sesion ------------------ #
usuarios_path = os.path.join(os.path.dirname(__file__), "data", "usuarios.xlsx")
clave_maestra = "FDsas/25"

def cargar_usuarios():
    if os.path.exists(usuarios_path):
        return pd.read_excel(usuarios_path)
    else:
        return pd.DataFrame(columns=["correo", "contraseña"])

def guardar_usuarios(df):
    df.to_excel(usuarios_path, index=False)

def iniciar_sesion():
    print("\n=== AUTENTICACIÓN DEL SISTEMA ===")
    usuarios_df = cargar_usuarios()

    while True:
        print("\n1. Iniciar sesión")
        print("2. Crear cuenta nueva")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            correo = input("📧 Correo: ").strip()
            contraseña = input("🔒 Contraseña: ").strip()

            if not correo or not contraseña:
                print("❌ Todos los campos son obligatorios.")
                continue

            encontrado = usuarios_df[
                (usuarios_df["correo"].str.strip().str.lower() == correo.lower()) &
                (usuarios_df["contraseña"] == contraseña)
            ]

            if not encontrado.empty:
                print("✅ Inicio de sesión exitoso.")
                return True
            else:
                print("❌ Correo o contraseña incorrectos.")

        elif opcion == "2":
            correo = input("📧 Nuevo correo: ").strip()
            contraseña_nueva = input("🔒 Nueva contraseña: ").strip()
            clave = input("🔑 Clave maestra para crear cuenta: ").strip()

            if not correo or not contraseña_nueva or not clave:
                print("❌ Todos los campos son obligatorios.")
                continue

            if clave != clave_maestra:
                print("❌ Clave maestra incorrecta. No se puede crear la cuenta.")
                continue

            if correo.lower() in usuarios_df["correo"].str.lower().values:
                print("❌ Ya existe una cuenta con ese correo.")
                continue

            nuevo = pd.DataFrame([[correo, contraseña_nueva]], columns=["correo", "contraseña"])
            usuarios_df = pd.concat([usuarios_df, nuevo], ignore_index=True)
            guardar_usuarios(usuarios_df)
            print("✅ Cuenta creada exitosamente. Ahora puedes iniciar sesión.")

        elif opcion == "3":
            print("👋 Saliendo del sistema.")
            return False

        else:
            print("❌ Opción inválida. Intente nuevamente.")

# ------------------ HU3 ------------------ #

def obtener_insumos_faltantes():
    inv = cargar_excel(inventario)
    dem = cargar_excel(demanda)
    inv["producto_norm"] = inv["producto"].str.lower().str.strip()
    dem["producto_norm"] = dem["producto"].str.lower().str.strip()
    
    merged = pd.merge(dem, inv, on="producto_norm", how="left", suffixes=("_dem", "_inv"))
    faltantes = merged[(merged["cantidad"].isna()) | (merged["cantidad"] < merged["total_cantidad"])]

    faltantes["cantidad"] = faltantes.apply(
        lambda row: row["total_cantidad"] if pd.isna(row["cantidad"]) else row["total_cantidad"] - row["cantidad"],
        axis=1
    )
    faltantes["id"] = faltantes["id"].fillna(-1).astype(int)
    faltantes["producto"] = faltantes["producto_dem"]
    return faltantes[["id", "producto", "cantidad"]].copy()

solicitud_actual = pd.DataFrame()

def menu_generar_solicitud():
    global solicitud_actual
    solicitud_actual = obtener_insumos_faltantes()

    if solicitud_actual.empty:
        print("\n✅ No hay productos faltantes. Toda la demanda está cubierta.")
        return

    while True:
        print("\n=== SOLICITUD DE COMPRA DE INSUMOS ===")
        print("1. Mostrar sugerencia de solicitud")
        print("2. Editar solicitud")
        print("3. Validar información")
        print("4. Guardar solicitud")
        print("5. Enviar solicitud")
        print("6. Volver")
        op = input("Seleccione una opción: ")

        if op == "1":
            print("\n📦 Insumos sugeridos para solicitar:")
            print(solicitud_actual.to_string(index=False))

        elif op == "2":
            editar_solicitud()

        elif op == "3":
            validar_solicitud()

        elif op == "4":
            guardar_excel(solicitud_actual, os.path.join(os.path.dirname(inventario), "solicitud_compra.xlsx"))
            print("✅ Solicitud guardada correctamente.")

        elif op == "5":
            enviar_solicitud()

        elif op == "6":
            break
        else:
            print("❌ Opción inválida.")

def editar_solicitud():
    global solicitud_actual
    while True:
        print("\n--- EDITAR SOLICITUD ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Modificar cantidad")
        print("4. Volver")
        op = input("Seleccione una opción: ")

        if op == "1":
            nombre = input("Nombre del producto: ")
            cantidad = input("Cantidad: ")
            if not cantidad.isdigit() or int(cantidad) <= 0:
                print("❌ Cantidad inválida.")
                continue
            nueva_fila = pd.DataFrame([[999, nombre.strip(), int(cantidad)]], columns=["id", "producto", "cantidad"])
            solicitud_actual = pd.concat([solicitud_actual, nueva_fila], ignore_index=True)
            print("✅ Producto agregado.")

        elif op == "2":
            nombre = input("Nombre del producto a eliminar: ").strip().lower()
            original_len = len(solicitud_actual)
            solicitud_actual = solicitud_actual[~solicitud_actual["producto"].str.lower().str.strip().eq(nombre)]
            if len(solicitud_actual) < original_len:
                print("✅ Producto eliminado.")
            else:
                print("❌ Producto no encontrado.")

        elif op == "3":
            nombre = input("Nombre del producto a modificar: ").strip().lower()
            if nombre not in solicitud_actual["producto"].str.lower().str.strip().values:
                print("❌ Producto no encontrado.")
                continue
            cantidad = input("Nueva cantidad: ")
            if not cantidad.isdigit() or int(cantidad) <= 0:
                print("❌ Cantidad inválida.")
                continue
            idx = solicitud_actual[solicitud_actual["producto"].str.lower().str.strip() == nombre].index[0]
            solicitud_actual.at[idx, "cantidad"] = int(cantidad)
            print("✅ Cantidad actualizada.")

        elif op == "4":
            break
        else:
            print("❌ Opción inválida.")

def validar_solicitud():
    errores = []
    for _, row in solicitud_actual.iterrows():
        if not row["producto"] or not isinstance(row["cantidad"], (int, float)):
            errores.append(f"❌ Producto inválido o sin cantidad: {row.to_dict()}")
        elif row["cantidad"] <= 0:
            errores.append(f"❌ Cantidad inválida para producto '{row['producto']}': {row['cantidad']}")

    if errores:
        print("\n❌ Se encontraron errores en la solicitud:")
        for e in errores:
            print("-", e)
    else:
        print("✅ Toda la información de la solicitud es válida.")

def enviar_solicitud():
    archivo = os.path.join(os.path.dirname(inventario), "solicitud_compra.xlsx")
    if not os.path.exists(archivo):
        print("❌ No se ha guardado la solicitud aún.")
        return

    email_remitente = "elcoordinadordecompras@gmail.com"
    contraseña = "iocsdhwphxxhbzzp"
    destinatario = "jurinconba@unal.edu.co"

    mensaje = EmailMessage()
    mensaje["Subject"] = "📋 Solicitud de compra de insumos"
    mensaje["From"] = email_remitente
    mensaje["To"] = destinatario
    mensaje.set_content("Adjunto se encuentra la solicitud de compra de insumos para cumplir la demanda.")

    with open(archivo, "rb") as f:
        mensaje.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="solicitud_compra.xlsx"
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_remitente, contraseña)
            smtp.send_message(mensaje)
            print("📧 Solicitud enviada correctamente.")
    except Exception as e:
        print("❌ Error al enviar la solicitud:", e)

# ------------------ HU6 ------------------ #
# Ruta donde se guardará el archivo del reporte de defectuosos
reporte_defectuosos = os.path.join(os.path.dirname(__file__), "data", "reporte_insumos_defectuosos.xlsx")

def menu_reportar_defectuosos():
    """
    Este menú permite al usuario:
    1. Crear un nuevo reporte de insumos defectuosos.
    2. Guardar el reporte en un archivo Excel.
    3. Enviar el reporte por correo al equipo encargado.
    4. Salir del menú.
    """
    reporte = []  # Lista para almacenar temporalmente los reportes ingresados

    while True:
        print("\n=== REPORTE DE INSUMOS DEFECTUOSOS ===")
        print("1. Crear nuevo reporte")
        print("2. Guardar reporte en Excel")
        print("3. Enviar reporte por correo")
        print("4. Volver al menú anterior")
        opcion = input("Seleccione una opción: ")

        # Opción 1: Crear nuevo reporte
        if opcion == "1":
            reporte.clear()  # Limpia el reporte anterior si existía
            while True:
                proveedor = input("Nombre del proveedor: ").strip()
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                producto = input("Nombre del producto: ").strip()
                defecto = input("Tipo de defecto (cantidad/calidad): ").strip().lower()
                observaciones = input("Observaciones (opcional): ").strip()

                # Validación del tipo de defecto
                if defecto not in ["cantidad", "calidad"]:
                    print("❌ Tipo de defecto inválido. Solo se permite 'cantidad' o 'calidad'.")
                    continue

                # Validación de la fecha
                try:
                    datetime.strptime(fecha, "%Y-%m-%d")
                except ValueError:
                    print("❌ Fecha inválida. Formato correcto: YYYY-MM-DD.")
                    continue

                # Confirmación antes de registrar
                confirmar = input("¿Confirmar reporte? (y/n): ").strip().lower()
                if confirmar == "y":
                    # Validación de campos obligatorios
                    if not proveedor or not producto or not defecto:
                        print("❌ Faltan campos obligatorios.")
                        continue

                    # Se guarda temporalmente el reporte
                    reporte.append([proveedor, fecha, producto, defecto, observaciones])
                    print("✅ Reporte creado correctamente.")
                    break
                else:
                    print("🔁 Reiniciando captura de datos...")

        # Opción 2: Guardar el reporte en archivo Excel
        elif opcion == "2":
            if not reporte:
                print("❌ No hay reporte cargado.")
                continue
            df = pd.DataFrame(reporte, columns=["proveedor", "fecha", "producto", "tipo_defecto", "observaciones"])
            df.to_excel(reporte_defectuosos, index=False)
            print(f"✅ Reporte guardado en '{reporte_defectuosos}'")

        # Opción 3: Enviar el archivo Excel por correo
        elif opcion == "3":
            if not os.path.exists(reporte_defectuosos):
                print("❌ No se ha generado ningún archivo aún.")
                continue

            # Parámetros del correo
            archivo = reporte_defectuosos
            email_remitente = "elcoordinadordecompras@gmail.com"
            contraseña = "iocsdhwphxxhbzzp"  # Contraseña de aplicación
            destinatario = "jurinconba@unal.edu.co"  # Correo de destino

            # Crear el mensaje
            mensaje = EmailMessage()
            mensaje["Subject"] = "❗Reporte de Insumos Defectuosos"
            mensaje["From"] = email_remitente
            mensaje["To"] = destinatario
            mensaje.set_content("Adjunto reporte de insumos defectuosos.")

            # Adjuntar el archivo
            with open(archivo, "rb") as f:
                mensaje.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename="reporte_defectuosos.xlsx"
                )

            # Enviar el correo
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(email_remitente, contraseña)
                    smtp.send_message(mensaje)
                    print("📧 Reporte enviado correctamente.")
            except Exception as e:
                print("❌ Error al enviar el correo:", e)

        # Opción 4: Salir del menú
        elif opcion == "4":
            break

        else:
            print("❌ Opción inválida.")

# ------------------ Módulo: Reportes de Solicitudes de Compra ------------------ #
ruta_solicitudes = os.path.join(os.path.dirname(__file__), "data", "solicitudes_compras.xlsx")
ruta_listos = os.path.join(os.path.dirname(__file__), "data", "insumos_listos_general.xlsx")

reporte_solicitudes = pd.DataFrame()
reporte_listos = pd.DataFrame()

def filtrar_solicitudes_fecha():
    global reporte_solicitudes
    df = pd.read_excel(ruta_solicitudes)
    if df.empty:
        print("❌ No hay solicitudes registradas.")
        return

    ini = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    try:
        df['fecha'] = pd.to_datetime(df['fecha'])
        ini_dt = pd.to_datetime(ini)
        fin_dt = pd.to_datetime(fin)
        reporte_solicitudes = df[(df['fecha'] >= ini_dt) & (df['fecha'] <= fin_dt)]
    except:
        print("❌ Fechas inválidas.")
        return

    if reporte_solicitudes.empty:
        print("🔍 No hay solicitudes en ese rango.")
    else:
        print("\n📄 Solicitudes disponibles:")
        for i, row in reporte_solicitudes.groupby('id').first().iterrows():
            print(f"ID: {i} | Fecha: {row['fecha'].date()} | Proveedor: {row['proveedor']}")

def seleccionar_reporte_solicitud():
    global reporte_solicitudes
    if reporte_solicitudes.empty:
        print("❌ Primero debes filtrar por fecha.")
        return

    id_sel = input("Ingrese el ID del reporte que desea ver: ")
    if not id_sel.isdigit():
        print("❌ ID inválido.")
        return

    id_sel = int(id_sel)
    detalle = reporte_solicitudes[reporte_solicitudes['id'] == id_sel].copy()
    if detalle.empty:
        print("❌ ID no encontrado.")
        return

    archivo = os.path.join(os.path.dirname(ruta_solicitudes), f"reporte_solicitud_{id_sel}.xlsx")
    detalle.to_excel(archivo, index=False)
    print(f"\n✅ Reporte guardado en '{archivo}'")

def descargar_reporte_solicitud():
    carpeta = os.path.dirname(ruta_solicitudes)
    archivos = [f for f in os.listdir(carpeta) if f.startswith("reporte_solicitud_") and f.endswith(".xlsx")]
    if not archivos:
        print("❌ No hay reportes generados.")
    else:
        print("📥 Reportes disponibles en la carpeta 'data/':")
        for archivo in archivos:
            print(" -", archivo)

# ------------------ Módulo: Reportes de Insumos Listos ------------------ #
def filtrar_listos_fecha():
    global reporte_listos
    df = pd.read_excel(ruta_listos)
    if df.empty:
        print("❌ No hay registros de insumos listos.")
        return

    ini = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    try:
        df['fecha'] = pd.to_datetime(df['fecha'])
        ini_dt = pd.to_datetime(ini)
        fin_dt = pd.to_datetime(fin)
        reporte_listos = df[(df['fecha'] >= ini_dt) & (df['fecha'] <= fin_dt)]
    except:
        print("❌ Fechas inválidas.")
        return

    if reporte_listos.empty:
        print("🔍 No hay insumos listos en ese rango.")
    else:
        print("\n📄 Reportes disponibles:")
        for i, row in reporte_listos.groupby('id').first().iterrows():
            print(f"ID: {i} | Fecha: {row['fecha'].date()} | Producto: {row['producto']}")

def seleccionar_reporte_listos():
    global reporte_listos
    if reporte_listos.empty:
        print("❌ Primero debes filtrar por fecha.")
        return

    id_sel = input("Ingrese el ID del reporte que desea ver: ")
    if not id_sel.isdigit():
        print("❌ ID inválido.")
        return

    id_sel = int(id_sel)
    detalle = reporte_listos[reporte_listos['id'] == id_sel].copy()
    if detalle.empty:
        print("❌ ID no encontrado.")
        return

    archivo = os.path.join(os.path.dirname(ruta_listos), f"reporte_insumos_listos_{id_sel}.xlsx")
    detalle.to_excel(archivo, index=False)
    print(f"\n✅ Reporte guardado en '{archivo}'")

def descargar_reporte_listos():
    carpeta = os.path.dirname(ruta_listos)
    archivos = [f for f in os.listdir(carpeta) if f.startswith("reporte_insumos_listos_") and f.endswith(".xlsx")]
    if not archivos:
        print("❌ No hay reportes generados.")
    else:
        print("📥 Reportes disponibles en la carpeta 'data/':")
        for archivo in archivos:
            print(" -", archivo)

# ------------------ Menú principal ------------------ #
def mostrar_menu_opciones():
    try:
        filtro = FiltroPedidos(pedidos)
    except RuntimeError as e:
        print("❌", e)
        return

    while True:
        print("\n=== MENÚ DE OPCIONES ===")
        print("1. Consultar demanda de pedidos (HU4)")
        print("2. Consultar inventario (HU1)")
        print("3. Verificar disponibilidad de insumos (HU2)")
        print("4. Recepcion de insumos (HU5)")
        print("5. Reportes de recepción de insumos (HU7)")
        print("6. Reportes de solicitudes de compra (HU8)")
        print("7. Reportes de insumos listos para envío (HU10)")
        print("0. Cerrar sesión")

        opcion = input("Elija una opción: ")
        match opcion:
            case "1":
                menu_consulta(filtro)
            case "2":
                menu_inventario()
            case "3":
                menu_envio()
            case "4":
                menu_recepcion()
            case "5":
                menu_reportes()
            case "6":
                menu_reportes_solicitudes()
            case "7":
                menu_reportes_insumos_listos()
            case "0":
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
        print("3. Filtrar pedidos producto y fecha")
        print("4. Ver detalle de un pedido específico")
        print("5. Exportar resultados")
        print("6. Reiniciar filtros")
        print("7. Volver al menú principal")

        opcion = input("Elija una opción: ").strip().lower()

        if opcion in ['7', 'salir']:
            break
        elif opcion == "1":
            filtro.filtrar_por_fecha()
        elif opcion == "2":
            filtro.filtrar_por_producto()
        elif opcion == "3":
            filtro.filtrar_combinado()
        elif opcion == "4":
            filtro.mostrar_detalle_pedido()
        elif opcion == "5":
            filtro.exportar_resultados()
        elif opcion == "6":
            filtro.reiniciar_filtros()
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

# ------------------ Submenú: Consulta de inventario ------------------ #
def menu_inventario():
    while True:
        print("\n== CONSULTAR INVENTARIO ==")
        print("1. Mostrar lista completa de insumos")
        print("2. Ver detalles de insumo")
        print("3. Buscar insumo por nombre")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
    
        if opcion == "1":
            mostrar_lista_insumos()
        elif opcion == "2":
            ver_detalle_insumo()
        elif opcion == "3":
            nombre = input("Ingrese el nombre del insumo: ")
            buscar_insumo(nombre)
        elif opcion == "4":
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

# ------------------ Submenú: Verificacion de insumos ------------------ #
def menu_envio():
    while True:
        print("\n== VERIFICAR DISPONIBILIDAD DE INSUMOS ==")
        print("1. Generar lista de insumos listos para envío")
        print("2. Enviar lista de insumos listos al lider de produccion")
        print("3. Actualizar inventario")
        print("4. Generar solicitud de compra de insumos")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            generar_lista_envio()
        elif opcion == "2":
            enviar_lista_insumos()
        elif opcion == "3":
            actualizar_inventario()
        elif opcion == "4":
            menu_generar_solicitud()
        elif opcion == "5":
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
        print("5. Reportar insumos defectuosos")
        print("6. Volver al menú principal")
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
            menu_reportar_defectuosos()
        elif opcion == "6":
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

# ------------------ Submenú: Reportes de solicitud de compra ------------------ #
def menu_reportes_solicitudes():
    while True:
        print("\n=== REPORTES DE SOLICITUDES DE COMPRA ===")
        print("1. Filtrar por fechas")
        print("2. Seleccionar reporte específico")
        print("3. Descargar reporte")
        print("4. Volver al menú principal")
        op = input("Seleccione una opción: ")
        if op == "1":
            filtrar_solicitudes_fecha()
        elif op == "2":
            seleccionar_reporte_solicitud()
        elif op == "3":
            descargar_reporte_solicitud()
        elif op == "4":
            break
        else:
            print("❌ Opción inválida")

# ------------------ Submenú: Reportes de insumos listos para envio ------------------ #
def menu_reportes_insumos_listos():
    while True:
        print("\n=== REPORTES DE INSUMOS LISTOS PARA ENVÍO ===")
        print("1. Filtrar por fechas")
        print("2. Seleccionar reporte específico")
        print("3. Descargar reporte")
        print("4. Volver al menú principal")
        op = input("Seleccione una opción: ")
        if op == "1":
            filtrar_listos_fecha()
        elif op == "2":
            seleccionar_reporte_listos()
        elif op == "3":
            descargar_reporte_listos()
        elif op == "4":
            break
        else:
            print("❌ Opción inválida")

# ------------------ Punto de entrada ------------------ #
if __name__ == "__main__":
    if iniciar_sesion():
        mostrar_menu_opciones()