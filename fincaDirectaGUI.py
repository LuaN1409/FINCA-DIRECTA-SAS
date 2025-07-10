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
            ("Consultar inventario", menu_inventario),
            ("Verificar disponibilidad de insumos", menu_envio),
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
                        text=f"🔍 Pedidos con '{nombre}' entre {inicio_dt.date()} y {fin_dt.date()}:", fg="green"
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

if __name__ == "__main__":
    root = tk.Tk()
    app = FincaDirectaGUI(root)
    root.mainloop()