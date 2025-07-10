import tkinter as tk
from tkinter import messagebox, simpledialog
from main import (
    FiltroPedidos, pedidos, menu_consulta, menu_inventario, menu_envio,
    menu_recepcion, menu_reportes, iniciar_sesion
)

class FincaDirectaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Finca Directa")
        self.root.geometry("400x400")
        self.filtro = None
        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="INICIO DE SESIÓN", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.root, text="Usuario:").pack()
        usuario_entry = tk.Entry(self.root)
        usuario_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        contraseña_entry = tk.Entry(self.root, show="*")
        contraseña_entry.pack()
        def intentar_login():
            usuario = usuario_entry.get()
            contraseña = contraseña_entry.get()
            if usuario == "j" and contraseña == "j":
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        tk.Button(self.root, text="Ingresar", command=intentar_login).pack(pady=10)

    def mostrar_menu_principal(self):
        self.limpiar_ventana()
        self.filtro = FiltroPedidos(pedidos)
        tk.Label(self.root, text="MENÚ DE OPCIONES", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Consultar demanda de pedidos", width=40, command=self.abrir_menu_consulta).pack(pady=5)
        tk.Button(self.root, text="Consultar inventario", width=40, command=menu_inventario).pack(pady=5)
        tk.Button(self.root, text="Verificar disponibilidad de insumos", width=40, command=menu_envio).pack(pady=5)
        tk.Button(self.root, text="Recepción de insumos", width=40, command=menu_recepcion).pack(pady=5)
        tk.Button(self.root, text="Reportes de recepción de insumos", width=40, command=menu_reportes).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", width=40, command=self.mostrar_login).pack(pady=20)

    def abrir_menu_consulta(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="CONSULTA DE PEDIDOS", font=("Arial", 14, "bold")).pack(pady=15)
        tk.Button(self.root, text="1. Filtrar pedidos por fecha", width=40,
                  command=self.filtrar_por_fecha_gui).pack(pady=3)
        tk.Button(self.root, text="2. Filtrar pedidos por producto", width=40,
                  command=self.filtrar_por_producto_gui).pack(pady=3)
        tk.Button(self.root, text="3. Filtrar pedidos producto y fecha", width=40,
                  command=self.filtrar_combinado_gui).pack(pady=3)
        tk.Button(self.root, text="4. Ver detalle de un pedido específico", width=40,
                  command=self.ver_detalle_pedido_gui).pack(pady=3)
        tk.Button(self.root, text="5. Exportar resultados", width=40,
                  command=self.exportar_resultados_gui).pack(pady=3)
        tk.Button(self.root, text="6. Reiniciar filtros", width=40,
                  command=self.reiniciar_filtros_gui).pack(pady=3)
        tk.Button(self.root, text="7. Volver al menú principal", width=40,
                  command=self.mostrar_menu_principal).pack(pady=15)

    def filtrar_por_fecha_gui(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Filtrar pedidos por fecha", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.root, text="Fecha desde (YYYY-MM-DD):").pack()
        desde_entry = tk.Entry(self.root)
        desde_entry.pack(pady=2)

        tk.Label(self.root, text="Fecha hasta (YYYY-MM-DD):").pack()
        hasta_entry = tk.Entry(self.root)
        hasta_entry.pack(pady=2)

        resultado_label = tk.Label(self.root, text="", fg="green")
        resultado_label.pack(pady=10)

        ids_label = tk.Label(self.root, text="", fg="blue")
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

        tk.Button(self.root, text="Filtrar", command=aplicar_filtro).pack(pady=10)
        tk.Button(self.root, text="Volver al menú anterior", command=self.abrir_menu_consulta).pack(pady=10)

    def filtrar_por_producto_gui(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Filtrar pedidos por producto", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.root, text="Nombre de producto:").pack()
        nombre_entry = tk.Entry(self.root)
        nombre_entry.pack(pady=2)

        resultado_label = tk.Label(self.root, text="", fg="green")
        resultado_label.pack(pady=10)

        ids_label = tk.Label(self.root, text="", fg="blue")
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

        tk.Button(self.root, text="Filtrar", command=aplicar_filtro).pack(pady=10)
        tk.Button(self.root, text="Volver al menú anterior", command=self.abrir_menu_consulta).pack(pady=10)

    def filtrar_combinado_gui(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Filtrar pedidos por producto y fecha", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.root, text="Nombre de producto:").pack()
        nombre_entry = tk.Entry(self.root)
        nombre_entry.pack(pady=2)

        tk.Label(self.root, text="Fecha desde (YYYY-MM-DD):").pack()
        desde_entry = tk.Entry(self.root)
        desde_entry.pack(pady=2)

        tk.Label(self.root, text="Fecha hasta (YYYY-MM-DD):").pack()
        hasta_entry = tk.Entry(self.root)
        hasta_entry.pack(pady=2)

        resultado_label = tk.Label(self.root, text="", fg="green")
        resultado_label.pack(pady=10)

        ids_label = tk.Label(self.root, text="", fg="blue")
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

        tk.Button(self.root, text="Filtrar", command=aplicar_filtro).pack(pady=10)
        tk.Button(self.root, text="Volver al menú anterior", command=self.abrir_menu_consulta).pack(pady=10)

    def ver_detalle_pedido_gui(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Ver detalle de un pedido específico", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.root, text="Ingrese el ID del pedido a consultar:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack(pady=2)

        detalle_label = tk.Label(self.root, text="", justify="left", font=("Arial", 11))
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

        tk.Button(self.root, text="Consultar", command=mostrar_detalle).pack(pady=10)
        tk.Button(self.root, text="Volver al menú anterior", command=self.abrir_menu_consulta).pack(pady=10)

    def exportar_resultados_gui(self):
        import os
        import pandas as pd
        self.limpiar_ventana()
        resultado_label = tk.Label(self.root, text="", font=("Arial", 12))
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

        tk.Button(self.root, text="Volver al menú anterior", command=self.abrir_menu_consulta).pack(pady=10)

    def reiniciar_filtros_gui(self):
        self.filtro.reiniciar_filtros()
        messagebox.showinfo("Filtros", "Filtros reiniciados correctamente. Se muestra la tabla original.")
        self.abrir_menu_consulta()

if __name__ == "__main__":
    root = tk.Tk()
    app = FincaDirectaGUI(root)
    root.mainloop()