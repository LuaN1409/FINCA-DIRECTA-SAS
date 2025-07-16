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
        self.root.geometry("900x600")
        self.root.configure(bg=COLOR_BG)
        self.filtro = None
        self.reportes_filtrados = None
        self.fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.mostrar_login()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        # For Windows, maximize if not fullscreen
        if not self.fullscreen:
            self.root.state('zoomed')

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.root.state('zoomed')

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_frame(self):
        frame = tk.Frame(self.root, bg=COLOR_FRAME, bd=2, relief="groove")
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
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
            ("Recepción de insumos", self.abrir_menu_recepcion),
            ("Reportes de recepción de insumos", self.abrir_menu_reportes),
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

    def abrir_menu_recepcion(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="RECEPCIÓN DE INSUMOS", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=15)
        opciones = [
            ("1. Registrar información del pedido", self.registrar_info_pedido_gui),
            ("2. Validar campos de ingreso de datos", self.validar_campos_gui),
            ("3. Verificar cantidad y calidad del insumo", self.verificar_cantidad_calidad_gui),
            ("4. Ingresar insumos conformes al inventario", self.ingresar_insumos_inventario_gui),
            ("5. Volver al menú principal", self.mostrar_menu_principal)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def registrar_info_pedido_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Registrar información del pedido", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        labels = [
            ("Nombre del proveedor:", "proveedor"),
            ("Fecha de recepción (YYYY-MM-DD):", "fecha"),
            ("Número de pedido:", "numero"),
            ("Cantidad de productos diferentes entregados:", "cantidad_productos")
        ]
        entries = {}
        for texto, key in labels:
            tk.Label(frame, text=texto, font=FONT_LABEL, bg=COLOR_FRAME).pack()
            entry = tk.Entry(frame, font=FONT_LABEL)
            entry.pack(pady=2)
            entries[key] = entry
        productos_frame = tk.Frame(frame, bg=COLOR_FRAME)
        productos_frame.pack(pady=10)
        productos = []
        registrar_btn = tk.Button(frame, text="Registrar productos entregados", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT)
        registrar_btn.pack(pady=10)
        reintentar_btn = tk.Button(frame, text="Reintentar", font=FONT_BTN, bg="#e74c3c", fg=COLOR_BTN_TEXT)
        reintentar_btn.pack_forget()
        def reintentar():
            self.registrar_info_pedido_gui()
        reintentar_btn.config(command=reintentar)
        def pedir_productos():
            # Deshabilita los campos generales
            for entry in entries.values():
                entry.config(state="disabled")
            registrar_btn.pack_forget()
            reintentar_btn.pack(pady=5)
            for widget in productos_frame.winfo_children():
                widget.destroy()
            try:
                n = int(entries["cantidad_productos"].get())
            except Exception:
                tk.Label(productos_frame, text="❌ Ingrese un número válido de productos.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                return
            productos.clear()
            def pedir_producto(i):
                for widget in productos_frame.winfo_children():
                    widget.destroy()
                tk.Label(productos_frame, text=f"Nombre del producto {i+1}:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
                nombre_entry = tk.Entry(productos_frame, font=FONT_LABEL)
                nombre_entry.pack(pady=2)
                tk.Label(productos_frame, text=f"Cantidad de '{i+1}':", font=FONT_LABEL, bg=COLOR_FRAME).pack()
                cantidad_entry = tk.Entry(productos_frame, font=FONT_LABEL)
                cantidad_entry.pack(pady=2)
                def siguiente():
                    nombre = nombre_entry.get().strip()
                    cantidad = cantidad_entry.get().strip()
                    if not nombre or not cantidad.isdigit():
                        tk.Label(productos_frame, text="❌ Complete ambos campos correctamente.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                        return
                    productos.append({"nombre": nombre, "cantidad": int(cantidad)})
                    if i + 1 < n:
                        pedir_producto(i + 1)
                    else:
                        self.datos_pedido = {
                            "proveedor": entries["proveedor"].get().strip(),
                            "fecha": entries["fecha"].get().strip(),
                            "numero": entries["numero"].get().strip(),
                            "cantidad_productos": n,
                            "productos": productos.copy()
                        }
                        self.mostrar_registro_exitoso()
                tk.Button(productos_frame, text="Siguiente", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=siguiente).pack(pady=5)
            pedir_producto(0)
        registrar_btn.config(command=pedir_productos)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=10)

    def mostrar_registro_exitoso(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="✅ Registro realizado con éxito", font=FONT_SUBTITLE, fg="green", bg=COLOR_FRAME).pack(pady=30)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=20)

    def validar_campos_gui(self):
        from datetime import datetime
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Validar datos del pedido", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        errores = []
        datos = getattr(self, "datos_pedido", None)
        if not datos:
            tk.Label(frame, text="❌ No hay datos registrados para validar.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
        else:
            if not datos["proveedor"]:
                errores.append("- El nombre del proveedor no puede estar vacío.")
            try:
                datetime.strptime(datos["fecha"], "%Y-%m-%d")
            except Exception:
                errores.append("- La fecha debe tener formato YYYY-MM-DD y ser válida.")
            if not datos["numero"]:
                errores.append("- El número de pedido no puede estar vacío.")
            if not isinstance(datos["cantidad_productos"], int) or datos["cantidad_productos"] <= 0:
                errores.append("- La cantidad de productos debe ser un número entero positivo.")
            for idx, prod in enumerate(datos["productos"]):
                if not prod["nombre"]:
                    errores.append(f"- El nombre del producto {idx+1} no puede estar vacío.")
                if not isinstance(prod["cantidad"], int) or prod["cantidad"] <= 0:
                    errores.append(f"- La cantidad de '{prod['nombre']}' debe ser un número entero positivo.")
            if errores:
                tk.Label(frame, text="❌ Errores encontrados:", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=5)
                for err in errores:
                    tk.Label(frame, text=err, fg="red", bg=COLOR_FRAME, font=FONT_LABEL, anchor="w", justify="left").pack(anchor="w")
            else:
                resumen = (
                    f"Proveedor: {datos['proveedor']}\n"
                    f"Fecha: {datos['fecha']}\n"
                    f"Número de pedido: {datos['numero']}\n"
                    f"Cantidad de productos: {datos['cantidad_productos']}\n"
                    "Productos:\n" +
                    "\n".join([f"  - {p['nombre']}: {p['cantidad']}" for p in datos['productos']])
                )
                tk.Label(frame, text="✅ Todos los datos son válidos.", fg="green", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=5)
                tk.Label(frame, text=resumen, fg="black", bg=COLOR_FRAME, font=FONT_LABEL, justify="left").pack(pady=5)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=10)

    def verificar_cantidad_calidad_gui(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Verificar cantidad y calidad del insumo", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        datos = getattr(self, "datos_pedido", None)
        if not datos or not datos.get("productos"):
            tk.Label(frame, text="❌ No hay productos registrados para verificar.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
            tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=10)
            return
        productos = datos["productos"]
        conformes = []
        def verificar_producto(i):
            for widget in frame.winfo_children()[1:]:
                widget.destroy()
            prod = productos[i]
            texto = f"Producto '{prod['nombre']}' ({prod['cantidad']} unidades). ¿Está Conforme?"
            tk.Label(frame, text=texto, font=FONT_LABEL, bg=COLOR_FRAME).pack(pady=10)
            var = tk.StringVar(value="Conforme")
            opciones = ["Conforme", "No conforme"]
            menu = tk.OptionMenu(frame, var, *opciones)
            menu.config(font=FONT_LABEL)
            menu.pack(pady=5)
            def siguiente():
                if var.get() == "Conforme":
                    conformes.append(prod)
                if i + 1 < len(productos):
                    verificar_producto(i + 1)
                else:
                    self.datos_pedido["productos"] = conformes
                    self.mostrar_verificacion_exitosa()
            tk.Button(frame, text="Siguiente", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=siguiente).pack(pady=10)
        verificar_producto(0)

    def mostrar_verificacion_exitosa(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="✅ Verificación completada. Solo se guardarán los productos conformes.", font=FONT_SUBTITLE, fg="green", bg=COLOR_FRAME).pack(pady=30)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=20)

    def ingresar_insumos_inventario_gui(self):
        import pandas as pd
        from main import cargar_excel, guardar_excel, inventario
        from datetime import datetime
        datos = getattr(self, "datos_pedido", None)
        if not datos or not datos.get("productos"):
            messagebox.showerror("Error", "No hay productos conformes para ingresar al inventario.")
            self.abrir_menu_recepcion()
            return
        productos = datos["productos"]
        if not productos:
            messagebox.showerror("Error", "No hay productos conformes para ingresar al inventario.")
            self.abrir_menu_recepcion()
            return
        df_inv = cargar_excel(inventario)
        if df_inv.empty or 'producto' not in df_inv.columns or 'cantidad' not in df_inv.columns:
            df_inv = pd.DataFrame(columns=["producto", "cantidad", "ultima_actualizacion"])
        if 'ultima_actualizacion' not in df_inv.columns:
            df_inv['ultima_actualizacion'] = None
        df_inv['producto_normalizado'] = df_inv['producto'].astype(str).str.strip().str.lower()
        hoy = datetime.today().strftime('%Y-%m-%d')
        for prod in productos:
            nombre_original = prod['nombre'].strip()
            nombre_normalizado = nombre_original.lower()
            cantidad = prod['cantidad']
            if nombre_normalizado in df_inv['producto_normalizado'].values:
                index = df_inv[df_inv['producto_normalizado'] == nombre_normalizado].index[0]
                df_inv.at[index, 'cantidad'] += cantidad
                df_inv.at[index, 'ultima_actualizacion'] = hoy
            else:
                nueva_fila = pd.DataFrame([[nombre_original, cantidad, hoy]], columns=["producto", "cantidad", "ultima_actualizacion"])
                df_inv = pd.concat([df_inv, nueva_fila], ignore_index=True)
        df_inv = df_inv.drop(columns=["producto_normalizado"])
        guardar_excel(df_inv, inventario)
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="✅ Insumos conformes ingresados al inventario correctamente.", font=FONT_SUBTITLE, fg="green", bg=COLOR_FRAME).pack(pady=30)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_recepcion).pack(pady=20)
        # Limpia productos para evitar doble ingreso
        self.datos_pedido["productos"] = []

    def abrir_menu_reportes(self):
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="REPORTES DE RECEPCIÓN DE INSUMOS", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=15)
        opciones = [
            ("1. Filtrar por fechas", self.filtrar_reportes_por_fechas_gui),
            ("2. Seleccionar reporte específico", self.seleccionar_reporte_gui),
            ("3. Descargar reporte", self.descargar_reporte_gui),
            ("4. Volver al menú principal", self.mostrar_menu_principal)
        ]
        for texto, comando in opciones:
            tk.Button(frame, text=texto, width=40, font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=comando).pack(pady=4)

    def filtrar_reportes_por_fechas_gui(self):
        import pandas as pd
        from main import cargar_excel, entregas
        from tkinter import ttk
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Filtrar reportes por fechas", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        tk.Label(frame, text="Ingrese la fecha de inicio (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        fecha_ini_entry = tk.Entry(frame, font=FONT_LABEL)
        fecha_ini_entry.pack(pady=2, fill="x", expand=True)
        tk.Label(frame, text="Ingrese la fecha de fin (YYYY-MM-DD):", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        fecha_fin_entry = tk.Entry(frame, font=FONT_LABEL)
        fecha_fin_entry.pack(pady=2, fill="x", expand=True)
        resultado_frame = tk.Frame(frame, bg=COLOR_FRAME)
        resultado_frame.pack(pady=10, fill="both", expand=True)
        self.reportes_filtrados = None  # Limpiar filtro previo
        def filtrar():
            for widget in resultado_frame.winfo_children():
                widget.destroy()
            fecha_ini = fecha_ini_entry.get().strip()
            fecha_fin = fecha_fin_entry.get().strip()
            try:
                df_entregas = cargar_excel(entregas)
                if df_entregas.empty:
                    tk.Label(resultado_frame, text="No hay entregas registradas.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                    self.reportes_filtrados = None
                    return
                df_entregas['fecha'] = pd.to_datetime(df_entregas['fecha'])
                ini = pd.to_datetime(fecha_ini)
                fin = pd.to_datetime(fecha_fin)
                filtrado = df_entregas[(df_entregas['fecha'] >= ini) & (df_entregas['fecha'] <= fin)]
                self.reportes_filtrados = filtrado.copy()  # Guardar filtro
                if filtrado.empty:
                    tk.Label(resultado_frame, text="🔍 No hay entregas en ese rango de fechas.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                else:
                    tk.Label(resultado_frame, text="📄 Reportes disponibles:", font=FONT_LABEL, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(anchor="w")
                    columnas = ("ID", "Pedido", "Fecha", "Proveedor")
                    tree = ttk.Treeview(resultado_frame, columns=columnas, show='headings')
                    for col in columnas:
                        tree.heading(col, text=col)
                        tree.column(col, anchor="center", width=150, stretch=True)
                    for _, row in filtrado.iterrows():
                        tree.insert("", "end", values=(row['id'], row['numero_pedido'], row['fecha'].strftime('%Y-%m-%d'), row['proveedor']))
                    tree.pack(fill="both", expand=True)
                    # Scrollbar
                    vsb = ttk.Scrollbar(resultado_frame, orient="vertical", command=tree.yview)
                    tree.configure(yscrollcommand=vsb.set)
                    vsb.pack(side='right', fill='y')
            except Exception:
                tk.Label(resultado_frame, text="❌ Formato de fecha inválido.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack()
                self.reportes_filtrados = None
        tk.Button(frame, text="Filtrar", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=filtrar).pack(pady=10)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_reportes).pack(pady=10)

    def seleccionar_reporte_gui(self):
        import pandas as pd
        from main import cargar_excel, entregas, detalle_entregas
        import os
        self.limpiar_ventana()
        frame = self.crear_frame()
        tk.Label(frame, text="Seleccionar reporte específico", font=FONT_SUBTITLE, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10)
        if not hasattr(self, "reportes_filtrados") or self.reportes_filtrados is None or self.reportes_filtrados.empty:
            tk.Label(frame, text="⚠ Primero debe filtrar por fechas para ver los reportes disponibles.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
            tk.Button(frame, text="Ir a filtrar por fechas", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.filtrar_reportes_por_fechas_gui).pack(pady=10)
            tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_reportes).pack(pady=10)
            return
        tk.Label(frame, text="Ingrese el ID del reporte que desea ver:", font=FONT_LABEL, bg=COLOR_FRAME).pack()
        id_entry = tk.Entry(frame, font=FONT_LABEL)
        id_entry.pack(pady=2)
        mensaje_label = tk.Label(frame, text="", font=FONT_LABEL, bg=COLOR_FRAME, fg="green")
        mensaje_label.pack(pady=8)
        def generar_reporte():
            id_sel = id_entry.get().strip()
            if not id_sel.isdigit():
                mensaje_label.config(text="❌ ID inválido.", fg="red")
                return
            id_sel = int(id_sel)
            # Solo IDs del filtro
            if id_sel not in self.reportes_filtrados['id'].values:
                mensaje_label.config(text="❌ El ID seleccionado no pertenece al filtro actual.", fg="red")
                return
            df_entregas = self.reportes_filtrados  # Usar solo el filtro
            df_detalle = cargar_excel(detalle_entregas)
            info = df_entregas[df_entregas['id'] == id_sel].iloc[0]
            detalle = df_detalle[df_detalle['id_entrega'] == id_sel].copy()
            if "conforme" not in detalle.columns:
                detalle["conforme"] = True
            salida = detalle.copy()
            salida.insert(0, "Proveedor", info['proveedor'])
            salida.insert(1, "Fecha", pd.to_datetime(info['fecha']).strftime('%Y-%m-%d'))
            salida.insert(2, "Pedido", info['numero_pedido'])
            salida['conformidad'] = salida['conforme'].apply(lambda x: "Conforme" if x else "No conforme")
            salida = salida[["Proveedor", "Fecha", "Pedido", "producto", "cantidad", "conformidad"]]
            nombre_archivo = os.path.join(os.path.dirname(entregas), f"reporte_pedido_{id_sel}.xlsx")
            salida.to_excel(nombre_archivo, index=False)
            mensaje_label.config(text=f"✅ El reporte ha sido generado como '{nombre_archivo}'.", fg="green")
        tk.Button(frame, text="Siguiente", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=generar_reporte).pack(pady=8)
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_reportes).pack(pady=10)

    def descargar_reporte_gui(self):
        import os
        from main import entregas
        self.limpiar_ventana()
        frame = self.crear_frame()
        carpeta = os.path.dirname(entregas)
        archivos = [f for f in os.listdir(carpeta) if f.startswith("reporte_pedido_") and f.endswith(".xlsx")]
        if not hasattr(self, "reportes_filtrados") or self.reportes_filtrados is None or self.reportes_filtrados.empty:
            tk.Label(frame, text="⚠ Primero debe filtrar por fechas y generar un reporte específico.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
            tk.Button(frame, text="Ir a filtrar por fechas", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.filtrar_reportes_por_fechas_gui).pack(pady=10)
            tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_reportes).pack(pady=10)
            return
        if not archivos:
            tk.Label(frame, text="❌ No hay reporte generado para descargar. Primero selecciona uno.", fg="red", bg=COLOR_FRAME, font=FONT_LABEL).pack(pady=10)
        else:
            tk.Label(frame, text="📥 Reportes disponibles en la carpeta 'data/':", font=FONT_LABEL, fg=COLOR_TITLE, bg=COLOR_FRAME).pack(pady=10, anchor="w")
            lista_frame = tk.Frame(frame, bg=COLOR_FRAME)
            lista_frame.pack(fill="both", expand=True)
            for archivo in archivos:
                tk.Label(lista_frame, text=f" - {archivo}", font=FONT_LABEL, fg="#222", bg=COLOR_FRAME, anchor="w", justify="left").pack(anchor="w")
        tk.Button(frame, text="Volver al menú anterior", font=FONT_BTN, bg=COLOR_BTN, fg=COLOR_BTN_TEXT, command=self.abrir_menu_reportes).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FincaDirectaGUI(root)
    root.mainloop()