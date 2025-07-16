"""
Interfaz Gráfica para el Sistema Finca Directa SAS
Archivo: intento.py
Descripción: Interfaz gráfica usando tkinter para el sistema de gestión de finca
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter import font as tkFont
import pandas as pd
from datetime import datetime
import os
import sys

# Importar la lógica del negocio desde main.py
try:
    from main import *
except ImportError:
    messagebox.showerror("Error", "No se pudo importar main.py. Asegúrate de que esté en el mismo directorio.")
    sys.exit(1)

class SistemaFincaDirectaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Finca Directa SAS")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar fuentes
        self.font_title = tkFont.Font(family="Arial", size=16, weight="bold")
        self.font_subtitle = tkFont.Font(family="Arial", size=12, weight="bold")
        self.font_normal = tkFont.Font(family="Arial", size=10)
        
        # Variables de estado
        self.usuario_actual = None
        self.filtro_pedidos = None
        self.df_reporte_filtrado = pd.DataFrame()
        self.solicitud_actual = pd.DataFrame()
        
        # Configurar estilo
        self.setup_styles()
        
        # Mostrar pantalla de login
        self.mostrar_login()
        
    def setup_styles(self):
        """Configurar estilos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Title.TLabel', font=self.font_title, background="#f0f0f0")
        style.configure('Subtitle.TLabel', font=self.font_subtitle, background="#f0f0f0")
        style.configure('Big.TButton', font=self.font_subtitle, padding=10)
        
    def limpiar_ventana(self):
        """Limpiar todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def mostrar_login(self):
        """Mostrar la pantalla de inicio de sesión"""
        self.limpiar_ventana()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="50")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        ttk.Label(main_frame, text="🌾 Sistema Finca Directa SAS", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=3, pady=30)
        
        # Campos de login
        ttk.Label(main_frame, text="📧 Correo:", font=self.font_normal).grid(
            row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_email = ttk.Entry(main_frame, font=self.font_normal, width=30)
        self.entry_email.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(main_frame, text="🔒 Contraseña:", font=self.font_normal).grid(
            row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_password = ttk.Entry(main_frame, font=self.font_normal, width=30, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=30)
        
        ttk.Button(btn_frame, text="🚀 Iniciar Sesión", 
                  command=self.login, style='Big.TButton').pack(side="left", padx=10)
        ttk.Button(btn_frame, text="➕ Crear Cuenta", 
                  command=self.crear_cuenta, style='Big.TButton').pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Salir", 
                  command=self.root.quit, style='Big.TButton').pack(side="left", padx=10)
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda event: self.login())
        
    def login(self):
        """Procesar el inicio de sesión"""
        correo = self.entry_email.get().strip()
        contraseña = self.entry_password.get().strip()
        
        if not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
            
        # Cargar usuarios y verificar credenciales
        usuarios_df = cargar_usuarios()
        
        encontrado = usuarios_df[
            (usuarios_df["correo"].str.strip().str.lower() == correo.lower()) &
            (usuarios_df["contraseña"] == contraseña)
        ]
        
        if not encontrado.empty:
            self.usuario_actual = correo
            messagebox.showinfo("Éxito", "✅ Inicio de sesión exitoso.")
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "❌ Correo o contraseña incorrectos.")
            
    def crear_cuenta(self):
        """Mostrar ventana para crear nueva cuenta"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Nueva Cuenta")
        ventana.geometry("400x250")
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self.root)
        ventana.grab_set()
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Crear Nueva Cuenta", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Campos
        ttk.Label(main_frame, text="📧 Correo:").pack(anchor="w", pady=5)
        entry_nuevo_email = ttk.Entry(main_frame, width=40)
        entry_nuevo_email.pack(pady=5)
        
        ttk.Label(main_frame, text="🔒 Contraseña:").pack(anchor="w", pady=5)
        entry_nueva_password = ttk.Entry(main_frame, width=40, show="*")
        entry_nueva_password.pack(pady=5)
        
        ttk.Label(main_frame, text="🔑 Clave maestra:").pack(anchor="w", pady=5)
        entry_clave_maestra = ttk.Entry(main_frame, width=40, show="*")
        entry_clave_maestra.pack(pady=5)
        
        def procesar_creacion():
            nuevo_correo = entry_nuevo_email.get().strip()
            nueva_contraseña = entry_nueva_password.get().strip()
            clave = entry_clave_maestra.get().strip()
            
            if not nuevo_correo or not nueva_contraseña or not clave:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
                
            if clave != clave_maestra:
                messagebox.showerror("Error", "❌ Clave maestra incorrecta.")
                return
                
            usuarios_df = cargar_usuarios()
            
            if not usuarios_df.empty and nuevo_correo.lower() in usuarios_df["correo"].str.lower().values:
                messagebox.showerror("Error", "❌ El correo ya está registrado.")
                return
                
            # Crear nueva cuenta
            nuevo_usuario = pd.DataFrame({"correo": [nuevo_correo], "contraseña": [nueva_contraseña]})
            usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)
            guardar_usuarios(usuarios_df)
            
            messagebox.showinfo("Éxito", "✅ Cuenta creada exitosamente.")
            ventana.destroy()
            
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✅ Crear", command=procesar_creacion).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana.destroy).pack(side="left", padx=10)
        
    def mostrar_menu_principal(self):
        """Mostrar el menú principal del sistema"""
        self.limpiar_ventana()
        
        # Inicializar filtro de pedidos
        try:
            self.filtro_pedidos = FiltroPedidos(pedidos)
        except RuntimeError as e:
            messagebox.showerror("Error", f"❌ {e}")
            return
            
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título y usuario
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=10)
        
        ttk.Label(title_frame, text="🌾 Sistema Finca Directa SAS", 
                 style='Title.TLabel').pack()
        ttk.Label(title_frame, text=f"Usuario: {self.usuario_actual}", 
                 style='Subtitle.TLabel').pack()
        
        # Frame para botones del menú
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(expand=True, fill="both", pady=20)
        
        # Configurar grid para botones
        for i in range(3):
            menu_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            menu_frame.grid_rowconfigure(i, weight=1)
            
        # Botones del menú principal
        botones = [
            ("📊 Consultar Demanda de Pedidos (HU4)", self.menu_consulta_pedidos),
            ("📦 Consultar Inventario (HU1)", self.menu_inventario),
            ("✅ Verificar Disponibilidad de Insumos (HU2)", self.menu_verificar_disponibilidad),
            ("📥 Recepción de Insumos (HU5)", self.menu_recepcion_insumos),
            ("📋 Reportes de Recepción (HU7)", self.menu_reportes_recepcion),
            ("🛒 Reportes de Solicitudes de Compra (HU8)", self.menu_reportes_solicitudes),
            ("🚚 Reportes de Insumos Listos (HU10)", self.menu_reportes_insumos_listos),
            ("🚪 Cerrar Sesión", self.cerrar_sesion),
        ]
        
        for i, (texto, comando) in enumerate(botones):
            row = i // 2
            col = i % 2
            btn = ttk.Button(menu_frame, text=texto, command=comando, 
                           style='Big.TButton')
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.usuario_actual = None
        self.mostrar_login()
        
    # ==================== MENÚS ESPECÍFICOS ====================
    
    def menu_consulta_pedidos(self):
        """Menú para consultar demanda de pedidos"""
        ventana = self.crear_ventana_secundaria("📊 Consultar Demanda de Pedidos", "800x600")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Consultar Demanda de Pedidos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para filtros
        filtro_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        filtro_frame.pack(fill="x", pady=10)
        
        # Filtro por fecha
        fecha_frame = ttk.Frame(filtro_frame)
        fecha_frame.pack(fill="x", pady=5)
        
        ttk.Label(fecha_frame, text="📅 Fecha desde:").pack(side="left", padx=5)
        self.entry_fecha_inicio = ttk.Entry(fecha_frame, width=15)
        self.entry_fecha_inicio.pack(side="left", padx=5)
        
        ttk.Label(fecha_frame, text="hasta:").pack(side="left", padx=5)
        self.entry_fecha_fin = ttk.Entry(fecha_frame, width=15)
        self.entry_fecha_fin.pack(side="left", padx=5)
        
        # Filtro por producto
        producto_frame = ttk.Frame(filtro_frame)
        producto_frame.pack(fill="x", pady=5)
        
        ttk.Label(producto_frame, text="📦 Producto:").pack(side="left", padx=5)
        self.entry_producto = ttk.Entry(producto_frame, width=30)
        self.entry_producto.pack(side="left", padx=5)
        
        # Botones de filtro
        btn_frame = ttk.Frame(filtro_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="🔍 Filtrar", 
                  command=self.aplicar_filtros_pedidos).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Reiniciar", 
                  command=self.reiniciar_filtros_pedidos).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📤 Exportar", 
                  command=self.exportar_demanda).pack(side="left", padx=5)
        
        # Área de resultados
        resultado_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        resultado_frame.pack(fill="both", expand=True, pady=10)
        
        # Treeview para mostrar pedidos
        columns = ('ID', 'Fecha', 'Cliente', 'Producto', 'Cantidad')
        self.tree_pedidos = ttk.Treeview(resultado_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=100)
            
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(resultado_frame, orient="vertical", command=self.tree_pedidos.yview)
        scrollbar_h = ttk.Scrollbar(resultado_frame, orient="horizontal", command=self.tree_pedidos.xview)
        self.tree_pedidos.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        self.tree_pedidos.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        resultado_frame.grid_rowconfigure(0, weight=1)
        resultado_frame.grid_columnconfigure(0, weight=1)
        
        # Botón para ver detalle
        ttk.Button(resultado_frame, text="👁️ Ver Detalle", 
                  command=self.ver_detalle_pedido).grid(row=2, column=0, pady=10)
        
        # Cargar todos los pedidos inicialmente
        self.cargar_pedidos_en_tree()
        
    def aplicar_filtros_pedidos(self):
        """Aplicar filtros a los pedidos"""
        inicio = self.entry_fecha_inicio.get().strip()
        fin = self.entry_fecha_fin.get().strip()
        producto = self.entry_producto.get().strip()
        
        try:
            if producto and (inicio or fin):
                # Filtro combinado
                df_filtrado, mensaje, ids = filtrar_pedidos_combinado(
                    self.filtro_pedidos.df, producto, inicio, fin)
            elif producto:
                # Solo filtro por producto
                df_filtrado, mensaje, ids = filtrar_pedidos_por_producto(
                    self.filtro_pedidos.df, producto)
            elif inicio or fin:
                # Solo filtro por fecha
                df_filtrado, mensaje, ids = filtrar_pedidos_por_fecha(
                    self.filtro_pedidos.df, inicio, fin)
            else:
                # Sin filtros
                df_filtrado = self.filtro_pedidos.df
                mensaje = "✅ Mostrando todos los pedidos"
                
            self.filtro_pedidos.df_filtrado = df_filtrado
            self.cargar_pedidos_en_tree(df_filtrado)
            messagebox.showinfo("Resultado", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtros: {e}")
            
    def reiniciar_filtros_pedidos(self):
        """Reiniciar filtros de pedidos"""
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)
        self.entry_producto.delete(0, tk.END)
        self.filtro_pedidos.df_filtrado = self.filtro_pedidos.df.copy()
        self.cargar_pedidos_en_tree()
        messagebox.showinfo("Info", "🔄 Filtros reiniciados")
        
    def cargar_pedidos_en_tree(self, df=None):
        """Cargar pedidos en el Treeview"""
        # Limpiar tree
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)
            
        if df is None:
            df = self.filtro_pedidos.df
            
        # Agregar datos
        for _, row in df.iterrows():
            self.tree_pedidos.insert('', 'end', values=(
                row.get('id', ''),
                row.get('fecha', ''),
                row.get('cliente', ''),
                row.get('producto', ''),
                row.get('cantidad', '')
            ))
            
    def ver_detalle_pedido(self):
        """Ver detalle del pedido seleccionado"""
        selection = self.tree_pedidos.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un pedido para ver el detalle")
            return
            
        item = self.tree_pedidos.item(selection[0])
        pedido_id = item['values'][0]
        
        detalle = obtener_detalle_pedido(self.filtro_pedidos.df_filtrado, pedido_id)
        if detalle:
            messagebox.showinfo("Detalle del Pedido", detalle)
        else:
            messagebox.showerror("Error", "No se pudo obtener el detalle del pedido")
            
    def exportar_demanda(self):
        """Exportar demanda a Excel"""
        if hasattr(self.filtro_pedidos, 'df_filtrado'):
            mensaje, color = exportar_resultados(self.filtro_pedidos.df_filtrado)
            if "Error" in mensaje:
                messagebox.showerror("Error", mensaje)
            else:
                messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showwarning("Advertencia", "No hay datos filtrados para exportar")
            
    def menu_inventario(self):
        """Menú para consultar inventario"""
        ventana = self.crear_ventana_secundaria("📦 Consultar Inventario", "700x500")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Consultar Inventario", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="📋 Mostrar Inventario Completo", 
                  command=self.mostrar_inventario_completo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔍 Buscar Insumo", 
                  command=self.buscar_insumo_gui).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="👁️ Ver Detalle por ID", 
                  command=self.ver_detalle_insumo_gui).pack(side="left", padx=5)
        
        # Área de resultados
        self.text_inventario = tk.Text(main_frame, height=20, width=80)
        scroll_inv = ttk.Scrollbar(main_frame, orient="vertical", command=self.text_inventario.yview)
        self.text_inventario.configure(yscrollcommand=scroll_inv.set)
        
        self.text_inventario.pack(side="left", fill="both", expand=True)
        scroll_inv.pack(side="right", fill="y")
        
    def mostrar_inventario_completo(self):
        """Mostrar el inventario completo"""
        df_inventario = cargar_excel(inventario)
        if df_inventario.empty:
            self.text_inventario.delete(1.0, tk.END)
            self.text_inventario.insert(tk.END, "❌ No hay datos de inventario disponibles.")
            return
            
        self.text_inventario.delete(1.0, tk.END)
        self.text_inventario.insert(tk.END, "📦 INVENTARIO COMPLETO:\n\n")
        
        # Mostrar solo las primeras 18 filas (0-17)
        df_mostrar = df_inventario.loc[0:17, ["producto", "cantidad"]] if len(df_inventario) > 17 else df_inventario[["producto", "cantidad"]]
        
        for idx, row in df_mostrar.iterrows():
            self.text_inventario.insert(tk.END, f"{idx:2d} | {row['producto']:30s} | {row['cantidad']}\n")
            
    def buscar_insumo_gui(self):
        """Buscar insumo por nombre"""
        nombre = tk.simpledialog.askstring("Buscar Insumo", 
                                          "Ingrese el nombre del insumo a buscar:")
        if not nombre:
            return
            
        df_inventario = cargar_excel(inventario)
        df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
        nombre = nombre.lower()
        resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre)]
        
        self.text_inventario.delete(1.0, tk.END)
        if resultado.empty:
            self.text_inventario.insert(tk.END, "❌ No se encontraron insumos con ese nombre.")
        else:
            self.text_inventario.insert(tk.END, f"🔍 Resultados para '{nombre}':\n\n")
            for _, row in resultado.iterrows():
                self.text_inventario.insert(tk.END, 
                    f"Producto: {row['producto']}\n"
                    f"Cantidad: {row['cantidad']}\n"
                    f"Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n\n")
                    
    def ver_detalle_insumo_gui(self):
        """Ver detalle de insumo por ID"""
        try:
            idx = tk.simpledialog.askinteger("Ver Detalle", 
                                           "Ingrese el ID del insumo (0-17):",
                                           minvalue=0, maxvalue=17)
            if idx is None:
                return
                
            df_inventario = cargar_excel(inventario)
            if 0 <= idx <= 17 and idx < len(df_inventario):
                row = df_inventario.iloc[idx]
                detalle = (
                    f"📋 DETALLE DEL INSUMO:\n\n"
                    f"ID: {idx}\n"
                    f"Producto: {row.get('producto', 'N/A')}\n"
                    f"Cantidad: {row.get('cantidad', 'N/A')}\n"
                    f"Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n"
                )
                
                self.text_inventario.delete(1.0, tk.END)
                self.text_inventario.insert(tk.END, detalle)
            else:
                messagebox.showerror("Error", "❌ ID inválido o fuera de rango.")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error: {e}")
            
    def menu_verificar_disponibilidad(self):
        """Menú para verificar disponibilidad de insumos"""
        ventana = self.crear_ventana_secundaria("✅ Verificar Disponibilidad de Insumos", "600x400")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Verificar Disponibilidad de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="📋 Generar Lista de Envío", 
                  command=self.generar_lista_envio_gui).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📧 Enviar Lista por Email", 
                  command=self.enviar_lista_email_gui).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar Inventario", 
                  command=self.actualizar_inventario_gui).pack(side="left", padx=5)
        
        # Área de resultados
        self.text_disponibilidad = tk.Text(main_frame, height=15, width=70)
        scroll_disp = ttk.Scrollbar(main_frame, orient="vertical", command=self.text_disponibilidad.yview)
        self.text_disponibilidad.configure(yscrollcommand=scroll_disp.set)
        
        self.text_disponibilidad.pack(side="left", fill="both", expand=True)
        scroll_disp.pack(side="right", fill="y")
        
    def generar_lista_envio_gui(self):
        """Generar lista de insumos listos para envío"""
        try:
            lista = generar_lista_envio()
            
            self.text_disponibilidad.delete(1.0, tk.END)
            if lista.empty:
                self.text_disponibilidad.insert(tk.END, "❌ No hay insumos que cumplan con la demanda.")
            else:
                self.text_disponibilidad.insert(tk.END, "✅ INSUMOS LISTOS PARA ENVÍO:\n\n")
                for _, row in lista.iterrows():
                    self.text_disponibilidad.insert(tk.END, 
                        f"Producto: {row['producto']}\n"
                        f"Cantidad a enviar: {row['cantidad_a_enviar']}\n\n")
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar lista: {e}")
            
    def enviar_lista_email_gui(self):
        """Enviar lista de insumos por email"""
        try:
            # Llamar a la función de envío
            enviar_lista_insumos()
            messagebox.showinfo("Éxito", "✅ Lista enviada por correo exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar email: {e}")
            
    def actualizar_inventario_gui(self):
        """Actualizar inventario con las cantidades demandadas"""
        try:
            actualizar_inventario()
            messagebox.showinfo("Éxito", "✅ Inventario actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar inventario: {e}")
            
    def menu_recepcion_insumos(self):
        """Menú para recepción de insumos"""
        ventana = self.crear_ventana_secundaria("📥 Recepción de Insumos", "700x600")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Recepción de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para información del pedido
        info_frame = ttk.LabelFrame(main_frame, text="Información del Pedido", padding="10")
        info_frame.pack(fill="x", pady=10)
        
        # Campos de información
        ttk.Label(info_frame, text="Proveedor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_proveedor = ttk.Entry(info_frame, width=30)
        self.entry_proveedor.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_fecha_recepcion = ttk.Entry(info_frame, width=30)
        self.entry_fecha_recepcion.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Número de pedido:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_numero_pedido = ttk.Entry(info_frame, width=30)
        self.entry_numero_pedido.grid(row=2, column=1, padx=5, pady=5)
        
        # Productos recibidos
        productos_frame = ttk.LabelFrame(main_frame, text="Productos Recibidos", padding="10")
        productos_frame.pack(fill="both", expand=True, pady=10)
        
        # Lista de productos
        self.productos_recibidos = []
        
        # Frame para agregar productos
        add_frame = ttk.Frame(productos_frame)
        add_frame.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="Producto:").pack(side="left", padx=5)
        self.entry_producto_nuevo = ttk.Entry(add_frame, width=20)
        self.entry_producto_nuevo.pack(side="left", padx=5)
        
        ttk.Label(add_frame, text="Cantidad:").pack(side="left", padx=5)
        self.entry_cantidad_nueva = ttk.Entry(add_frame, width=10)
        self.entry_cantidad_nueva.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="➕ Agregar", 
                  command=self.agregar_producto_recibido).pack(side="left", padx=5)
        
        # Lista de productos agregados
        self.list_productos = tk.Listbox(productos_frame, height=8)
        self.list_productos.pack(fill="both", expand=True, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="✅ Procesar Recepción", 
                  command=self.procesar_recepcion_completa).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Limpiar", 
                  command=self.limpiar_recepcion).pack(side="left", padx=5)
        
    def agregar_producto_recibido(self):
        """Agregar producto a la lista de productos recibidos"""
        producto = self.entry_producto_nuevo.get().strip()
        try:
            cantidad = int(self.entry_cantidad_nueva.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
            
        if not producto or cantidad <= 0:
            messagebox.showerror("Error", "Ingrese un producto válido y cantidad mayor a 0")
            return
            
        self.productos_recibidos.append((producto, cantidad))
        self.list_productos.insert(tk.END, f"{producto} - {cantidad} unidades")
        
        # Limpiar campos
        self.entry_producto_nuevo.delete(0, tk.END)
        self.entry_cantidad_nueva.delete(0, tk.END)
        
    def limpiar_recepcion(self):
        """Limpiar todos los campos de recepción"""
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_recepcion.delete(0, tk.END)
        self.entry_numero_pedido.delete(0, tk.END)
        self.entry_producto_nuevo.delete(0, tk.END)
        self.entry_cantidad_nueva.delete(0, tk.END)
        self.list_productos.delete(0, tk.END)
        self.productos_recibidos = []
        
    def procesar_recepcion_completa(self):
        """Procesar la recepción completa de insumos"""
        proveedor = self.entry_proveedor.get().strip()
        fecha = self.entry_fecha_recepcion.get().strip()
        numero_pedido = self.entry_numero_pedido.get().strip()
        
        if not proveedor or not fecha or not numero_pedido:
            messagebox.showerror("Error", "Todos los campos de información son obligatorios")
            return
            
        if not self.productos_recibidos:
            messagebox.showerror("Error", "Debe agregar al menos un producto")
            return
            
        try:
            # Validar fecha
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida. Debe tener formato YYYY-MM-DD.")
            return
            
        try:
            # Registrar la recepción (simular el proceso completo)
            # 1. Registrar entrega
            df_entregas = cargar_excel(entregas)
            nuevo_id = 1 if df_entregas.empty else df_entregas['id'].max() + 1
            nueva_entrega = pd.DataFrame([[nuevo_id, proveedor, fecha, numero_pedido, len(self.productos_recibidos)]],
                                        columns=["id", "proveedor", "fecha", "numero_pedido", "cantidades_entregadas"])
            df_entregas = pd.concat([df_entregas, nueva_entrega], ignore_index=True)
            guardar_excel(df_entregas, entregas)
            
            # 2. Guardar detalle
            guardar_detalle_entrega(self.productos_recibidos, nuevo_id)
            
            # 3. Validar campos
            if not validar_campos(self.productos_recibidos):
                return
                
            # 4. Verificar calidad (simplificado - asumir conformes)
            productos_validados = self.productos_recibidos.copy()
            
            # 5. Ingresar al inventario
            ingresar_inventario(productos_validados)
            
            messagebox.showinfo("Éxito", f"✅ Recepción procesada exitosamente. ID de entrega: {nuevo_id}")
            self.limpiar_recepcion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar recepción: {e}")
            
    def menu_reportes_recepcion(self):
        """Menú para reportes de recepción"""
        ventana = self.crear_ventana_secundaria("📋 Reportes de Recepción", "800x600")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Reportes de Recepción de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para filtros de fecha
        filtro_frame = ttk.LabelFrame(main_frame, text="Filtrar por Fechas", padding="10")
        filtro_frame.pack(fill="x", pady=10)
        
        fecha_frame = ttk.Frame(filtro_frame)
        fecha_frame.pack(fill="x")
        
        ttk.Label(fecha_frame, text="Fecha inicio:").pack(side="left", padx=5)
        self.entry_fecha_ini_reporte = ttk.Entry(fecha_frame, width=15)
        self.entry_fecha_ini_reporte.pack(side="left", padx=5)
        
        ttk.Label(fecha_frame, text="Fecha fin:").pack(side="left", padx=5)
        self.entry_fecha_fin_reporte = ttk.Entry(fecha_frame, width=15)
        self.entry_fecha_fin_reporte.pack(side="left", padx=5)
        
        ttk.Button(fecha_frame, text="🔍 Filtrar", 
                  command=self.filtrar_reportes_fecha).pack(side="left", padx=10)
        
        # Lista de reportes
        lista_frame = ttk.LabelFrame(main_frame, text="Reportes Disponibles", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        self.list_reportes = tk.Listbox(lista_frame, height=10)
        scroll_reportes = ttk.Scrollbar(lista_frame, orient="vertical", command=self.list_reportes.yview)
        self.list_reportes.configure(yscrollcommand=scroll_reportes.set)
        
        self.list_reportes.pack(side="left", fill="both", expand=True)
        scroll_reportes.pack(side="right", fill="y")
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="👁️ Ver Reporte", 
                  command=self.ver_reporte_seleccionado).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Descargar", 
                  command=self.descargar_reporte_seleccionado).pack(side="left", padx=5)
        
    def filtrar_reportes_fecha(self):
        """Filtrar reportes por fecha"""
        fecha_ini = self.entry_fecha_ini_reporte.get().strip()
        fecha_fin = self.entry_fecha_fin_reporte.get().strip()
        
        if not fecha_ini or not fecha_fin:
            messagebox.showerror("Error", "Ambas fechas son obligatorias")
            return
            
        try:
            df_entregas = pd.read_excel(entregas)
            if df_entregas.empty:
                messagebox.showinfo("Info", "No hay entregas registradas.")
                return
                
            df_entregas['fecha'] = pd.to_datetime(df_entregas['fecha'])
            ini = pd.to_datetime(fecha_ini)
            fin = pd.to_datetime(fecha_fin)
            
            self.df_reporte_filtrado = df_entregas[(df_entregas['fecha'] >= ini) & (df_entregas['fecha'] <= fin)]
            
            # Actualizar lista
            self.list_reportes.delete(0, tk.END)
            if self.df_reporte_filtrado.empty:
                self.list_reportes.insert(tk.END, "No hay entregas en ese rango de fechas")
            else:
                for _, row in self.df_reporte_filtrado.iterrows():
                    fecha_str = row['fecha'].strftime('%Y-%m-%d')
                    texto = f"ID: {row['id']} | {fecha_str} | {row['proveedor']} | Pedido: {row['numero_pedido']}"
                    self.list_reportes.insert(tk.END, texto)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar: {e}")
            
    def ver_reporte_seleccionado(self):
        """Ver el reporte seleccionado"""
        selection = self.list_reportes.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un reporte")
            return
            
        if self.df_reporte_filtrado.empty:
            messagebox.showwarning("Advertencia", "Primero filtre por fechas")
            return
            
        index = selection[0]
        row = self.df_reporte_filtrado.iloc[index]
        id_entrega = row['id']
        
        # Generar y mostrar reporte
        try:
            df_detalle = pd.read_excel(detalle_entregas)
            detalle = df_detalle[df_detalle['id_entrega'] == id_entrega].copy()
            
            if "conforme" not in detalle.columns:
                detalle["conforme"] = True
                
            # Crear ventana de detalle
            ventana_detalle = tk.Toplevel(self.root)
            ventana_detalle.title(f"Detalle Reporte ID: {id_entrega}")
            ventana_detalle.geometry("600x400")
            
            text_detalle = tk.Text(ventana_detalle, wrap=tk.WORD)
            scroll_detalle = ttk.Scrollbar(ventana_detalle, orient="vertical", command=text_detalle.yview)
            text_detalle.configure(yscrollcommand=scroll_detalle.set)
            
            # Mostrar información
            info_text = f"""DETALLE DE RECEPCIÓN
            
Proveedor: {row['proveedor']}
Fecha: {row['fecha'].strftime('%Y-%m-%d')}
Número de Pedido: {row['numero_pedido']}
Cantidad de productos: {row['cantidades_entregadas']}

PRODUCTOS RECIBIDOS:
"""
            text_detalle.insert(tk.END, info_text)
            
            for _, det_row in detalle.iterrows():
                estado = "✅ Conforme" if det_row.get("conforme", True) else "❌ No conforme"
                text_detalle.insert(tk.END, f"- {det_row['producto']}: {det_row['cantidad']} unidades - {estado}\n")
                
            text_detalle.pack(side="left", fill="both", expand=True)
            scroll_detalle.pack(side="right", fill="y")
            
            # Generar archivo Excel
            salida = detalle.copy()
            salida.insert(0, "Proveedor", row['proveedor'])
            salida.insert(1, "Fecha", row['fecha'].strftime('%Y-%m-%d'))
            salida.insert(2, "Pedido", row['numero_pedido'])
            salida['conformidad'] = salida['conforme'].apply(lambda x: "Conforme" if x else "No conforme")
            salida = salida[["Proveedor", "Fecha", "Pedido", "producto", "cantidad", "conformidad"]]
            
            nombre_archivo = os.path.join(os.path.dirname(entregas), f"reporte_pedido_{id_entrega}.xlsx")
            salida.to_excel(nombre_archivo, index=False)
            
            messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")
            
    def descargar_reporte_seleccionado(self):
        """Mostrar reportes disponibles para descarga"""
        carpeta = os.path.dirname(entregas)
        archivos = [f for f in os.listdir(carpeta) if f.startswith("reporte_pedido_") and f.endswith(".xlsx")]
        
        if not archivos:
            messagebox.showinfo("Info", "No hay reportes generados para descargar.")
        else:
            mensaje = "Reportes disponibles en la carpeta 'data/':\n\n" + "\n".join(archivos)
            messagebox.showinfo("Reportes Disponibles", mensaje)
            
    def menu_reportes_solicitudes(self):
        """Menú para reportes de solicitudes de compra"""
        messagebox.showinfo("Info", "Funcionalidad de reportes de solicitudes - Por implementar")
        
    def menu_reportes_insumos_listos(self):
        """Menú para reportes de insumos listos"""
        messagebox.showinfo("Info", "Funcionalidad de reportes de insumos listos - Por implementar")
        
    # ==================== MÉTODOS AUXILIARES ====================
    
    def crear_ventana_secundaria(self, titulo, tamaño):
        """Crear una ventana secundaria"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(tamaño)
        ventana.configure(bg="#f0f0f0")
        ventana.transient(self.root)
        return ventana
        
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal para ejecutar la aplicación"""
    try:
        app = SistemaFincaDirectaGUI()
        app.ejecutar()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()
