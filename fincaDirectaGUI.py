import tkinter as tk
from tkinter import messagebox
from main import (
    FiltroPedidos, pedidos, menu_consulta, menu_inventario, menu_envio,
    menu_recepcion, menu_reportes, iniciar_sesion
)

COLOR_BG = "#f4f6fb"
COLOR_FRAME = "#e3eafc"
COLOR_BTN = "#4f8cff" 
COLOR_BTN_TEXT = "#fff"
COLOR_TITLE = "#2a3b8f"
COLOR_LABEL = "#222"
FONT_TITLE = ("Arial", 18, "bold")
FONT_SUBTITLE = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 11)
FONT_BTN = ("Arial", 11, "bold")

class FincaDirectaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Finca Directa")
        self.root.geometry("500x500")
        self.root.configure(bg=COLOR_BG)
        self.filtro = None
        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_frame(self):
        frame = tk.Frame(self.root, bg=COLOR_FRAME, bd=2, relief="groove")
        frame.pack(pady=30, padx=30, fill="both", expand=True)
        return frame

    def mostrar_login(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="INICIO DE SESIÓN", font=FONT_TITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=20)
        tk.Label(frame, text="Usuario:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        usuario_entry = tk.Entry(frame, font=FONT_LABEL)
        usuario_entry.pack(pady=5)
        tk.Label(frame, text="Contraseña:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        contraseña_entry = tk.Entry(frame, show="*", font=FONT_LABEL)
        contraseña_entry.pack(pady=5)
        def intentar_login():
            usuario = usuario_entry.get()
            contraseña = contraseña_entry.get()
            if usuario == "j" and contraseña == "j":
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        tk.Button(frame, text="Ingresar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=intentar_login).pack(pady=20)

    def mostrar_menu_principal(self):
        self.limpiar_ventana()
        self.filtro = FiltroPedidos(pedidos)
        frame = self.crear_frame()
        tk.Label(frame, text="MENÚ DE OPCIONES", font=FONT_TITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=20)
        opciones = [
            ("Consultar demanda de pedidos", self.abrir_menu_consulta),
            ("Consultar inventario", self.abrir_menu_inventario),
            ("Verificar disponibilidad de insumos", self.abrir_menu_envio),
            ("Recepción de insumos", menu_recepcion),
            ("Reportes de recepción de insumos", menu_reportes),
            ("Cerrar sesión", self.mostrar_login)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=6)

    def abrir_menu_consulta(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="CONSULTA DE PEDIDOS", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=15)
        opciones = [
            ("1. Filtrar pedidos por fecha", self.filtrar_por_fecha_gui),
            ("2. Filtrar pedidos por producto", self.filtrar_por_producto_gui),
            ("3. Filtrar pedidos producto y fecha", self.filtrar_combinado_gui),
            ("4. Ver detalle de un pedido específico", self.ver_detalle_pedido_gui),
            ("5. Exportar resultados", self.exportar_resultados_gui),
            ("6. Reiniciar filtros", self.reiniciar_filtros_gui),
            ("7. Volver al menú principal", self.mostrar_menu_principal)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def filtrar_por_fecha_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Filtrar pedidos por fecha", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        tk.Label(frame, text="Fecha desde (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        desde_entry = tk.Entry(frame, font=FONT_LABEL)
        desde_entry.pack(pady=2)
        tk.Label(frame, text="Fecha hasta (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        hasta_entry = tk.Entry(frame, font=FONT_LABEL)
        hasta_entry.pack(pady=2)
        resultado_label = tk.Label(frame, text="", fg="green", bg=COLOR_FRAME, font=FONT_LABEL)
        resultado_label.pack(pady=10)
        ids_label = tk.Label(frame, text="", fg="blue", bg=COLOR_FRAME, font=FONT_LABEL)
        ids_label.pack(pady=5)
        def aplicar_filtro():
            inicio = desde_entry.get()
            fin = hasta_entry.get()
            try:
                import pandas as pd
                if inicio:
                    inicio_dt = pd.to_datetime(inicio)
                else:
                    inicio_dt = self.filtro.df['fecha'].min()
                if fin:
                    fin_dt = pd.to_datetime(fin)
                else:
                    fin_dt = self.filtro.df['fecha'].max()
                self.filtro.df_filtrado = self.filtro.df[
                    self.filtro.df['fecha'].between(inicio_dt, fin_dt)
                ]
                if self.filtro.df_filtrado.empty:
                    resultado_label.config(text="⚠ No se encontraron pedidos en el rango.", fg="red")
                    ids_label.config(text="")
                else:
                    resultado_label.config(
                        text=f"✅ Pedidos filtrados desde {inicio_dt.date()} hasta {fin_dt.date()}.",
                        fg="green"
                    )
                    ids = self.filtro.df_filtrado['id'].to_list()
                    ids_str = ", ".join(str(i) for i in ids)
                    ids_label.config(text=f"ID de pedido: {ids_str}", fg="blue")
            except Exception:
                resultado_label.config(text="⚠ Formato de fecha inválido.", fg="red")
                ids_label.config(text="")
        tk.Button(frame, text="Filtrar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=aplicar_filtro).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_consulta).pack(pady=10)

    def filtrar_por_producto_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Filtrar pedidos por producto", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        tk.Label(frame, text="Nombre de producto:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        nombre_entry = tk.Entry(frame, font=FONT_LABEL)
        nombre_entry.pack(pady=2)
        resultado_label = tk.Label(frame, text="", fg="green", bg=COLOR_FRAME, font=FONT_LABEL)
        resultado_label.pack(pady=10)
        ids_label = tk.Label(frame, text="", fg="blue", bg=COLOR_FRAME, font=FONT_LABEL)
        ids_label.pack(pady=5)
        def aplicar_filtro():
            nombre = nombre_entry.get().strip()
            if not nombre:
                resultado_label.config(text="⚠ Debe ingresar un nombre de producto.", fg="red")
                ids_label.config(text="")
                return
            df_filtrado = self.filtro.df[
                self.filtro.df['producto'].str.lower().str.contains(nombre.lower(), na=False)
            ]
            self.filtro.df_filtrado = df_filtrado
            if df_filtrado.empty:
                resultado_label.config(text=f"⚠ No se encontraron pedidos del producto '{nombre}'.", fg="red")
                ids_label.config(text="")
            else:
                resultado_label.config(
                    text=f"🔍 Pedidos con producto '{nombre}':", fg="green"
                )
                ids = df_filtrado['id'].to_list()
                ids_str = ", ".join(str(i) for i in ids)
                ids_label.config(text=f"ID de pedido: {ids_str}", fg="blue")
        tk.Button(frame, text="Filtrar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=aplicar_filtro).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_consulta).pack(pady=10)

    def filtrar_combinado_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Filtrar pedidos por producto y fecha", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        tk.Label(frame, text="Nombre de producto:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        nombre_entry = tk.Entry(frame, font=FONT_LABEL)
        nombre_entry.pack(pady=2)
        tk.Label(frame, text="Fecha desde (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        desde_entry = tk.Entry(frame, font=FONT_LABEL)
        desde_entry.pack(pady=2)
        tk.Label(frame, text="Fecha hasta (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        hasta_entry = tk.Entry(frame, font=FONT_LABEL)
        hasta_entry.pack(pady=2)
        resultado_label = tk.Label(frame, text="", fg="green", bg=COLOR_FRAME, font=FONT_LABEL)
        resultado_label.pack(pady=10)
        ids_label = tk.Label(frame, text="", fg="blue", bg=COLOR_FRAME, font=FONT_LABEL)
        ids_label.pack(pady=5)
        def aplicar_filtro():
            nombre = nombre_entry.get().strip()
            inicio = desde_entry.get()
            fin = hasta_entry.get()
            import pandas as pd
            df_temp = self.filtro.df.copy()
            if nombre:
                df_temp = df_temp[df_temp['producto'].str.lower().str.contains(nombre.lower(), na=False)]
            try:
                if inicio:
                    inicio_dt = pd.to_datetime(inicio)
                else:
                    inicio_dt = df_temp['fecha'].min()
                if fin:
                    fin_dt = pd.to_datetime(fin)
                else:
                    fin_dt = df_temp['fecha'].max()
                df_temp = df_temp[df_temp['fecha'].between(inicio_dt, fin_dt)]
                self.filtro.df_filtrado = df_temp
                if df_temp.empty:
                    resultado_label.config(text="⚠ No se encontraron pedidos con esos filtros.", fg="red")
                    ids_label.config(text="")
                else:
                    resultado_label.config(
                        text=f"🔍 Pedidos con '{nombre}' entre {inicio_dt.date()} y {fin_dt.date()}:",
                        fg="green"
                    )
                    ids = df_temp['id'].to_list()
                    ids_str = ", ".join(str(i) for i in ids)
                    ids_label.config(text=f"ID de pedido: {ids_str}", fg="blue")
            except Exception:
                resultado_label.config(text="⚠ Formato de fecha inválido.", fg="red")
                ids_label.config(text="")
        tk.Button(frame, text="Filtrar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=aplicar_filtro).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_consulta).pack(pady=10)

    def ver_detalle_pedido_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Ver detalle de un pedido específico", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        tk.Label(frame, text="Ingrese el ID del pedido a consultar:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        id_entry = tk.Entry(frame, font=FONT_LABEL)
        id_entry.pack(pady=2)
        detalle_label = tk.Label(frame, text="", justify="left", font=FONT_LABEL, bg=COLOR_FRAME)
        detalle_label.pack(pady=10)
        def mostrar_detalle():
            pedido_id = id_entry.get().strip()
            df = self.filtro.df_filtrado if not self.filtro.df_filtrado.empty else self.filtro.df
            detalle = df[df['id'].astype(str) == pedido_id]
            if not detalle.empty:
                fila = detalle.iloc[0]
                texto = (
                    "📌 Detalle del pedido:\n"
                    f"- ID: {fila.get('id','')}\n"
                    f"- Fecha: {fila.get('fecha','')}\n"
                    f"- Cliente: {fila.get('cliente','')}\n"
                    f"- Cedula: {fila.get('cedula','')}\n"
                    f"- Direccion: {fila.get('direccion','')}\n"
                    f"- Producto: {fila.get('producto','')}\n"
                    f"- Cantidad: {fila.get('cantidad','')}\n"
                    f"- Fecha_entrega: {fila.get('fecha_entrega','')}\n"
                )
                detalle_label.config(text=texto, fg="black")
            else:
                detalle_label.config(text="❌ ID de pedido no encontrado en los filtrados", fg="red")
        tk.Button(frame, text="Consultar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=mostrar_detalle).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_consulta).pack(pady=10)
    
    def abrir_menu_inventario(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="INVENTARIO DE INSUMOS", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=15)
        opciones = [
            ("1. Mostrar lista completa de insumos", self.mostrar_lista_insumos_gui),
            ("2. Ver detalles de insumo", self.ver_detalle_insumo_gui),
            ("3. Buscar insumo por nombre", self.buscar_insumo_nombre_gui),
            ("4. Volver al menú principal", self.mostrar_menu_principal)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def exportar_resultados_gui(self):
        import os
        import pandas as pd
        self.limpiar_ventana()
        frame = self.crear_frame()
        resultado_label = tk.Label(frame, text="", font=FONT_LABEL, bg=COLOR_FRAME)
        resultado_label.pack(pady=20)
        demanda_path = os.path.join(os.path.dirname(__file__), "data", "demanda.xlsx")
        try:
            if self.filtro.df_filtrado.empty:
                resultado_label.config(text="⚠ No hay datos para exportar.", fg="red")
            else:
                resumen = self.filtro.df_filtrado.groupby('producto', as_index=False)['cantidad'].sum()
                resumen.columns = ['producto', 'total_cantidad']
                resumen.to_excel(demanda_path, index=False)
                resultado_label.config(
                    text=f"✅ Resultados exportados a '{demanda_path}'", fg="green"
                )
                self.filtro.reiniciar_filtros()
        except PermissionError:
            resultado_label.config(
                text=f"❌ No se pudo exportar '{demanda_path}' porque está abierto en otro programa (como Excel).\n🔁 Por favor, ciérralo y vuelve a intentarlo.",
                fg="red"
            )
        except Exception as e:
            resultado_label.config(text=f"❌ Error al exportar: {e}", fg="red")
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_consulta).pack(pady=10)

        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def reiniciar_filtros_gui(self):
        self.filtro.reiniciar_filtros()
        messagebox.showinfo("Filtros", "Filtros reiniciados correctamente. Se muestra la tabla original.")
        self.abrir_menu_consulta()
        
    def mostrar_lista_insumos_gui(self):
        from main import df_inventario
        import tkinter.ttk as ttk
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Inventario Completo:", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)

        columnas = [col for col in ['id', 'producto', 'cantidad'] if col in df_inventario.columns]
        df_mostrar = df_inventario[columnas]

        tree = ttk.Treeview(frame, columns=columnas, show='headings', height=12)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=FONT_LABEL, background=COLOR_FRAME, foreground=COLOR_TITLE)
        style.configure("Treeview", font=FONT_LABEL, rowheight=24, background="#f9fafc", fieldbackground="#f9fafc")

        for col in columnas:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=120)

        for _, row in df_mostrar.iterrows():
            tree.insert("", tk.END, values=list(row))
            tree.pack(pady=10, fill="x", expand=True)

        tk.Button(
        frame, text="Volver al menú anterior",
        font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT,
        command=self.abrir_menu_inventario
        ).pack(pady=10)

    def ver_detalle_insumo_gui(self):
        from main import df_inventario
        import tkinter.ttk as ttk

        self.limpiar_ventana()
        frame = self.crear_frame()

        # Detectar el ID máximo
        max_id = len(df_inventario) - 1
        tk.Label(
            frame,
            text=f"🔍 Ingrese el ID del insumo (0-{max_id}):",
            font=FONT_LABEL,
            bg=COLOR_FRAME
        ).pack(pady=10)
        id_entry = tk.Entry(frame, font=FONT_LABEL)
        id_entry.pack(pady=2)

        detalle_frame = tk.Frame(frame, bg=COLOR_FRAME)
        detalle_frame.pack(pady=15)

        # Título SIEMPRE arriba de la tabla
        titulo_label = tk.Label(
            detalle_frame,
            text="📦 Detalle del insumo:",
            font=FONT_SUBTITLE,
            fg=COLOR_TITLE,
            bg=COLOR_FRAME
        )
        titulo_label.pack(side="top", pady=5)

        def mostrar_detalle():
            # Elimina widgets previos excepto el título
            for widget in detalle_frame.winfo_children():
                if widget != titulo_label:
                    widget.destroy()
            try:
                idx = int(id_entry.get())
                if 0 <= idx <= max_id:
                    fila = df_inventario.loc[idx]
                    # Mostrar como tabla estilizada
                    tree = ttk.Treeview(detalle_frame, columns=("Campo", "Valor"), show="headings", height=3)
                    tree.heading("Campo", text="Campo")
                    tree.heading("Valor", text="Valor")
                    tree.column("Campo", anchor="center", width=150)
                    tree.column("Valor", anchor="center", width=200)
                    tree.insert("", "end", values=("Producto", fila["producto"]))
                    tree.insert("", "end", values=("Cantidad", fila["cantidad"]))
                    tree.insert("", "end", values=("Última actualización", fila["ultima_actualizacion"]))
                    tree.pack()
                else:
                    tk.Label(detalle_frame, text="❌ ID fuera de rango.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
            except Exception:
                tk.Label(detalle_frame, text="❌ Entrada inválida. Ingrese un número entero.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()

        tk.Button(
            frame, text="Consultar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=mostrar_detalle
        ).pack(pady=10)
        tk.Button(
            frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_inventario
        ).pack(pady=10)

    def buscar_insumo_nombre_gui(self):
        from main import df_inventario
        import tkinter.ttk as ttk

        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Ingrese el nombre del insumo:", font=FONT_LABEL, bg=COLOR_FRAME).pack(pady=10)
        nombre_entry = tk.Entry(frame, font=FONT_LABEL)
        nombre_entry.pack(pady=2)

        resultado_frame = tk.Frame(frame, bg=COLOR_FRAME)
        resultado_frame.pack(pady=15)

        def buscar():
            for widget in resultado_frame.winfo_children():
                widget.destroy()
            nombre = nombre_entry.get().strip().lower()
            if not nombre:
                tk.Label(resultado_frame, text="⚠ Debe ingresar un nombre.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                return
            # Normaliza y busca
            df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
            resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre)]
            if resultado.empty:
                tk.Label(resultado_frame, text="❌ No se encontraron insumos con ese nombre.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
            else:
                tk.Label(resultado_frame, text="Resultado de la búsqueda:", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=5)
                columnas = ["producto", "cantidad", "ultima_actualizacion"]
                tree = ttk.Treeview(resultado_frame, columns=columnas, show='headings', height=len(resultado))
                for col in columnas:
                    tree.heading(col, text=col.capitalize())
                    tree.column(col, anchor="center", width=140)
                for _, row in resultado.iterrows():
                    tree.insert("", tk.END, values=[row["producto"], row["cantidad"], row["ultima_actualizacion"]])
                tree.pack(pady=5, fill="x", expand=True)

        tk.Button(frame, text="Buscar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=buscar).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_inventario).pack(pady=10)

    def generar_lista_envio_gui(self):
        import tkinter.ttk as ttk
        from main import generar_lista_envio

        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="📦 Insumos listos para envío:", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)

        # Obtener el DataFrame usando la función del main
        lista = generar_lista_envio()
        if lista is None or lista.empty:
            tk.Label(frame, text="❌ No hay insumos que cumplan con la demanda.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
        else:
            columnas = ["producto", "cantidad_a_enviar"]
            tree = ttk.Treeview(frame, columns=columnas, show='headings', height=len(lista))
            for col in columnas:
                tree.heading(col, text=col.replace("_", " ").capitalize())
                tree.column(col, anchor="center", width=180 if col == "producto" else 120)
            for _, row in lista.iterrows():
                tree.insert("", tk.END, values=[row["producto"], row["cantidad_a_enviar"]])
            tree.pack(pady=10, fill="x", expand=True)

        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_envio).pack(pady=10)

    def abrir_menu_envio(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="VERIFICAR DISPONIBILIDAD DE INSUMOS", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=15)
        opciones = [
            ("1. Generar lista de insumos listos para envío", self.generar_lista_envio_gui),
            ("2. Enviar lista de insumos listos al lider de produccion", self.enviar_lista_lider_gui),
            ("3. Actualizar inventario", self.actualizar_inventario_gui),
            ("4. Volver al menú principal", self.mostrar_menu_principal)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def enviar_lista_lider_gui(self):
        from main import enviar_lista_insumos
        import os

        self.limpiar_ventana()
        frame = self.crear_frame()
        resultado_label = tk.Label(frame, text="", font=FONT_LABEL, bg=COLOR_FRAME)
        resultado_label.pack(pady=30)

        try:
            # Llama a la función que exporta y envía el correo
            enviar_lista_insumos()
            ruta = os.path.join(os.path.dirname(__file__), "data", "insumos_listos.xlsx")
            resultado_label.config(
                text=f"✅ Archivo generado: {ruta}\n📧 Correo enviado exitosamente.",
                fg="green"
            )
        except Exception as e:
            resultado_label.config(
                text=f"❌ Error al enviar el correo o generar el archivo:\n{e}",
                fg="red"
            )

        tk.Button(
            frame, text="Volver al menú anterior",
            font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT,
            command=self.abrir_menu_envio
        ).pack(pady=10)

    def actualizar_inventario_gui(self):
        from main import actualizar_inventario  # Importa la función directamente
        self.limpiar_ventana()
        frame = self.crear_frame()
        resultado_label = tk.Label(frame, text="", font=FONT_LABEL, bg=COLOR_FRAME)
        resultado_label.pack(pady=30)

        try:
            actualizar_inventario()  # Llama la función que actualiza el inventario y guarda el archivo
            resultado_label.config(
                text="✅ Inventario actualizado correctamente.",
                fg="green"
            )
        except Exception as e:
            resultado_label.config(
                text=f"❌ Error al actualizar el inventario:\n{e}",
                fg="red"
            )

        tk.Button(
            frame, text="Volver al menú anterior",
            font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT,
            command=self.abrir_menu_envio
        ).pack(pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = FincaDirectaGUI(root)
    root.mainloop()