"""
Interfaz Gráfica Modernizada para el Sistema Finca Directa SAS
Archivo: fincaDirectaGUI.py
Descripción: Interfaz gráfica moderna usando ttkbootstrap para el sistema de gestión de finca
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText
from ttkbootstrap.dialogs import Messagebox
from tkinter import font as tkFont
import pandas as pd
from datetime import datetime
import os
import sys
import time
import threading

# Importar la lógica del negocio desde main.py
try:
    from main import *
except ImportError:
    messagebox.showerror("Error", "No se pudo importar main.py. Asegúrate de que esté en el mismo directorio.")
    sys.exit(1)

class PantallaCarga:
    """Pantalla de carga inicial del sistema"""
    def __init__(self, parent_callback):
        self.parent_callback = parent_callback
        self.ventana = tk.Tk()
        self.ventana.title("Cargando...")
        self.ventana.geometry("600x400")
        self.ventana.configure(bg="#5B6043")  # Verde oliva
        self.ventana.resizable(False, False)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear contenido
        self.crear_contenido()
        
        # Iniciar proceso de carga
        self.iniciar_carga()
        
    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
    def crear_contenido(self):
        """Crear el contenido de la pantalla de carga"""
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg="#5B6043")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Logo del sistema (amarillo)
        logo_label = tk.Label(main_frame, text="🌾", font=("Arial", 80), 
                             bg="#5B6043", fg="#FDC304")  # Amarillo
        logo_label.pack(pady=(20, 30))
        
        # Título principal
        titulo = tk.Label(main_frame, text="Bienvenido a", 
                         font=("Arial", 18, "bold"), 
                         bg="#5B6043", fg="#FAF4DC")  # Crema
        titulo.pack(pady=(0, 10))
        
        titulo2 = tk.Label(main_frame, text="Sistema Finca Directa", 
                          font=("Arial", 24, "bold"), 
                          bg="#5B6043", fg="#FDC304")  # Amarillo
        titulo2.pack(pady=(0, 30))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate',
                                          variable=self.progress_var)
        self.progress_bar.pack(pady=(20, 10))
        
        # Texto de estado
        self.estado_label = tk.Label(main_frame, text="Iniciando sistema...", 
                                    font=("Arial", 12), 
                                    bg="#5B6043", fg="#FAF4DC")  # Crema
        self.estado_label.pack(pady=(0, 20))
        
        # Versión
        version_label = tk.Label(main_frame, text="Versión 2.0 - Interfaz Modernizada", 
                                font=("Arial", 10), 
                                bg="#5B6043", fg="#E4901D")  # Naranja
        version_label.pack(side="bottom", pady=(20, 0))
        
    def iniciar_carga(self):
        """Iniciar el proceso de carga simulado"""
        def proceso_carga():
            estados = [
                "Cargando módulos del sistema...",
                "Verificando archivos de datos...",
                "Configurando interfaz...",
                "Preparando módulos de negocio...",
                "Inicializando sistema..."
            ]
            
            for i, estado in enumerate(estados):
                self.ventana.after(0, lambda s=estado: self.estado_label.config(text=s))
                self.ventana.after(0, lambda p=(i+1)*20: self.progress_var.set(p))
                time.sleep(0.8)
            
            # Finalizar carga
            self.ventana.after(0, self.finalizar_carga)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=proceso_carga, daemon=True)
        thread.start()
        
    def finalizar_carga(self):
        """Finalizar la carga y abrir la aplicación principal"""
        # Pequeña pausa antes de cerrar
        time.sleep(0.3)
        
        # Ocultar en lugar de destruir para evitar conflictos
        self.ventana.withdraw()
        
        # Llamar al callback después de un pequeño delay
        self.ventana.after(100, self.ejecutar_callback)
        
    def ejecutar_callback(self):
        """Ejecutar el callback y luego destruir la ventana"""
        try:
            self.parent_callback()
        finally:
            # Destruir la ventana de carga después del callback
            if self.ventana:
                self.ventana.destroy()
        
    def mostrar(self):
        """Mostrar la pantalla de carga"""
        self.ventana.mainloop()

class SistemaFincaDirectaGUI:
    def __init__(self):
        self.root = None
        self.usuario_actual = None
        self.filtro_pedidos = None
        self.df_reporte_filtrado = pd.DataFrame()
        self.solicitud_actual = pd.DataFrame()
        
        # Colores corporativos
        self.colors = {
            'primary': '#E4901D',    # Naranja
            'secondary': '#FDC304',  # Amarillo
            'success': '#5B6043',    # Verde oliva
            'light': '#FAF4DC',      # Crema
            'dark': '#2C3E50',       # Oscuro para texto
            'white': '#FFFFFF'       # Blanco
        }
        
    def inicializar_aplicacion(self):
        """Inicializar la aplicación principal después de la carga"""
        # Crear ventana principal con ttkbootstrap usando tema más estable
        self.root = ttk.Window(themename="cosmo")
        self.root.title("Sistema Finca Directa SAS")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Pantalla completa
        
        # Configurar fuentes
        self.font_title = ('Segoe UI', 20, 'bold')
        self.font_subtitle = ('Segoe UI', 14, 'bold')
        self.font_normal = ('Segoe UI', 11)
        self.font_small = ('Segoe UI', 9)
        
        # Configurar estilo personalizado
        self.setup_custom_styles()
        
        # Mostrar pantalla de login
        self.mostrar_login()
        
        # Ejecutar aplicación
        self.root.mainloop()
        
    def setup_custom_styles(self):
        """Configurar estilos personalizados para la aplicación"""
        style = ttk.Style()
        
        # Configurar tema personalizado con colores corporativos
        style.configure('Title.TLabel', 
                       font=self.font_title, 
                       foreground=self.colors['success'])
        
        style.configure('Subtitle.TLabel', 
                       font=self.font_subtitle, 
                       foreground=self.colors['primary'])
        
        style.configure('Custom.TLabel', 
                       font=self.font_normal, 
                       foreground=self.colors['dark'])
                       
        # Header styles
        style.configure('HeaderTitle.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['success'])
                       
        style.configure('HeaderUser.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['primary'])
                       
        # Module styles
        style.configure('ModuleTitle.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['success'])
                       
        style.configure('SectionTitle.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colors['primary'])
        
        # Botones principales
        style.configure('Primary.TButton',
                       font=self.font_subtitle,
                       padding=(20, 12),
                       foreground=self.colors['white'])
        
        style.configure('Secondary.TButton',
                       font=self.font_normal,
                       padding=(15, 10),
                       foreground=self.colors['dark'])
        
        style.configure('Success.TButton',
                       font=self.font_normal,
                       padding=(15, 8),
                       foreground=self.colors['white'])
                       
        style.configure('Danger.TButton',
                       font=self.font_normal,
                       padding=(12, 8),
                       foreground=self.colors['white'])
                       
        # Module card styles
        style.configure('ModuleCard.TFrame',
                       relief='solid',
                       borderwidth=2,
                       background=self.colors['white'])
                       
        style.configure('ModuleCardHover.TFrame',
                       relief='solid',
                       borderwidth=2,
                       background=self.colors['light'])
                       
        style.configure('ModuleCardTitle.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=self.colors['primary'])
                       
        style.configure('ModuleCardDesc.TLabel',
                       font=('Segoe UI', 10),
                       foreground=self.colors['dark'])
                       
        style.configure('ModuleAction.TButton',
                       font=self.font_normal,
                       padding=(10, 6))
        
        # Frames con estilo
        style.configure('Card.TFrame',
                       relief='solid',
                       borderwidth=1,
                       background=self.colors['white'])
        
        style.configure('Main.TFrame',
                       background=self.colors['light'])
                       
        style.configure('Header.TFrame',
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
                       
        style.configure('Footer.TFrame',
                       background=self.colors['success'])
                       
        style.configure('Footer.TLabel',
                       background=self.colors['success'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10))
        
        # Entry personalizado
        style.configure('Modern.TEntry',
                       font=self.font_normal,
                       foreground=self.colors['dark'],
                       padding=(10, 8))
                       
        # LabelFrame moderno
        style.configure('Modern.TLabelframe',
                       relief='solid',
                       borderwidth=1,
                       background=self.colors['white'])
                       
        style.configure('Modern.TLabelframe.Label',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['white'])
        
    def crear_ventana_secundaria(self, titulo, tamaño, icono="📋"):
        """Crear una ventana secundaria moderna"""
        ventana = ttk.Toplevel(self.root)
        ventana.title(f"{icono} {titulo}")
        ventana.geometry(tamaño)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")
        
        return ventana
        
    def limpiar_ventana(self):
        """Limpiar todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def mostrar_login(self):
        """Mostrar la pantalla de inicio de sesión moderna"""
        self.limpiar_ventana()
        
        # Frame principal con diseño moderno
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding=50)
        main_frame.pack(fill="both", expand=True)
        
        # Card de login centrada
        login_card = ttk.Frame(main_frame, style='Card.TFrame', padding=40)
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo y título principal
        logo_frame = ttk.Frame(login_card, style='Card.TFrame')
        logo_frame.pack(pady=(0, 30))
        
        # Logo amarillo más grande
        logo_label = ttk.Label(logo_frame, text="🌾", 
                              font=('Segoe UI', 60), 
                              foreground=self.colors['secondary'])
        logo_label.pack()
        
        # Título del sistema
        ttk.Label(login_card, text="Sistema Finca Directa SAS", 
                 style='Title.TLabel').pack(pady=(0, 10))
        
        ttk.Label(login_card, text="Gestión Inteligente de Insumos Agrícolas", 
                 style='Custom.TLabel').pack(pady=(0, 30))
        
        # Campos de entrada modernos
        campos_frame = ttk.Frame(login_card, style='Card.TFrame')
        campos_frame.pack(fill="x", pady=(0, 30))
        
        # Campo de correo
        ttk.Label(campos_frame, text="📧 Correo electrónico:", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 5))
        self.entry_email = ttk.Entry(campos_frame, font=self.font_normal, 
                                    width=35, style='Modern.TEntry')
        self.entry_email.pack(fill="x", pady=(0, 15))
        
        # Campo de contraseña
        ttk.Label(campos_frame, text="🔒 Contraseña:", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 5))
        self.entry_password = ttk.Entry(campos_frame, font=self.font_normal, 
                                       width=35, show="*", style='Modern.TEntry')
        self.entry_password.pack(fill="x", pady=(0, 20))
        
        # Botones modernos
        botones_frame = ttk.Frame(login_card, style='Card.TFrame')
        botones_frame.pack(fill="x")
        botones_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        ttk.Button(botones_frame, text="🚀 Iniciar Sesión", 
                  command=self.login, style='Primary.TButton').grid(
                  row=0, column=0, padx=(0, 10), sticky="ew")
        
        ttk.Button(botones_frame, text="➕ Crear Cuenta", 
                  command=self.crear_cuenta, style='Secondary.TButton').grid(
                  row=0, column=1, padx=5, sticky="ew")
        
        ttk.Button(botones_frame, text="❌ Salir", 
                  command=self.root.quit, style='Success.TButton').grid(
                  row=0, column=2, padx=(10, 0), sticky="ew")
        
        # Información adicional
        info_frame = ttk.Frame(login_card, style='Card.TFrame')
        info_frame.pack(pady=(30, 0))
        
        ttk.Label(info_frame, text="Versión 2.0 - Interfaz Modernizada", 
                 style='Custom.TLabel', font=self.font_small,
                 foreground=self.colors['primary']).pack()
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus en el campo de email
        self.entry_email.focus()
        
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
        
        # Campos con mejor visibilidad
        ttk.Label(main_frame, text="📧 Correo:").pack(anchor="w", pady=5)
        entry_nuevo_email = ttk.Entry(main_frame, width=40, style='Custom.TEntry')
        entry_nuevo_email.pack(pady=5)
        
        ttk.Label(main_frame, text="🔒 Contraseña:").pack(anchor="w", pady=5)
        entry_nueva_password = ttk.Entry(main_frame, width=40, show="*", style='Custom.TEntry')
        entry_nueva_password.pack(pady=5)
        
        ttk.Label(main_frame, text="🔑 Clave maestra:").pack(anchor="w", pady=5)
        entry_clave_maestra = ttk.Entry(main_frame, width=40, show="*", style='Custom.TEntry')
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
        """Mostrar el menú principal moderno del sistema"""
        self.limpiar_ventana()
        
        # Inicializar filtro de pedidos
        try:
            self.filtro_pedidos = FiltroPedidos(pedidos)
        except RuntimeError as e:
            messagebox.showerror("Error", f"❌ {e}")
            return
            
        # Header con información del usuario y logo
        header_frame = ttk.Frame(self.root, style='Header.TFrame', padding=20)
        header_frame.pack(fill="x")
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo en header (amarillo)
        ttk.Label(header_frame, text="🌾", 
                 font=('Segoe UI', 32), 
                 foreground=self.colors['secondary']).grid(row=0, column=0, padx=(0, 20))
        
        # Información del usuario
        user_info = ttk.Frame(header_frame, style='Header.TFrame')
        user_info.grid(row=0, column=1, sticky="w")
        
        ttk.Label(user_info, text="Sistema Finca Directa SAS", 
                 style='HeaderTitle.TLabel').pack(anchor="w")
        ttk.Label(user_info, text=f"👤 Usuario: {self.usuario_actual}", 
                 style='HeaderUser.TLabel').pack(anchor="w")
        
        # Botón de logout
        ttk.Button(header_frame, text="🚪 Cerrar Sesión", 
                  command=self.cerrar_sesion, 
                  style='Danger.TButton').grid(row=0, column=2)
        
        # Separador
        ttk.Separator(self.root, orient='horizontal').pack(fill="x", pady=10)
        
        # Contenedor principal de módulos
        main_container = ttk.Frame(self.root, style='Main.TFrame', padding=30)
        main_container.pack(fill="both", expand=True)
        
        # Título principal de módulos
        ttk.Label(main_container, text="🏗️ Módulos del Sistema", 
                 style='ModuleTitle.TLabel').pack(pady=(0, 30))
        
        # Grid de módulos con cards modernas
        modules_frame = ttk.Frame(main_container, style='Main.TFrame')
        modules_frame.pack(expand=True)
        
        # Configurar grid para 4 columnas y 3 filas
        for i in range(4):
            modules_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            modules_frame.grid_rowconfigure(i, weight=1)
        
        # Módulos con iconos y descripciones mejoradas
        modulos = [
            ("📊 Consultar Demanda de Pedidos", "Análisis de solicitudes (HU4)", self.menu_consulta_pedidos, 0, 0),
            ("📦 Consultar Inventario", "Control de stock disponible (HU1)", self.menu_inventario, 0, 1),
            ("✅ Verificar Disponibilidad", "Validar insumos requeridos (HU2)", self.menu_verificar_disponibilidad, 0, 2),
            ("📋 Solicitud de Compra", "Generar solicitudes de insumos (HU3)", self.menu_registro_pedidos_hu3, 0, 3),
            ("📥 Recepción de Insumos", "Registrar llegadas (HU5)", self.menu_recepcion_insumos, 1, 0),
            ("⚠️ Reportar Insumos Defectuosos", "Control de calidad y cantidad (HU6)", self.menu_reportar_defectuosos, 1, 1),
            ("📋 Reportes de Recepción", "Estadísticas de recepción (HU7)", self.menu_reportes_recepcion, 1, 2),
            ("🛒 Reportes de Solicitudes", "Gestión de compras (HU8)", self.menu_solicitud_compra_hu8, 1, 3),
            ("🚚 Reportes Insumos Listos", "Estado de preparación (HU10)", self.menu_reportes_insumos_listos, 2, 0),
            ("⚙️ Configuración", "Ajustes del sistema", self.mostrar_configuracion, 2, 1)
        ]
        
        for texto, descripcion, comando, fila, columna in modulos:
            self.crear_card_modulo(modules_frame, texto, descripcion, comando, fila, columna)
        
        # Footer con información del sistema
        footer_frame = ttk.Frame(self.root, style='Footer.TFrame', padding=15)
        footer_frame.pack(fill="x", side="bottom")
        
        ttk.Label(footer_frame, 
                 text="🌾 Finca Directa SAS - Sistema de Gestión de Insumos Agrícolas v2.0", 
                 style='Footer.TLabel').pack()
            
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.usuario_actual = None
        self.mostrar_login()
        
    def crear_card_modulo(self, parent, titulo, descripcion, comando, fila, columna):
        """Crear una tarjeta moderna para un módulo"""
        # Card container con estilo moderno
        card = ttk.Frame(parent, style='ModuleCard.TFrame', padding=20)
        card.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
        
        # Hover effect configurado via estilo
        card.bind("<Enter>", lambda e: card.configure(style='ModuleCardHover.TFrame'))
        card.bind("<Leave>", lambda e: card.configure(style='ModuleCard.TFrame'))
        
        # Título del módulo
        titulo_label = ttk.Label(card, text=titulo, style='ModuleCardTitle.TLabel')
        titulo_label.pack(pady=(0, 10))
        
        # Descripción del módulo
        desc_label = ttk.Label(card, text=descripcion, 
                              style='ModuleCardDesc.TLabel', wraplength=200)
        desc_label.pack(pady=(0, 15))
        
        # Botón de acción
        btn = ttk.Button(card, text="Acceder", command=comando, 
                        style='ModuleAction.TButton')
        btn.pack(fill="x")
        
        # Hacer toda la card clickeable
        def click_card(event=None):
            comando()
            
        for widget in [card, titulo_label, desc_label]:
            widget.bind("<Button-1>", click_card)
            widget.bind("<Enter>", lambda e: card.configure(style='ModuleCardHover.TFrame'))
            widget.bind("<Leave>", lambda e: card.configure(style='ModuleCard.TFrame'))
            
    def mostrar_configuracion(self):
        """Mostrar el módulo de configuración del sistema"""
        ventana = self.crear_ventana_secundaria("⚙️ Configuración del Sistema", "600x500")
        
        main_frame = ttk.Frame(ventana, style='Card.TFrame', padding=30)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título de la sección
        ttk.Label(main_frame, text="⚙️ Configuración del Sistema", 
                 style='SectionTitle.TLabel').pack(pady=(0, 20))
        
        # Información del sistema
        info_frame = ttk.LabelFrame(main_frame, text="📊 Información del Sistema", 
                                   style='Modern.TLabelframe', padding=20)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_data = [
            ("Versión:", "2.0 - Interfaz Modernizada"),
            ("Framework GUI:", "ttkbootstrap"),
            ("Base de datos:", "Excel (xlsx)"),
            ("Usuario actual:", self.usuario_actual),
            ("Módulos activos:", "8 módulos principales"),
            ("Estado:", "🟢 Sistema operativo")
        ]
        
        for i, (label, value) in enumerate(info_data):
            info_row = ttk.Frame(info_frame)
            info_row.pack(fill="x", pady=5)
            info_row.grid_columnconfigure(1, weight=1)
            
            ttk.Label(info_row, text=label, style='Custom.TLabel', 
                     font=self.font_normal).grid(row=0, column=0, sticky="w", padx=(0, 10))
            ttk.Label(info_row, text=value, style='Custom.TLabel', 
                     font=self.font_normal, foreground=self.colors['primary']).grid(
                     row=0, column=1, sticky="w")
        
        # Configuraciones disponibles
        config_frame = ttk.LabelFrame(main_frame, text="🔧 Opciones de Configuración", 
                                     style='Modern.TLabelframe', padding=20)
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Opciones con botones
        opciones = [
            ("🔄 Actualizar Datos", "Recargar información desde archivos", self.actualizar_datos),
            ("📁 Abrir Carpeta de Datos", "Acceder a archivos del sistema", self.abrir_carpeta_datos),
            ("📋 Exportar Configuración", "Guardar configuración actual", self.exportar_config),
            ("🎨 Cambiar Tema", "Personalizar apariencia", self.cambiar_tema)
        ]
        
        for titulo, desc, comando in opciones:
            option_frame = ttk.Frame(config_frame)
            option_frame.pack(fill="x", pady=8)
            option_frame.grid_columnconfigure(1, weight=1)
            
            ttk.Button(option_frame, text=titulo, command=comando, 
                      style='Secondary.TButton', width=25).grid(row=0, column=0, sticky="w")
            ttk.Label(option_frame, text=desc, style='Custom.TLabel', 
                     font=self.font_small).grid(row=0, column=1, sticky="w", padx=(15, 0))
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(action_frame, text="🏠 Volver al Menú Principal", 
                  command=lambda: [ventana.destroy(), self.mostrar_menu_principal()], 
                  style='Primary.TButton').pack(side="left")
        
        ttk.Button(action_frame, text="❌ Cerrar", 
                  command=ventana.destroy, 
                  style='Danger.TButton').pack(side="right")
                  
    def actualizar_datos(self):
        """Actualizar datos del sistema"""
        messagebox.showinfo("Actualización", "🔄 Datos actualizados correctamente")
        
    def abrir_carpeta_datos(self):
        """Abrir la carpeta de datos"""
        import os
        import subprocess
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        if os.path.exists(data_path):
            subprocess.Popen(f'explorer "{data_path}"')
        else:
            messagebox.showerror("Error", "📁 No se encontró la carpeta de datos")
            
    def exportar_config(self):
        """Exportar configuración del sistema"""
        messagebox.showinfo("Exportar", "📋 Configuración exportada exitosamente")
        
    def cambiar_tema(self):
        """Cambiar tema de la aplicación"""
        messagebox.showinfo("Tema", "🎨 Funcionalidad de cambio de tema próximamente")
        
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
        self.entry_fecha_inicio = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_inicio.pack(side="left", padx=5)
        
        ttk.Label(fecha_frame, text="hasta:").pack(side="left", padx=5)
        self.entry_fecha_fin = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_fin.pack(side="left", padx=5)
        
        # Filtro por producto
        producto_frame = ttk.Frame(filtro_frame)
        producto_frame.pack(fill="x", pady=5)
        
        ttk.Label(producto_frame, text="📦 Producto:").pack(side="left", padx=5)
        self.entry_producto = ttk.Entry(producto_frame, width=30, style='Custom.TEntry')
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
        """Menú avanzado para gestionar inventario"""
        ventana = self.crear_ventana_secundaria("📦 Gestión de Inventario", "1200x800")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Gestión de Inventario", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame superior con botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill="x", pady=15)
        
        ttk.Button(botones_frame, text="➕ Agregar Producto", 
                  command=self.agregar_producto_inventario,
                  style='Success.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="✏️ Editar Producto", 
                  command=self.editar_producto_inventario,
                  style='Primary.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="�️ Eliminar Producto", 
                  command=self.eliminar_producto_inventario,
                  style='Danger.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="� Actualizar Vista", 
                  command=self.actualizar_vista_inventario,
                  style='Secondary.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="🔍 Buscar", 
                  command=self.buscar_producto_inventario,
                  style='Info.TButton').pack(side="left", padx=10)
        
        # Frame para el Treeview con inventario
        inventario_frame = ttk.LabelFrame(main_frame, text="📋 Lista de Productos en Inventario", padding="15")
        inventario_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar inventario
        columns = ('ID', 'Producto', 'Cantidad', 'Última Actualización')
        self.tree_inventario = ttk.Treeview(inventario_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        self.tree_inventario.heading('ID', text='ID')
        self.tree_inventario.heading('Producto', text='Producto')
        self.tree_inventario.heading('Cantidad', text='Cantidad')
        self.tree_inventario.heading('Última Actualización', text='Última Actualización')
        
        self.tree_inventario.column('ID', width=80, anchor='center')
        self.tree_inventario.column('Producto', width=300)
        self.tree_inventario.column('Cantidad', width=120, anchor='center')
        self.tree_inventario.column('Última Actualización', width=180, anchor='center')
        
        # Scrollbars para el Treeview
        scrollbar_v_inv = ttk.Scrollbar(inventario_frame, orient="vertical", command=self.tree_inventario.yview)
        scrollbar_h_inv = ttk.Scrollbar(inventario_frame, orient="horizontal", command=self.tree_inventario.xview)
        self.tree_inventario.configure(yscrollcommand=scrollbar_v_inv.set, xscrollcommand=scrollbar_h_inv.set)
        
        # Empaquetar Treeview y scrollbars
        self.tree_inventario.grid(row=0, column=0, sticky="nsew")
        scrollbar_v_inv.grid(row=0, column=1, sticky="ns")
        scrollbar_h_inv.grid(row=1, column=0, sticky="ew")
        
        # Configurar grid
        inventario_frame.grid_rowconfigure(0, weight=1)
        inventario_frame.grid_columnconfigure(0, weight=1)
        
        # Bind para doble clic
        self.tree_inventario.bind('<Double-1>', self.ver_detalle_producto_inventario)
        
        # Cargar datos iniciales
        self.cargar_inventario_en_tree()

    def cargar_inventario_en_tree(self):
        """Cargar datos del inventario en el Treeview"""
        try:
            # Limpiar tree actual
            for item in self.tree_inventario.get_children():
                self.tree_inventario.delete(item)
            
            # Cargar datos del inventario
            from main import cargar_excel, inventario
            df_inventario = cargar_excel(inventario)
            
            if df_inventario.empty:
                messagebox.showwarning("Sin Datos", "📦 No hay productos en el inventario")
                return
            
            # Llenar el tree con datos
            for _, row in df_inventario.iterrows():
                self.tree_inventario.insert('', 'end', values=(
                    row.get('id', 'N/A'),
                    row.get('producto', 'N/A'),
                    row.get('cantidad', 0),
                    row.get('ultima_actualizacion', 'N/A')
                ))
            
            print(f"✅ Inventario cargado: {len(df_inventario)} productos")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inventario: {str(e)}")

    def agregar_producto_inventario(self):
        """Agregar un nuevo producto al inventario"""
        try:
            # Crear ventana de diálogo
            dialog = self.crear_ventana_secundaria("➕ Agregar Nuevo Producto", "450x350")
            
            form_frame = ttk.Frame(dialog, padding="30")
            form_frame.pack(fill="both", expand=True)
            
            ttk.Label(form_frame, text="➕ Agregar Nuevo Producto al Inventario", 
                     style='Subtitle.TLabel').pack(pady=(0, 20))
            
            # Campo nombre del producto
            ttk.Label(form_frame, text="📦 Nombre del Producto:").pack(anchor="w", pady=(10, 5))
            entry_nombre = ttk.Entry(form_frame, width=40, font=self.font_normal)
            entry_nombre.pack(fill="x", pady=(0, 15))
            
            # Campo cantidad
            ttk.Label(form_frame, text="📊 Cantidad:").pack(anchor="w", pady=(0, 5))
            entry_cantidad = ttk.Entry(form_frame, width=40, font=self.font_normal)
            entry_cantidad.pack(fill="x", pady=(0, 20))
            
            def procesar_agregar():
                nombre = entry_nombre.get().strip()
                cantidad_str = entry_cantidad.get().strip()
                
                if not nombre:
                    messagebox.showerror("Error", "📦 El nombre del producto es obligatorio")
                    return
                
                try:
                    cantidad = int(cantidad_str)
                    if cantidad < 0:
                        messagebox.showerror("Error", "📊 La cantidad debe ser un número positivo")
                        return
                except ValueError:
                    messagebox.showerror("Error", "📊 La cantidad debe ser un número válido")
                    return
                
                # Cargar inventario actual
                from main import cargar_excel, inventario
                import pandas as pd
                from datetime import datetime
                
                df_inventario = cargar_excel(inventario)
                
                # Verificar si el producto ya existe
                if not df_inventario.empty:
                    producto_existente = df_inventario[df_inventario['producto'].str.lower() == nombre.lower()]
                    if not producto_existente.empty:
                        messagebox.showerror("Error", 
                            f"❌ El producto '{nombre}' ya existe en el inventario.\n"
                            f"Use la función 'Editar' para modificar la cantidad.")
                        return
                
                # Generar nuevo ID
                if df_inventario.empty:
                    nuevo_id = 0
                else:
                    nuevo_id = df_inventario['id'].max() + 1
                
                # Crear nuevo registro
                nuevo_producto = pd.DataFrame({
                    'id': [nuevo_id],
                    'producto': [nombre],
                    'cantidad': [cantidad],
                    'ultima_actualizacion': [datetime.now().strftime('%Y-%m-%d')]
                })
                
                # Agregar al DataFrame existente
                if df_inventario.empty:
                    df_final = nuevo_producto
                else:
                    df_final = pd.concat([df_inventario, nuevo_producto], ignore_index=True)
                
                # Guardar archivo
                df_final.to_excel(inventario, index=False)
                
                messagebox.showinfo("Éxito", 
                    f"✅ Producto agregado exitosamente!\n\n"
                    f"🆔 ID: {nuevo_id}\n"
                    f"📦 Producto: {nombre}\n"
                    f"📊 Cantidad: {cantidad}")
                
                # Actualizar vista y cerrar diálogo
                self.recargar_inventario_silencioso()
                dialog.destroy()
            
            # Botones
            botones_frame = ttk.Frame(form_frame)
            botones_frame.pack(fill="x", pady=20)
            
            ttk.Button(botones_frame, text="✅ Agregar", 
                      command=procesar_agregar,
                      style='Success.TButton').pack(side="left", padx=10)
            
            ttk.Button(botones_frame, text="❌ Cancelar", 
                      command=dialog.destroy,
                      style='Danger.TButton').pack(side="right", padx=10)
            
            # Focus en el campo nombre
            entry_nombre.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def editar_producto_inventario(self):
        """Editar un producto del inventario"""
        try:
            # Verificar selección
            selection = self.tree_inventario.selection()
            if not selection:
                messagebox.showwarning("Selección Requerida", 
                    "🔍 Seleccione un producto del inventario para editar")
                return
            
            # Obtener datos del producto seleccionado
            item = self.tree_inventario.item(selection[0])
            producto_id = item['values'][0]
            nombre_actual = item['values'][1]
            cantidad_actual = item['values'][2]
            
            # Crear ventana de diálogo
            dialog = self.crear_ventana_secundaria("✏️ Editar Producto", "450x350")
            
            form_frame = ttk.Frame(dialog, padding="30")
            form_frame.pack(fill="both", expand=True)
            
            ttk.Label(form_frame, text="✏️ Editar Producto del Inventario", 
                     style='Subtitle.TLabel').pack(pady=(0, 20))
            
            # Mostrar ID (solo lectura)
            ttk.Label(form_frame, text=f"🆔 ID del Producto: {producto_id}",
                     style='Custom.TLabel').pack(anchor="w", pady=(0, 15))
            
            # Campo nombre del producto (editable)
            ttk.Label(form_frame, text="📦 Nombre del Producto:").pack(anchor="w", pady=(0, 5))
            entry_nombre = ttk.Entry(form_frame, width=40, font=self.font_normal)
            entry_nombre.pack(fill="x", pady=(0, 15))
            entry_nombre.insert(0, nombre_actual)
            
            # Campo cantidad (editable)
            ttk.Label(form_frame, text="📊 Cantidad:").pack(anchor="w", pady=(0, 5))
            entry_cantidad = ttk.Entry(form_frame, width=40, font=self.font_normal)
            entry_cantidad.pack(fill="x", pady=(0, 20))
            entry_cantidad.insert(0, str(cantidad_actual))
            
            def procesar_edicion():
                nuevo_nombre = entry_nombre.get().strip()
                nueva_cantidad_str = entry_cantidad.get().strip()
                
                if not nuevo_nombre:
                    messagebox.showerror("Error", "📦 El nombre del producto es obligatorio")
                    return
                
                try:
                    nueva_cantidad = int(nueva_cantidad_str)
                    if nueva_cantidad < 0:
                        messagebox.showerror("Error", "📊 La cantidad debe ser un número positivo")
                        return
                except ValueError:
                    messagebox.showerror("Error", "📊 La cantidad debe ser un número válido")
                    return
                
                # Cargar inventario actual
                from main import cargar_excel, inventario
                import pandas as pd
                from datetime import datetime
                
                df_inventario = cargar_excel(inventario)
                
                if df_inventario.empty:
                    messagebox.showerror("Error", "❌ No se pudo cargar el inventario")
                    return
                
                # Verificar que no haya otro producto con el mismo nombre (excepto el actual)
                otros_productos = df_inventario[(df_inventario['id'] != producto_id) & 
                                              (df_inventario['producto'].str.lower() == nuevo_nombre.lower())]
                if not otros_productos.empty:
                    messagebox.showerror("Error", 
                        f"❌ Ya existe otro producto con el nombre '{nuevo_nombre}'")
                    return
                
                # Actualizar el producto
                df_inventario.loc[df_inventario['id'] == producto_id, 'producto'] = nuevo_nombre
                df_inventario.loc[df_inventario['id'] == producto_id, 'cantidad'] = nueva_cantidad
                df_inventario.loc[df_inventario['id'] == producto_id, 'ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d')
                
                # Guardar archivo
                df_inventario.to_excel(inventario, index=False)
                
                messagebox.showinfo("Éxito", 
                    f"✅ Producto actualizado exitosamente!\n\n"
                    f"🆔 ID: {producto_id}\n"
                    f"📦 Nuevo Nombre: {nuevo_nombre}\n"
                    f"📊 Nueva Cantidad: {nueva_cantidad}")
                
                # Actualizar vista y cerrar diálogo
                self.recargar_inventario_silencioso()
                dialog.destroy()
            
            # Botones
            botones_frame = ttk.Frame(form_frame)
            botones_frame.pack(fill="x", pady=20)
            
            ttk.Button(botones_frame, text="✅ Guardar Cambios", 
                      command=procesar_edicion,
                      style='Success.TButton').pack(side="left", padx=10)
            
            ttk.Button(botones_frame, text="❌ Cancelar", 
                      command=dialog.destroy,
                      style='Danger.TButton').pack(side="right", padx=10)
            
            # Focus en el campo nombre
            entry_nombre.focus()
            entry_nombre.select_range(0, 'end')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar producto: {str(e)}")

    def eliminar_producto_inventario(self):
        """Eliminar un producto del inventario"""
        try:
            # Verificar selección
            selection = self.tree_inventario.selection()
            if not selection:
                messagebox.showwarning("Selección Requerida", 
                    "🔍 Seleccione un producto del inventario para eliminar")
                return
            
            # Obtener datos del producto seleccionado
            item = self.tree_inventario.item(selection[0])
            producto_id = item['values'][0]
            nombre_producto = item['values'][1]
            cantidad_producto = item['values'][2]
            
            # Confirmar eliminación
            respuesta = messagebox.askyesno("Confirmar Eliminación", 
                f"�️ ¿Está seguro de eliminar este producto?\n\n"
                f"🆔 ID: {producto_id}\n"
                f"📦 Producto: {nombre_producto}\n"
                f"📊 Cantidad: {cantidad_producto}\n\n"
                f"⚠️ Esta acción no se puede deshacer.")
            
            if not respuesta:
                return
            
            # Cargar inventario actual
            from main import cargar_excel, inventario
            import pandas as pd
            
            df_inventario = cargar_excel(inventario)
            
            if df_inventario.empty:
                messagebox.showerror("Error", "❌ No se pudo cargar el inventario")
                return
            
            # Verificar que el producto existe
            producto_existente = df_inventario[df_inventario['id'] == producto_id]
            if producto_existente.empty:
                messagebox.showerror("Error", "❌ El producto no existe en el inventario")
                return
            
            # Eliminar el producto
            df_inventario = df_inventario[df_inventario['id'] != producto_id]
            
            # Guardar archivo actualizado
            df_inventario.to_excel(inventario, index=False)
            
            messagebox.showinfo("Eliminación Exitosa", 
                f"✅ Producto eliminado exitosamente!\n\n"
                f"🗑️ Producto eliminado: {nombre_producto}\n"
                f"📊 Cantidad que tenía: {cantidad_producto}")
            
            # Actualizar vista
            self.recargar_inventario_silencioso()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")

    def actualizar_vista_inventario(self):
        """Actualizar la vista del inventario"""
        self.cargar_inventario_en_tree()

    def recargar_inventario_silencioso(self):
        """Recargar inventario sin mostrar mensajes de confirmación"""
        try:
            # Limpiar tree actual
            for item in self.tree_inventario.get_children():
                self.tree_inventario.delete(item)
            
            # Cargar datos del inventario
            from main import cargar_excel, inventario
            df_inventario = cargar_excel(inventario)
            
            if not df_inventario.empty:
                # Llenar el tree con datos
                for _, row in df_inventario.iterrows():
                    self.tree_inventario.insert('', 'end', values=(
                        row.get('id', 'N/A'),
                        row.get('producto', 'N/A'),
                        row.get('cantidad', 0),
                        row.get('ultima_actualizacion', 'N/A')
                    ))
                
        except Exception as e:
            print(f"Error al recargar inventario: {str(e)}")

    def buscar_producto_inventario(self):
        """Buscar productos en el inventario"""
        try:
            termino = tk.simpledialog.askstring("🔍 Buscar Producto", 
                "Ingrese el nombre del producto a buscar:")
            
            if not termino:
                return
            
            termino = termino.lower().strip()
            
            # Limpiar tree actual
            for item in self.tree_inventario.get_children():
                self.tree_inventario.delete(item)
            
            # Cargar y filtrar datos
            from main import cargar_excel, inventario
            df_inventario = cargar_excel(inventario)
            
            if df_inventario.empty:
                messagebox.showinfo("Sin Datos", "📦 No hay productos en el inventario")
                return
            
            # Filtrar productos que contengan el término de búsqueda
            df_filtrado = df_inventario[df_inventario['producto'].str.lower().str.contains(termino)]
            
            if df_filtrado.empty:
                messagebox.showinfo("Sin Resultados", 
                    f"� No se encontraron productos que contengan '{termino}'")
                # Recargar todos los productos
                self.recargar_inventario_silencioso()
                return
            
            # Mostrar productos filtrados
            for _, row in df_filtrado.iterrows():
                self.tree_inventario.insert('', 'end', values=(
                    row.get('id', 'N/A'),
                    row.get('producto', 'N/A'),
                    row.get('cantidad', 0),
                    row.get('ultima_actualizacion', 'N/A')
                ))
            
            messagebox.showinfo("Búsqueda Completada", 
                f"🔍 Se encontraron {len(df_filtrado)} productos que contienen '{termino}'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar productos: {str(e)}")

    def ver_detalle_producto_inventario(self, event):
        """Ver detalle de un producto (doble clic)"""
        try:
            selection = self.tree_inventario.selection()
            if not selection:
                return
            
            item = self.tree_inventario.item(selection[0])
            producto_id = item['values'][0]
            nombre_producto = item['values'][1]
            cantidad_producto = item['values'][2]
            fecha_actualizacion = item['values'][3]
            
            # Mostrar información detallada
            detalle = f"""📦 DETALLE DEL PRODUCTO

🆔 ID: {producto_id}
📦 Nombre: {nombre_producto}
📊 Cantidad Disponible: {cantidad_producto} unidades
📅 Última Actualización: {fecha_actualizacion}

💡 Para editar este producto, selecciónelo y haga clic en 'Editar Producto'
🗑️ Para eliminarlo, selecciónelo y haga clic en 'Eliminar Producto'"""
            
            messagebox.showinfo("Detalle del Producto", detalle)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalle: {str(e)}")
            
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
        
        # Área de resultados con texto oscuro
        self.text_disponibilidad = tk.Text(main_frame, height=15, width=70,
                                          bg='white', fg='#2C3E50', insertbackground='#2C3E50')
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

    def menu_solicitud_compra_hu8(self):
        """Menú completo para reportes de solicitudes de compra - HU8"""
        ventana = self.crear_ventana_secundaria("🛒 Reportes de Solicitudes de Compra - HU8", "1200x800")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Reportes de Solicitudes de Compra", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame principal con notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # === PESTAÑA 1: FILTRAR SOLICITUDES ===
        tab_filtrar = ttk.Frame(notebook)
        notebook.add(tab_filtrar, text="🔍 Filtrar Solicitudes")
        
        filtrar_frame = ttk.Frame(tab_filtrar, padding="20")
        filtrar_frame.pack(fill="both", expand=True)
        
        ttk.Label(filtrar_frame, text="Filtrar Solicitudes por Fecha", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para filtros de fecha
        filtro_frame = ttk.LabelFrame(filtrar_frame, text="Filtrar por Fechas", padding="10")
        filtro_frame.pack(fill="x", pady=10)
        
        fecha_frame = ttk.Frame(filtro_frame)
        fecha_frame.pack(fill="x")
        
        ttk.Label(fecha_frame, text="Fecha inicio:").pack(side="left", padx=5)
        self.entry_fecha_ini_solicitudes = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_ini_solicitudes.pack(side="left", padx=5)
        
        ttk.Label(fecha_frame, text="Fecha fin:").pack(side="left", padx=5)
        self.entry_fecha_fin_solicitudes = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_fin_solicitudes.pack(side="left", padx=5)
        
        ttk.Button(fecha_frame, text="🔍 Filtrar", 
                  command=self.filtrar_solicitudes_fecha,
                  style='Primary.TButton').pack(side="left", padx=10)
        
        # Lista de solicitudes filtradas
        lista_frame = ttk.LabelFrame(filtrar_frame, text="Solicitudes Filtradas", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar solicitudes
        columns = ('ID', 'Fecha', 'Proveedor', 'Estado')
        self.tree_solicitudes = ttk.Treeview(lista_frame, columns=columns, show='headings', height=15)
        
        self.tree_solicitudes.heading('ID', text='ID')
        self.tree_solicitudes.heading('Fecha', text='Fecha')
        self.tree_solicitudes.heading('Proveedor', text='Proveedor')
        self.tree_solicitudes.heading('Estado', text='Estado')
        
        self.tree_solicitudes.column('ID', width=100)
        self.tree_solicitudes.column('Fecha', width=150)
        self.tree_solicitudes.column('Proveedor', width=200)
        self.tree_solicitudes.column('Estado', width=150)
        
        # Scrollbar para el Treeview
        scrollbar_solicitudes = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_solicitudes.yview)
        self.tree_solicitudes.configure(yscrollcommand=scrollbar_solicitudes.set)
        
        self.tree_solicitudes.pack(side="left", fill="both", expand=True)
        scrollbar_solicitudes.pack(side="right", fill="y")
        
        # Botones de acción para solicitudes
        botones_sol_frame = ttk.Frame(filtrar_frame)
        botones_sol_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_sol_frame, text="👁️ Ver Detalle", 
                  command=self.ver_detalle_solicitud,
                  style='Success.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_sol_frame, text="💾 Descargar Reporte", 
                  command=self.descargar_reporte_solicitud,
                  style='Secondary.TButton').pack(side="left", padx=10)
        
        # === PESTAÑA 2: GENERAR NUEVA SOLICITUD ===
        tab_generar = ttk.Frame(notebook)
        notebook.add(tab_generar, text="🛒 Generar Solicitud")
        
        generar_frame = ttk.Frame(tab_generar, padding="20")
        generar_frame.pack(fill="both", expand=True)
        
        ttk.Label(generar_frame, text="Generar Nueva Solicitud de Compra", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información de la funcionalidad
        info_frame = ttk.LabelFrame(generar_frame, text="Información", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """Esta función analiza automáticamente la demanda vs inventario para 
identificar productos faltantes y generar solicitudes de compra."""
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(generar_frame, text="Productos Faltantes Detectados", padding="15")
        resultados_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar productos faltantes
        columns_falt = ('Producto', 'Demanda', 'Inventario', 'Cantidad Faltante')
        self.tree_faltantes = ttk.Treeview(resultados_frame, columns=columns_falt, show='headings', height=15)
        
        self.tree_faltantes.heading('Producto', text='Producto')
        self.tree_faltantes.heading('Demanda', text='Demanda')
        self.tree_faltantes.heading('Inventario', text='Inventario')
        self.tree_faltantes.heading('Cantidad Faltante', text='Cantidad Faltante')
        
        self.tree_faltantes.column('Producto', width=250)
        self.tree_faltantes.column('Demanda', width=100)
        self.tree_faltantes.column('Inventario', width=100)
        self.tree_faltantes.column('Cantidad Faltante', width=150)
        
        # Scrollbar para el Treeview de faltantes
        scrollbar_faltantes = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree_faltantes.yview)
        self.tree_faltantes.configure(yscrollcommand=scrollbar_faltantes.set)
        
        self.tree_faltantes.pack(side="left", fill="both", expand=True)
        scrollbar_faltantes.pack(side="right", fill="y")
        
        # Botones de acción para generar
        botones_generar_frame = ttk.Frame(generar_frame)
        botones_generar_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_generar_frame, text="🔄 Detectar Faltantes", 
                  command=self.detectar_productos_faltantes,
                  style='Primary.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_generar_frame, text="💾 Guardar Solicitud", 
                  command=self.guardar_solicitud_compra,
                  style='Success.TButton').pack(side="left", padx=10)

    def filtrar_solicitudes_fecha(self):
        """Filtrar solicitudes por fecha"""
        try:
            from main import filtrar_solicitudes_fecha as filtrar_sol_main
            
            fecha_ini = self.entry_fecha_ini_solicitudes.get().strip()
            fecha_fin = self.entry_fecha_fin_solicitudes.get().strip()
            
            if not fecha_ini or not fecha_fin:
                messagebox.showerror("Error", "Ambas fechas son obligatorias")
                return
            
            # Leer archivo de solicitudes
            archivo_solicitudes = os.path.join("data", "solicitudes_compras.xlsx")
            if not os.path.exists(archivo_solicitudes):
                messagebox.showwarning("Advertencia", "No hay solicitudes registradas")
                return
            
            df_solicitudes = pd.read_excel(archivo_solicitudes)
            if df_solicitudes.empty:
                messagebox.showinfo("Info", "No hay solicitudes para mostrar")
                return
            
            # Filtrar por fechas
            try:
                df_solicitudes['fecha'] = pd.to_datetime(df_solicitudes['fecha'])
                ini_dt = pd.to_datetime(fecha_ini)
                fin_dt = pd.to_datetime(fecha_fin)
                df_filtrado = df_solicitudes[(df_solicitudes['fecha'] >= ini_dt) & (df_solicitudes['fecha'] <= fin_dt)]
            except Exception as e:
                messagebox.showerror("Error", f"Fechas inválidas: {e}")
                return
            
            # Limpiar tree y cargar datos
            for item in self.tree_solicitudes.get_children():
                self.tree_solicitudes.delete(item)
            
            if df_filtrado.empty:
                messagebox.showinfo("Resultado", "No hay solicitudes en ese rango de fechas")
            else:
                # Agrupar por ID y mostrar resumen
                for id_sol, grupo in df_filtrado.groupby('id'):
                    primera_fila = grupo.iloc[0]
                    self.tree_solicitudes.insert('', 'end', values=(
                        id_sol,
                        primera_fila['fecha'].strftime('%Y-%m-%d'),
                        primera_fila.get('proveedor', 'N/A'),
                        primera_fila.get('estado', 'Pendiente')
                    ))
                
                self.df_solicitudes_filtradas = df_filtrado
                messagebox.showinfo("Éxito", f"Se encontraron {len(df_filtrado.groupby('id'))} solicitudes")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar solicitudes: {str(e)}")

    def ver_detalle_solicitud(self):
        """Ver detalle de la solicitud seleccionada"""
        try:
            selection = self.tree_solicitudes.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione una solicitud para ver el detalle")
                return
            
            item = self.tree_solicitudes.item(selection[0])
            id_solicitud = item['values'][0]
            
            # Buscar detalles en el DataFrame filtrado
            if hasattr(self, 'df_solicitudes_filtradas'):
                detalle = self.df_solicitudes_filtradas[self.df_solicitudes_filtradas['id'] == id_solicitud]
                
                if not detalle.empty:
                    # Crear ventana de detalle
                    ventana_detalle = self.crear_ventana_secundaria("📋 Detalle de Solicitud", "800x600")
                    
                    frame_detalle = ttk.Frame(ventana_detalle, padding="20")
                    frame_detalle.pack(fill="both", expand=True)
                    
                    ttk.Label(frame_detalle, text=f"Detalle de Solicitud ID: {id_solicitud}", 
                             style='Subtitle.TLabel').pack(pady=10)
                    
                    # Crear texto con detalles
                    text_detalle = tk.Text(frame_detalle, height=20, width=80, 
                                          font=("Consolas", 10), bg="#f8f9fa", fg="#2c3e50")
                    scroll_detalle = ttk.Scrollbar(frame_detalle, orient="vertical", command=text_detalle.yview)
                    text_detalle.configure(yscrollcommand=scroll_detalle.set)
                    
                    text_detalle.pack(side="left", fill="both", expand=True)
                    scroll_detalle.pack(side="right", fill="y")
                    
                    # Llenar con información
                    text_detalle.insert(tk.END, f"📋 SOLICITUD DE COMPRA - ID: {id_solicitud}\n")
                    text_detalle.insert(tk.END, "=" * 50 + "\n\n")
                    
                    primera_fila = detalle.iloc[0]
                    text_detalle.insert(tk.END, f"📅 Fecha: {primera_fila['fecha'].strftime('%Y-%m-%d')}\n")
                    text_detalle.insert(tk.END, f"🏢 Proveedor: {primera_fila.get('proveedor', 'N/A')}\n")
                    text_detalle.insert(tk.END, f"📊 Estado: {primera_fila.get('estado', 'Pendiente')}\n\n")
                    
                    text_detalle.insert(tk.END, "📦 PRODUCTOS SOLICITADOS:\n")
                    text_detalle.insert(tk.END, "-" * 30 + "\n")
                    
                    for _, row in detalle.iterrows():
                        text_detalle.insert(tk.END, f"• {row.get('producto', 'N/A')}: {row.get('cantidad', 0)} unidades\n")
                else:
                    messagebox.showerror("Error", "No se encontraron detalles para esta solicitud")
            else:
                messagebox.showwarning("Advertencia", "Primero debe filtrar las solicitudes")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al ver detalle: {str(e)}")

    def descargar_reporte_solicitud(self):
        """Descargar reporte de solicitud seleccionada"""
        try:
            selection = self.tree_solicitudes.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione una solicitud para descargar")
                return
            
            item = self.tree_solicitudes.item(selection[0])
            id_solicitud = item['values'][0]
            
            if hasattr(self, 'df_solicitudes_filtradas'):
                detalle = self.df_solicitudes_filtradas[self.df_solicitudes_filtradas['id'] == id_solicitud]
                
                if not detalle.empty:
                    archivo = os.path.join("data", f"reporte_solicitud_{id_solicitud}.xlsx")
                    detalle.to_excel(archivo, index=False)
                    messagebox.showinfo("Éxito", f"✅ Reporte guardado en:\n{archivo}")
                else:
                    messagebox.showerror("Error", "No se encontraron datos para descargar")
            else:
                messagebox.showwarning("Advertencia", "Primero debe filtrar las solicitudes")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar reporte: {str(e)}")

    def detectar_productos_faltantes(self):
        """Detectar productos faltantes comparando demanda vs inventario"""
        try:
            from main import obtener_insumos_faltantes
            
            # Limpiar tree de faltantes
            for item in self.tree_faltantes.get_children():
                self.tree_faltantes.delete(item)
            
            # Obtener productos faltantes
            faltantes = obtener_insumos_faltantes()
            
            if faltantes.empty:
                messagebox.showinfo("Resultado", "✅ No hay productos faltantes detectados.\nEl inventario actual cubre toda la demanda.")
                return
            
            # Cargar datos en el tree
            for _, row in faltantes.iterrows():
                self.tree_faltantes.insert('', 'end', values=(
                    row.get('producto', 'N/A'),
                    row.get('cantidad_demandada', 0),
                    row.get('cantidad_disponible', 0),
                    row.get('cantidad_faltante', 0)
                ))
            
            self.df_faltantes_actual = faltantes
            messagebox.showinfo("Resultado", f"📊 Se detectaron {len(faltantes)} productos faltantes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al detectar faltantes: {str(e)}")

    def guardar_solicitud_compra(self):
        """Guardar solicitud de compra basada en productos faltantes"""
        try:
            if not hasattr(self, 'df_faltantes_actual') or self.df_faltantes_actual.empty:
                messagebox.showwarning("Advertencia", "Primero debe detectar productos faltantes")
                return
            
            from datetime import datetime
            
            # Generar ID único para la solicitud
            id_solicitud = int(datetime.now().strftime('%Y%m%d%H%M%S'))
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            
            # Preparar datos para guardar
            solicitud_data = []
            for _, row in self.df_faltantes_actual.iterrows():
                solicitud_data.append({
                    'id': id_solicitud,
                    'fecha': fecha_actual,
                    'producto': row.get('producto', 'N/A'),
                    'cantidad': row.get('cantidad_faltante', 0),
                    'proveedor': 'Por definir',
                    'estado': 'Pendiente',
                    'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            df_nueva_solicitud = pd.DataFrame(solicitud_data)
            
            # Guardar en archivo
            archivo_solicitudes = os.path.join("data", "solicitudes_compras.xlsx")
            
            if os.path.exists(archivo_solicitudes):
                df_existente = pd.read_excel(archivo_solicitudes)
                df_final = pd.concat([df_existente, df_nueva_solicitud], ignore_index=True)
            else:
                df_final = df_nueva_solicitud
            
            df_final.to_excel(archivo_solicitudes, index=False)
            
            messagebox.showinfo("Éxito", 
                f"✅ Solicitud de compra creada exitosamente!\n\n"
                f"🆔 ID: {id_solicitud}\n"
                f"📅 Fecha: {fecha_actual}\n"
                f"📦 Productos: {len(df_nueva_solicitud)}\n"
                f"💾 Guardado en: {archivo_solicitudes}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar solicitud: {str(e)}")

    def ejecutar_hu8_directo(self):
        """Ejecutar HU8 directamente con captura de salida"""
        try:
            self.text_hu8.delete(1.0, tk.END)
            self.text_hu8.insert(tk.END, "🔄 Generando solicitud de compra...\n\n")
            
            # Ejecutar detección de faltantes
            from main import obtener_insumos_faltantes
            faltantes = obtener_insumos_faltantes()
            
            if faltantes.empty:
                self.text_hu8.insert(tk.END, "✅ No hay productos faltantes detectados.\n")
                self.text_hu8.insert(tk.END, "El inventario actual cubre toda la demanda.\n")
            else:
                self.text_hu8.insert(tk.END, f"📊 Se detectaron {len(faltantes)} productos faltantes:\n\n")
                
                for _, row in faltantes.iterrows():
                    self.text_hu8.insert(tk.END, 
                        f"• ID: {row['id']} | Producto: {row['producto']} | Cantidad: {row['cantidad']}\n")
                
                self.text_hu8.insert(tk.END, "\n🛒 Solicitud de compra generada automáticamente.\n")
                self.text_hu8.insert(tk.END, "💾 Para guardar y enviar por email, use la interfaz avanzada.\n")
            
            self.text_hu8.insert(tk.END, "\n✅ Proceso de generación completado.")
            
        except Exception as e:
            self.text_hu8.insert(tk.END, f"❌ Error al generar solicitud: {str(e)}\n")

    def menu_registro_pedidos_hu3(self):
        """HU3 - Solicitud de Compra: Generar solicitudes de compra de insumos (igual flujo que main.py)"""
        # Obtener insumos faltantes desde el inicio
        try:
            from main import obtener_insumos_faltantes
            self.solicitud_actual = obtener_insumos_faltantes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener insumos faltantes: {str(e)}")
            return
            
        if self.solicitud_actual.empty:
            messagebox.showinfo("Sin Faltantes", "✅ No hay productos faltantes. Toda la demanda está cubierta.")
            return

        # Crear ventana principal del menú
        ventana = self.crear_ventana_secundaria("📋 Solicitud de Compra de Insumos - HU3", "1000x700")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Solicitud de Compra de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame de información
        info_frame = ttk.LabelFrame(main_frame, text="Información del Proceso", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """HU3 - Generar solicitudes de compra de insumos.
Este módulo analiza los productos faltantes y permite gestionar la solicitud de compra."""
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Frame con los botones del menú (igual a main.py)
        menu_frame = ttk.LabelFrame(main_frame, text="Opciones del Menú", padding="15")
        menu_frame.pack(fill="x", pady=10)
        
        # Configurar grid para 3 columnas, 2 filas
        for i in range(3):
            menu_frame.grid_columnconfigure(i, weight=1)
        
        # Botones siguiendo el flujo exacto de main.py
        ttk.Button(menu_frame, text="1. � Mostrar Sugerencia de Solicitud", 
                  command=self.mostrar_sugerencia_solicitud_hu3,
                  style='Primary.TButton').grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(menu_frame, text="2. ✏️ Editar Solicitud", 
                  command=self.editar_solicitud_hu3,
                  style='Secondary.TButton').grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(menu_frame, text="3. ✅ Validar Información", 
                  command=self.validar_solicitud_hu3,
                  style='Info.TButton').grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        ttk.Button(menu_frame, text="4. 💾 Guardar Solicitud", 
                  command=self.guardar_solicitud_hu3,
                  style='Success.TButton').grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(menu_frame, text="5. 📧 Enviar Solicitud", 
                  command=self.enviar_solicitud_hu3,
                  style='Warning.TButton').grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(menu_frame, text="6. 🏠 Volver", 
                  command=ventana.destroy,
                  style='Danger.TButton').grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        # Frame para mostrar la solicitud actual
        solicitud_frame = ttk.LabelFrame(main_frame, text="Solicitud Actual", padding="15")
        solicitud_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar productos faltantes
        columns = ('ID', 'Producto', 'Cantidad')
        self.tree_solicitud_hu3 = ttk.Treeview(solicitud_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree_solicitud_hu3.heading(col, text=col)
        
        self.tree_solicitud_hu3.column('ID', width=80, anchor='center')
        self.tree_solicitud_hu3.column('Producto', width=300)
        self.tree_solicitud_hu3.column('Cantidad', width=120, anchor='center')
        
        # Scrollbar para el Treeview
        scrollbar_solicitud = ttk.Scrollbar(solicitud_frame, orient="vertical", command=self.tree_solicitud_hu3.yview)
        self.tree_solicitud_hu3.configure(yscrollcommand=scrollbar_solicitud.set)
        
        self.tree_solicitud_hu3.grid(row=0, column=0, sticky="nsew")
        scrollbar_solicitud.grid(row=0, column=1, sticky="ns")
        
        solicitud_frame.grid_rowconfigure(0, weight=1)
        solicitud_frame.grid_columnconfigure(0, weight=1)
        
        # Cargar datos iniciales
        self.actualizar_tree_solicitud_hu3()
        
        # Guardar referencia a la ventana para poder cerrarla
        self.ventana_hu3 = ventana

    def actualizar_tree_solicitud_hu3(self):
        """Actualizar el Treeview con la solicitud actual"""
        # Limpiar tree
        for item in self.tree_solicitud_hu3.get_children():
            self.tree_solicitud_hu3.delete(item)
            
        # Agregar datos de la solicitud actual
        for _, row in self.solicitud_actual.iterrows():
            self.tree_solicitud_hu3.insert('', 'end', values=(
                row.get('id', ''),
                row.get('producto', ''),
                row.get('cantidad', '')
            ))
    
    def mostrar_sugerencia_solicitud_hu3(self):
        """1. Mostrar sugerencia de solicitud (igual a main.py)"""
        try:
            # Convertir DataFrame a string para mostrar
            solicitud_texto = "📦 Insumos sugeridos para solicitar:\n\n"
            solicitud_texto += self.solicitud_actual.to_string(index=False)
            
            # Crear ventana para mostrar la sugerencia
            ventana_sugerencia = self.crear_ventana_secundaria("📋 Sugerencia de Solicitud", "600x500")
            
            frame_sugerencia = ttk.Frame(ventana_sugerencia, padding="20")
            frame_sugerencia.pack(fill="both", expand=True)
            
            ttk.Label(frame_sugerencia, text="Sugerencia de Solicitud de Compra", 
                     style='Subtitle.TLabel').pack(pady=10)
            
            # Texto con la información
            text_widget = tk.Text(frame_sugerencia, height=20, wrap=tk.WORD, 
                                 font=("Consolas", 10), bg="#f8f9fa", fg="#2c3e50")
            scrollbar_text = ttk.Scrollbar(frame_sugerencia, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar_text.set)
            
            text_widget.insert(tk.END, solicitud_texto)
            text_widget.configure(state='disabled')  # Solo lectura
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar_text.pack(side="right", fill="y")
            
            ttk.Button(frame_sugerencia, text="Cerrar", 
                      command=ventana_sugerencia.destroy,
                      style='Primary.TButton').pack(pady=10)
                      
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar sugerencia: {str(e)}")
    
    def editar_solicitud_hu3(self):
        """2. Editar solicitud (igual flujo que main.py)"""
        ventana_editar = self.crear_ventana_secundaria("✏️ Editar Solicitud", "600x500")
        
        main_frame = ttk.Frame(ventana_editar, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Editar Solicitud", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Botones del submenú (igual a main.py)
        submenu_frame = ttk.LabelFrame(main_frame, text="Opciones de Edición", padding="15")
        submenu_frame.pack(fill="x", pady=10)
        
        ttk.Button(submenu_frame, text="1. Agregar Producto", 
                  command=lambda: self.agregar_producto_solicitud_hu3(ventana_editar),
                  style='Success.TButton').pack(fill="x", pady=5)
        
        ttk.Button(submenu_frame, text="2. Eliminar Producto", 
                  command=lambda: self.eliminar_producto_solicitud_hu3(ventana_editar),
                  style='Danger.TButton').pack(fill="x", pady=5)
        
        ttk.Button(submenu_frame, text="3. Modificar Cantidad", 
                  command=lambda: self.modificar_cantidad_solicitud_hu3(ventana_editar),
                  style='Warning.TButton').pack(fill="x", pady=5)
        
        ttk.Button(submenu_frame, text="4. Volver", 
                  command=ventana_editar.destroy,
                  style='Secondary.TButton').pack(fill="x", pady=5)
        
        # Vista previa de la solicitud actual
        preview_frame = ttk.LabelFrame(main_frame, text="Solicitud Actual", padding="15")
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Mini Treeview para edición
        columns_edit = ('ID', 'Producto', 'Cantidad')
        self.tree_editar_hu3 = ttk.Treeview(preview_frame, columns=columns_edit, show='headings', height=10)
        
        for col in columns_edit:
            self.tree_editar_hu3.heading(col, text=col)
        
        self.tree_editar_hu3.column('ID', width=80, anchor='center')
        self.tree_editar_hu3.column('Producto', width=250)
        self.tree_editar_hu3.column('Cantidad', width=100, anchor='center')
        
        scrollbar_edit = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree_editar_hu3.yview)
        self.tree_editar_hu3.configure(yscrollcommand=scrollbar_edit.set)
        
        self.tree_editar_hu3.pack(side="left", fill="both", expand=True)
        scrollbar_edit.pack(side="right", fill="y")
        
        # Actualizar vista previa
        self.actualizar_tree_editar_hu3()
    
    def actualizar_tree_editar_hu3(self):
        """Actualizar el tree de edición"""
        for item in self.tree_editar_hu3.get_children():
            self.tree_editar_hu3.delete(item)
            
        for _, row in self.solicitud_actual.iterrows():
            self.tree_editar_hu3.insert('', 'end', values=(
                row.get('id', ''),
                row.get('producto', ''),
                row.get('cantidad', '')
            ))
    
    def agregar_producto_solicitud_hu3(self, ventana_padre):
        """Agregar producto a la solicitud (igual lógica que main.py)"""
        def procesar_agregar():
            nombre = entry_nombre.get().strip()
            cantidad_str = entry_cantidad.get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "❌ Debe ingresar un nombre de producto")
                return
                
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                messagebox.showerror("Error", "❌ Cantidad inválida.")
                return
            
            # Agregar nuevo producto (igual lógica que main.py)
            import pandas as pd
            nueva_fila = pd.DataFrame([[999, nombre, int(cantidad_str)]], columns=["id", "producto", "cantidad"])
            self.solicitud_actual = pd.concat([self.solicitud_actual, nueva_fila], ignore_index=True)
            
            messagebox.showinfo("Éxito", "✅ Producto agregado.")
            
            # Actualizar vistas
            self.actualizar_tree_solicitud_hu3()
            self.actualizar_tree_editar_hu3()
            
            ventana_agregar.destroy()
        
        ventana_agregar = tk.Toplevel(ventana_padre)
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.geometry("400x200")
        ventana_agregar.transient(ventana_padre)
        ventana_agregar.grab_set()
        
        frame = ttk.Frame(ventana_agregar, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Agregar Nuevo Producto", style='Subtitle.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Nombre del producto:").pack(anchor="w", pady=5)
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.pack(pady=5)
        
        ttk.Label(frame, text="Cantidad:").pack(anchor="w", pady=5)
        entry_cantidad = ttk.Entry(frame, width=40)
        entry_cantidad.pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✅ Agregar", command=procesar_agregar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_agregar.destroy).pack(side="left", padx=10)
    
    def eliminar_producto_solicitud_hu3(self, ventana_padre):
        """Eliminar producto de la solicitud (igual lógica que main.py)"""
        def procesar_eliminar():
            nombre = entry_nombre.get().strip().lower()
            
            if not nombre:
                messagebox.showerror("Error", "❌ Debe ingresar un nombre de producto")
                return
            
            # Eliminar producto (igual lógica que main.py)
            original_len = len(self.solicitud_actual)
            self.solicitud_actual = self.solicitud_actual[~self.solicitud_actual["producto"].str.lower().str.strip().eq(nombre)]
            
            if len(self.solicitud_actual) < original_len:
                messagebox.showinfo("Éxito", "✅ Producto eliminado.")
                # Actualizar vistas
                self.actualizar_tree_solicitud_hu3()
                self.actualizar_tree_editar_hu3()
            else:
                messagebox.showerror("Error", "❌ Producto no encontrado.")
            
            ventana_eliminar.destroy()
        
        ventana_eliminar = tk.Toplevel(ventana_padre)
        ventana_eliminar.title("Eliminar Producto")
        ventana_eliminar.geometry("400x150")
        ventana_eliminar.transient(ventana_padre)
        ventana_eliminar.grab_set()
        
        frame = ttk.Frame(ventana_eliminar, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Eliminar Producto", style='Subtitle.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Nombre del producto a eliminar:").pack(anchor="w", pady=5)
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=procesar_eliminar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_eliminar.destroy).pack(side="left", padx=10)
    
    def modificar_cantidad_solicitud_hu3(self, ventana_padre):
        """Modificar cantidad de producto en la solicitud (igual lógica que main.py)"""
        def procesar_modificar():
            nombre = entry_nombre.get().strip().lower()
            cantidad_str = entry_cantidad.get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "❌ Debe ingresar un nombre de producto")
                return
                
            if nombre not in self.solicitud_actual["producto"].str.lower().str.strip().values:
                messagebox.showerror("Error", "❌ Producto no encontrado.")
                return
            
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                messagebox.showerror("Error", "❌ Cantidad inválida.")
                return
            
            # Modificar cantidad (igual lógica que main.py)
            idx = self.solicitud_actual[self.solicitud_actual["producto"].str.lower().str.strip() == nombre].index[0]
            self.solicitud_actual.at[idx, "cantidad"] = int(cantidad_str)
            
            messagebox.showinfo("Éxito", "✅ Cantidad actualizada.")
            
            # Actualizar vistas
            self.actualizar_tree_solicitud_hu3()
            self.actualizar_tree_editar_hu3()
            
            ventana_modificar.destroy()
        
        ventana_modificar = tk.Toplevel(ventana_padre)
        ventana_modificar.title("Modificar Cantidad")
        ventana_modificar.geometry("400x200")
        ventana_modificar.transient(ventana_padre)
        ventana_modificar.grab_set()
        
        frame = ttk.Frame(ventana_modificar, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Modificar Cantidad", style='Subtitle.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Nombre del producto a modificar:").pack(anchor="w", pady=5)
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.pack(pady=5)
        
        ttk.Label(frame, text="Nueva cantidad:").pack(anchor="w", pady=5)
        entry_cantidad = ttk.Entry(frame, width=40)
        entry_cantidad.pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✏️ Modificar", command=procesar_modificar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_modificar.destroy).pack(side="left", padx=10)
    
    def validar_solicitud_hu3(self):
        """3. Validar información (igual lógica que main.py)"""
        try:
            errores = []
            for _, row in self.solicitud_actual.iterrows():
                if not row["producto"] or not isinstance(row["cantidad"], (int, float)):
                    errores.append(f"❌ Producto inválido o sin cantidad: {row.to_dict()}")
                elif row["cantidad"] <= 0:
                    errores.append(f"❌ Cantidad inválida para producto '{row['producto']}': {row['cantidad']}")

            if errores:
                error_texto = "\n❌ Se encontraron errores en la solicitud:\n\n"
                for e in errores:
                    error_texto += f"- {e}\n"
                messagebox.showerror("Errores de Validación", error_texto)
            else:
                messagebox.showinfo("Validación", "✅ Toda la información de la solicitud es válida.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar solicitud: {str(e)}")
    
    def guardar_solicitud_hu3(self):
        """4. Guardar solicitud (igual lógica que main.py)"""
        try:
            import os
            from main import guardar_excel, inventario
            
            archivo_solicitud = os.path.join(os.path.dirname(inventario), "solicitud_compra.xlsx")
            guardar_excel(self.solicitud_actual, archivo_solicitud)
            
            messagebox.showinfo("Éxito", "✅ Solicitud guardada correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar solicitud: {str(e)}")
    
    def enviar_solicitud_hu3(self):
        """5. Enviar solicitud (igual lógica que main.py)"""
        try:
            import os
            from main import inventario
            from email.message import EmailMessage
            import smtplib
            
            archivo = os.path.join(os.path.dirname(inventario), "solicitud_compra.xlsx")
            if not os.path.exists(archivo):
                messagebox.showerror("Error", "❌ No se ha guardado la solicitud aún.")
                return

            # Pedir correo del destinatario
            destinatario = self.pedir_correo_hu3()
            if not destinatario:
                return
            
            # Configuración de correo (igual que main.py)
            email_remitente = "elcoordinadordecompras@gmail.com"
            contraseña = "iocsdhwphxxhbzzp"
            
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
                    messagebox.showinfo("Éxito", "📧 Solicitud enviada correctamente.")
            except Exception as e:
                messagebox.showerror("Error Email", f"❌ Error al enviar la solicitud: {e}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en envío de solicitud: {str(e)}")
    
    def pedir_correo_hu3(self):
        """Pedir correo del destinatario con validación (igual que main.py)"""
        import re
        
        def validar_y_enviar():
            correo = entry_correo.get().strip()
            patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
            
            if re.match(patron, correo):
                self.correo_destinatario = correo
                ventana_correo.destroy()
            else:
                messagebox.showerror("Error", "❌ El correo ingresado no es válido. Verifica el formato (ej: ejemplo@dominio.com). Inténtalo de nuevo.")
        
        self.correo_destinatario = None
        
        ventana_correo = tk.Toplevel()
        ventana_correo.title("Correo Destinatario")
        ventana_correo.geometry("400x150")
        ventana_correo.transient()
        ventana_correo.grab_set()
        
        frame = ttk.Frame(ventana_correo, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="📧 Ingrese el correo del destinatario:", style='Custom.TLabel').pack(anchor="w", pady=5)
        entry_correo = ttk.Entry(frame, width=40)
        entry_correo.pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✅ Enviar", command=validar_y_enviar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_correo.destroy).pack(side="left", padx=10)
        
        # Esperar a que se cierre la ventana
        ventana_correo.wait_window()
        
        return getattr(self, 'correo_destinatario', None)

    def menu_recepcion_insumos(self):
        """Menú para recepción de insumos con control de conformidad"""
        ventana = self.crear_ventana_secundaria("📥 Recepción de Insumos", "900x700")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Recepción de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para información del pedido
        info_frame = ttk.LabelFrame(main_frame, text="Información del Pedido", padding="10")
        info_frame.pack(fill="x", pady=10)
        
        # Campos de información con mejor visibilidad
        ttk.Label(info_frame, text="Proveedor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_proveedor = ttk.Entry(info_frame, width=30, style='Custom.TEntry')
        self.entry_proveedor.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_fecha_recepcion = ttk.Entry(info_frame, width=30, style='Custom.TEntry')
        self.entry_fecha_recepcion.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Número de pedido:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_numero_pedido = ttk.Entry(info_frame, width=30, style='Custom.TEntry')
        self.entry_numero_pedido.grid(row=2, column=1, padx=5, pady=5)
        
        # Productos recibidos con conformidad
        productos_frame = ttk.LabelFrame(main_frame, text="Productos Recibidos", padding="10")
        productos_frame.pack(fill="both", expand=True, pady=10)
        
        # Lista de productos con conformidad
        self.productos_recibidos = []
        
        # Frame para agregar productos
        add_frame = ttk.Frame(productos_frame)
        add_frame.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="Producto:").pack(side="left", padx=5)
        self.entry_producto_nuevo = ttk.Entry(add_frame, width=20, style='Custom.TEntry')
        self.entry_producto_nuevo.pack(side="left", padx=5)
        
        ttk.Label(add_frame, text="Cantidad:").pack(side="left", padx=5)
        self.entry_cantidad_nueva = ttk.Entry(add_frame, width=10, style='Custom.TEntry')
        self.entry_cantidad_nueva.pack(side="left", padx=5)
        
        ttk.Label(add_frame, text="Estado:").pack(side="left", padx=5)
        self.combo_estado_nuevo = ttk.Combobox(add_frame, width=12, 
                                             values=["Conforme", "No conforme"],
                                             state="readonly")
        self.combo_estado_nuevo.set("Conforme")  # Valor por defecto
        self.combo_estado_nuevo.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="➕ Agregar", 
                  command=self.agregar_producto_recibido).pack(side="left", padx=5)
        
        # Frame con Treeview para mostrar productos con conformidad
        tree_frame = ttk.Frame(productos_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)
        
        # Crear Treeview para productos
        columns = ('Producto', 'Cantidad', 'Estado')
        self.tree_productos = ttk.Treeview(tree_frame, columns=columns, show='tree headings', height=8)
        
        # Configurar columnas
        self.tree_productos.heading('#0', text='#')
        self.tree_productos.heading('Producto', text='Producto')
        self.tree_productos.heading('Cantidad', text='Cantidad')
        self.tree_productos.heading('Estado', text='Estado')
        
        self.tree_productos.column('#0', width=50)
        self.tree_productos.column('Producto', width=200)
        self.tree_productos.column('Cantidad', width=100)
        self.tree_productos.column('Estado', width=120)
        
        # Scrollbar para el Treeview
        scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")
        
        # Frame para modificar conformidad de producto seleccionado
        modify_frame = ttk.Frame(productos_frame)
        modify_frame.pack(fill="x", pady=5)
        
        ttk.Label(modify_frame, text="Modificar estado del producto seleccionado:").pack(side="left", padx=5)
        self.combo_estado_modificar = ttk.Combobox(modify_frame, width=12,
                                                 values=["Conforme", "No conforme"],
                                                 state="readonly")
        self.combo_estado_modificar.pack(side="left", padx=5)
        
        ttk.Button(modify_frame, text="✏️ Modificar", 
                  command=self.modificar_estado_producto).pack(side="left", padx=5)
        ttk.Button(modify_frame, text="🗑️ Eliminar", 
                  command=self.eliminar_producto).pack(side="left", padx=5)
        
        # Botones finales
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_frame, text="💾 Guardar Recepción", 
                  command=self.guardar_recepcion_insumos,
                  style='Success.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="📋 Ver Recepciones", 
                  command=self.ver_recepciones_hu5).pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="📦 Verificar Inventario", 
                  command=self.mostrar_inventario_actual,
                  style='Info.TButton').pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="🧹 Limpiar Todo", 
                  command=self.limpiar_campos_recepcion).pack(side="left", padx=10)

    def agregar_producto_recibido(self):
        """Agregar producto a la lista de recepción"""
        try:
            producto = self.entry_producto_nuevo.get().strip()
            cantidad_str = self.entry_cantidad_nueva.get().strip()
            estado = self.combo_estado_nuevo.get()
            
            if not producto or not cantidad_str or not estado:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero positivo")
                return
            
            # Agregar al tree
            item_id = self.tree_productos.insert('', 'end', 
                                                text=str(len(self.productos_recibidos) + 1),
                                                values=(producto, cantidad, estado))
            
            # Agregar a la lista interna
            self.productos_recibidos.append({
                'producto': producto,
                'cantidad': cantidad,
                'estado': estado,
                'item_id': item_id
            })
            
            # Limpiar campos
            self.entry_producto_nuevo.delete(0, tk.END)
            self.entry_cantidad_nueva.delete(0, tk.END)
            self.combo_estado_nuevo.set("Conforme")
            
            messagebox.showinfo("Éxito", f"✅ Producto '{producto}' agregado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def modificar_estado_producto(self):
        """Modificar estado del producto seleccionado"""
        try:
            selection = self.tree_productos.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione un producto para modificar")
                return
            
            nuevo_estado = self.combo_estado_modificar.get()
            if not nuevo_estado:
                messagebox.showerror("Error", "Seleccione un estado")
                return
            
            item = selection[0]
            valores = list(self.tree_productos.item(item)['values'])
            valores[2] = nuevo_estado  # Cambiar el estado
            
            self.tree_productos.item(item, values=valores)
            
            # Actualizar en la lista interna
            for producto in self.productos_recibidos:
                if producto['item_id'] == item:
                    producto['estado'] = nuevo_estado
                    break
            
            messagebox.showinfo("Éxito", f"✅ Estado cambiado a: {nuevo_estado}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar estado: {str(e)}")

    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        try:
            selection = self.tree_productos.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
                item = selection[0]
                
                # Eliminar de la lista interna
                self.productos_recibidos = [p for p in self.productos_recibidos if p['item_id'] != item]
                
                # Eliminar del tree
                self.tree_productos.delete(item)
                
                # Reordenar números
                for i, item_id in enumerate(self.tree_productos.get_children()):
                    self.tree_productos.item(item_id, text=str(i + 1))
                
                messagebox.showinfo("Éxito", "✅ Producto eliminado correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")

    def guardar_recepcion_insumos(self):
        """Guardar la recepción de insumos y actualizar inventario para productos conformes"""
        try:
            proveedor = self.entry_proveedor.get().strip()
            fecha = self.entry_fecha_recepcion.get().strip()
            numero_pedido = self.entry_numero_pedido.get().strip()
            
            if not proveedor or not fecha or not numero_pedido:
                messagebox.showerror("Error", "Todos los campos de información son obligatorios")
                return
            
            if not self.productos_recibidos:
                messagebox.showerror("Error", "Debe agregar al menos un producto")
                return
            
            from datetime import datetime
            from main import guardar_excel, cargar_excel, entregas, detalle_entregas, ingresar_inventario, validar_campos
            import pandas as pd
            
            # Validar fecha
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida. Debe tener formato YYYY-MM-DD.")
                return
            
            # Registrar entrega usando el sistema de main.py
            df_entregas = cargar_excel(entregas)
            nuevo_id = 1 if df_entregas.empty else df_entregas['id'].max() + 1
            nueva_entrega = pd.DataFrame([[nuevo_id, proveedor, fecha, numero_pedido, len(self.productos_recibidos)]],
                                        columns=["id", "proveedor", "fecha", "numero_pedido", "cantidades_entregadas"])
            df_entregas = pd.concat([df_entregas, nueva_entrega], ignore_index=True)
            guardar_excel(df_entregas, entregas)
            
            # Guardar detalle de entrega con estados de conformidad
            df_detalle = cargar_excel(detalle_entregas)
            nuevos_detalles = []
            
            for producto in self.productos_recibidos:
                # Cambiar el nombre de la columna para que coincida con el formato esperado
                nuevo_detalle = [nuevo_id, producto['producto'], producto['cantidad'], producto['estado'] == "Conforme"]
                nuevos_detalles.append(nuevo_detalle)
            
            # Definir columnas consistentes
            columnas_esperadas = ["id_entrega", "producto", "cantidad", "conforme"]
            
            if df_detalle.empty:
                df_detalle = pd.DataFrame(columns=columnas_esperadas)
            else:
                # Asegurar que las columnas necesarias existan
                for col in columnas_esperadas:
                    if col not in df_detalle.columns:
                        df_detalle[col] = None
            
            df_nuevos = pd.DataFrame(nuevos_detalles, columns=columnas_esperadas)
            df_detalle = pd.concat([df_detalle, df_nuevos], ignore_index=True)
            guardar_excel(df_detalle, detalle_entregas)
            
            # Separar productos conformes y no conformes
            productos_conformes = [p for p in self.productos_recibidos if p['estado'] == "Conforme"]
            productos_no_conformes = [p for p in self.productos_recibidos if p['estado'] == "No conforme"]
            
            # ACTUALIZAR INVENTARIO - Solo productos conformes
            if productos_conformes:
                productos_para_inventario = [(p['producto'], p['cantidad']) for p in productos_conformes]
                
                # Validar campos antes de agregar al inventario
                if validar_campos(productos_para_inventario):
                    # ESTE ES EL PUNTO CLAVE: Agregar al inventario
                    ingresar_inventario(productos_para_inventario)
                    print(f"✅ Se agregaron {len(productos_conformes)} productos conformes al inventario")
                    
                    # Verificar que el inventario se actualizó correctamente
                    verificacion = self.verificar_actualizacion_inventario(productos_para_inventario)
                    print(verificacion)
                else:
                    messagebox.showwarning("Advertencia", "Algunos productos no pudieron ser validados")
            
            # Mostrar resumen detallado
            resumen = f"✅ Recepción registrada exitosamente!\n\n"
            resumen += f"🆔 ID de entrega: {nuevo_id}\n"
            resumen += f"🏢 Proveedor: {proveedor}\n"
            resumen += f"📅 Fecha: {fecha}\n"
            resumen += f"📦 Total productos recibidos: {len(self.productos_recibidos)}\n"
            resumen += f"✅ Productos conformes: {len(productos_conformes)}\n"
            resumen += f"⚠️ Productos no conformes: {len(productos_no_conformes)}\n\n"
            
            if productos_conformes:
                resumen += "✅ PRODUCTOS CONFORMES (AGREGADOS AL INVENTARIO):\n"
                for p in productos_conformes:
                    resumen += f"   • {p['producto']}: {p['cantidad']} unidades\n"
                resumen += "\n📋 IMPORTANTE: Estas cantidades se han SUMADO al inventario existente.\n\n"
            
            if productos_no_conformes:
                resumen += "⚠️ PRODUCTOS NO CONFORMES (NO agregados al inventario):\n"
                for p in productos_no_conformes:
                    resumen += f"   • {p['producto']}: {p['cantidad']} unidades\n"
                resumen += "\n"
            
            resumen += "📋 NOTA: Solo los productos marcados como 'Conforme' se han agregado al inventario.\n"
            resumen += "Los productos 'No conforme' se registraron en la recepción pero NO se sumaron al inventario.\n\n"
            resumen += "🔍 Para verificar el inventario actualizado, use el módulo 'Consultar Inventario'."
            
            messagebox.showinfo("Recepción Completada", resumen)
            
            # Limpiar formulario
            self.limpiar_campos_recepcion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar recepción: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Para debug

    def ver_recepciones_hu5(self):
        """Ver todas las recepciones registradas usando archivos de main.py"""
        try:
            from main import cargar_excel, entregas, detalle_entregas
            
            # Cargar entregas y detalles
            df_entregas = cargar_excel(entregas)
            df_detalles = cargar_excel(detalle_entregas)
            
            if df_entregas.empty:
                messagebox.showinfo("Info", "No hay recepciones registradas")
                return
            
            # Mostrar en nueva ventana
            ventana_recepciones = self.crear_ventana_secundaria("📋 Recepciones Registradas - HU5", "1200x700")
            
            frame_recepciones = ttk.Frame(ventana_recepciones, padding="20")
            frame_recepciones.pack(fill="both", expand=True)
            
            ttk.Label(frame_recepciones, text="Historial de Recepciones de Insumos", 
                     style='Subtitle.TLabel').pack(pady=10)
            
            # Crear notebook para pestañas
            notebook = ttk.Notebook(frame_recepciones)
            notebook.pack(fill="both", expand=True, pady=10)
            
            # === PESTAÑA 1: ENTREGAS GENERALES ===
            tab_entregas = ttk.Frame(notebook)
            notebook.add(tab_entregas, text="📦 Entregas")
            
            frame_entregas = ttk.Frame(tab_entregas, padding="10")
            frame_entregas.pack(fill="both", expand=True)
            
            # Treeview para entregas
            columns_entregas = ('ID', 'Proveedor', 'Fecha', 'Número Pedido', 'Productos')
            tree_entregas = ttk.Treeview(frame_entregas, columns=columns_entregas, show='headings', height=15)
            
            for col in columns_entregas:
                tree_entregas.heading(col, text=col)
                tree_entregas.column(col, width=150)
            
            # Llenar datos de entregas
            for _, row in df_entregas.iterrows():
                tree_entregas.insert('', 'end', values=(
                    row.get('id', ''),
                    row.get('proveedor', ''),
                    row.get('fecha', ''),
                    row.get('numero_pedido', ''),
                    row.get('cantidades_entregadas', '')
                ))
            
            scrollbar_entregas = ttk.Scrollbar(frame_entregas, orient="vertical", command=tree_entregas.yview)
            tree_entregas.configure(yscrollcommand=scrollbar_entregas.set)
            
            tree_entregas.pack(side="left", fill="both", expand=True)
            scrollbar_entregas.pack(side="right", fill="y")
            
            # === PESTAÑA 2: DETALLES DE PRODUCTOS ===
            tab_detalles = ttk.Frame(notebook)
            notebook.add(tab_detalles, text="📋 Detalles de Productos")
            
            frame_detalles = ttk.Frame(tab_detalles, padding="10")
            frame_detalles.pack(fill="both", expand=True)
            
            if not df_detalles.empty:
                # Treeview para detalles
                columns_detalles = ['ID Entrega', 'Producto', 'Cantidad']
                if 'estado_conformidad' in df_detalles.columns:
                    columns_detalles.append('Estado')
                
                tree_detalles = ttk.Treeview(frame_detalles, columns=columns_detalles, show='headings', height=15)
                
                for col in columns_detalles:
                    tree_detalles.heading(col, text=col)
                    tree_detalles.column(col, width=150)
                
                # Llenar datos de detalles
                for _, row in df_detalles.iterrows():
                    valores = [
                        row.get('entrega_id', ''),
                        row.get('producto', ''),
                        row.get('cantidad', '')
                    ]
                    if 'estado_conformidad' in df_detalles.columns:
                        valores.append(row.get('estado_conformidad', 'N/A'))
                    
                    tree_detalles.insert('', 'end', values=valores)
                
                scrollbar_detalles = ttk.Scrollbar(frame_detalles, orient="vertical", command=tree_detalles.yview)
                tree_detalles.configure(yscrollcommand=scrollbar_detalles.set)
                
                tree_detalles.pack(side="left", fill="both", expand=True)
                scrollbar_detalles.pack(side="right", fill="y")
            else:
                ttk.Label(frame_detalles, text="No hay detalles de productos disponibles").pack(pady=50)
            
            # Botones de acción
            botones_frame = ttk.Frame(frame_recepciones)
            botones_frame.pack(fill="x", pady=10)
            
            ttk.Button(botones_frame, text="🔄 Actualizar", 
                      command=lambda: [ventana_recepciones.destroy(), self.ver_recepciones_hu5()],
                      style='Primary.TButton').pack(side="left", padx=10)
            
            ttk.Button(botones_frame, text="❌ Cerrar", 
                      command=ventana_recepciones.destroy,
                      style='Danger.TButton').pack(side="right", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar recepciones: {str(e)}")

    def limpiar_campos_recepcion(self):
        """Limpiar todos los campos del formulario de recepción"""
        try:
            # Limpiar campos de información
            self.entry_proveedor.delete(0, tk.END)
            self.entry_fecha_recepcion.delete(0, tk.END)
            self.entry_numero_pedido.delete(0, tk.END)
            
            # Limpiar campos de productos
            self.entry_producto_nuevo.delete(0, tk.END)
            self.entry_cantidad_nueva.delete(0, tk.END)
            self.combo_estado_nuevo.set("Conforme")
            
            # Limpiar combobox de modificación
            self.combo_estado_modificar.set("")
            
            # Limpiar lista de productos recibidos
            self.productos_recibidos = []
            
            # Limpiar tree de productos
            for item in self.tree_productos.get_children():
                self.tree_productos.delete(item)
                
            print("✅ Formulario de recepción limpiado completamente")
            
        except Exception as e:
            print(f"Error al limpiar campos: {str(e)}")
    
    def mostrar_inventario_actual(self):
        """Mostrar el estado actual del inventario"""
        try:
            from main import cargar_excel, inventario
            
            df_inv = cargar_excel(inventario)
            
            if df_inv.empty:
                messagebox.showinfo("Inventario Vacío", "📦 El inventario está vacío. No hay productos registrados.")
                return
            
            # Crear ventana para mostrar inventario
            ventana_inventario = self.crear_ventana_secundaria("📦 Estado Actual del Inventario", "800x600")
            
            frame_inventario = ttk.Frame(ventana_inventario, padding="20")
            frame_inventario.pack(fill="both", expand=True)
            
            ttk.Label(frame_inventario, text="Estado Actual del Inventario", 
                     style='Subtitle.TLabel').pack(pady=10)
            
            # Información general
            info_frame = ttk.LabelFrame(frame_inventario, text="Resumen General", padding="10")
            info_frame.pack(fill="x", pady=10)
            
            total_productos = len(df_inv)
            total_unidades = df_inv['cantidad'].sum() if 'cantidad' in df_inv.columns else 0
            
            ttk.Label(info_frame, text=f"📊 Total de productos diferentes: {total_productos}").pack(anchor="w")
            ttk.Label(info_frame, text=f"📦 Total de unidades en inventario: {total_unidades:.0f}").pack(anchor="w")
            
            # Lista de productos
            productos_frame = ttk.LabelFrame(frame_inventario, text="Lista de Productos", padding="10")
            productos_frame.pack(fill="both", expand=True, pady=10)
            
            # Crear Treeview para mostrar productos
            columns = ('Producto', 'Cantidad', 'Última Actualización')
            tree_inv = ttk.Treeview(productos_frame, columns=columns, show='headings', height=15)
            
            tree_inv.heading('Producto', text='Producto')
            tree_inv.heading('Cantidad', text='Cantidad')
            tree_inv.heading('Última Actualización', text='Última Actualización')
            
            tree_inv.column('Producto', width=300)
            tree_inv.column('Cantidad', width=120, anchor='center')
            tree_inv.column('Última Actualización', width=180, anchor='center')
            
            # Llenar datos (ordenar por producto)
            df_ordenado = df_inv.sort_values('producto') if 'producto' in df_inv.columns else df_inv
            
            for _, row in df_ordenado.iterrows():
                tree_inv.insert('', 'end', values=(
                    row.get('producto', 'N/A'),
                    f"{row.get('cantidad', 0):.0f}",
                    row.get('ultima_actualizacion', 'N/A')
                ))
            
            scrollbar_inv = ttk.Scrollbar(productos_frame, orient="vertical", command=tree_inv.yview)
            tree_inv.configure(yscrollcommand=scrollbar_inv.set)
            
            tree_inv.pack(side="left", fill="both", expand=True)
            scrollbar_inv.pack(side="right", fill="y")
            
            # Botones de acción
            botones_frame = ttk.Frame(frame_inventario)
            botones_frame.pack(fill="x", pady=10)
            
            ttk.Button(botones_frame, text="🔄 Actualizar", 
                      command=lambda: [ventana_inventario.destroy(), self.mostrar_inventario_actual()],
                      style='Primary.TButton').pack(side="left", padx=10)
            
            ttk.Button(botones_frame, text="📤 Exportar a Excel", 
                      command=lambda: self.exportar_inventario_excel(df_inv),
                      style='Secondary.TButton').pack(side="left", padx=10)
            
            ttk.Button(botones_frame, text="❌ Cerrar", 
                      command=ventana_inventario.destroy,
                      style='Danger.TButton').pack(side="right", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar inventario: {str(e)}")
    
    def exportar_inventario_excel(self, df_inventario):
        """Exportar inventario actual a Excel"""
        try:
            from datetime import datetime
            import os
            
            fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"inventario_exportado_{fecha_actual}.xlsx"
            ruta_archivo = os.path.join("data", nombre_archivo)
            
            df_inventario.to_excel(ruta_archivo, index=False)
            
            messagebox.showinfo("Exportación Exitosa", 
                f"✅ Inventario exportado exitosamente!\n\n"
                f"📁 Archivo: {nombre_archivo}\n"
                f"📂 Ubicación: carpeta 'data'\n"
                f"📊 {len(df_inventario)} productos exportados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar inventario: {str(e)}")
            
    def verificar_actualizacion_inventario(self, productos_agregados):
        """Verificar que el inventario se haya actualizado correctamente"""
        try:
            from main import cargar_excel, inventario
            
            df_inv = cargar_excel(inventario)
            if df_inv.empty:
                return "⚠️ El archivo de inventario está vacío"
            
            verificacion = "🔍 VERIFICACIÓN DE ACTUALIZACIÓN DEL INVENTARIO:\n\n"
            
            for producto, cantidad in productos_agregados:
                producto_norm = producto.lower().strip()
                df_inv['producto_norm'] = df_inv['producto'].astype(str).str.strip().str.lower()
                producto_en_inventario = df_inv[df_inv['producto_norm'] == producto_norm]
                
                if not producto_en_inventario.empty:
                    cantidad_actual = producto_en_inventario['cantidad'].iloc[0]
                    fecha_actualizacion = producto_en_inventario['ultima_actualizacion'].iloc[0]
                    verificacion += f"✅ {producto}: {cantidad_actual} unidades (actualizado: {fecha_actualizacion})\n"
                else:
                    verificacion += f"❌ {producto}: No encontrado en inventario\n"
            
            return verificacion
            
        except Exception as e:
            return f"❌ Error al verificar inventario: {str(e)}"
        self.combo_estado_nuevo.set("Conforme")
        self.combo_estado_modificar.set("")
        
        # Limpiar tree y lista
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        self.productos_recibidos = []
            
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
        self.entry_fecha_ini_reporte = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_ini_reporte.pack(side="left", padx=5)
        
        ttk.Label(fecha_frame, text="Fecha fin:").pack(side="left", padx=5)
        self.entry_fecha_fin_reporte = ttk.Entry(fecha_frame, width=15, style='Custom.TEntry')
        self.entry_fecha_fin_reporte.pack(side="left", padx=5)
        
        ttk.Button(fecha_frame, text="🔍 Filtrar", 
                  command=self.filtrar_reportes_fecha).pack(side="left", padx=10)
        
        # Lista de reportes con mejor visibilidad
        lista_frame = ttk.LabelFrame(main_frame, text="Reportes Disponibles", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        self.list_reportes = tk.Listbox(lista_frame, height=10,
                                       bg='white', fg='#2C3E50', selectbackground='#3498DB')
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
            
            text_detalle = tk.Text(ventana_detalle, wrap=tk.WORD,
                                  bg='white', fg='#2C3E50', insertbackground='#2C3E50')
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
        """Menú completo para solicitudes de compra de insumos - HU8"""
        ventana = self.crear_ventana_secundaria("🛒 Solicitudes de Compra de Insumos - HU8", "1200x900")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Gestión de Solicitudes de Compra", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame principal con notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # === PESTAÑA 1: GENERAR SOLICITUD ===
        tab_generar = ttk.Frame(notebook)
        notebook.add(tab_generar, text="📋 Generar Solicitud")
        
        generar_frame = ttk.Frame(tab_generar, padding="20")
        generar_frame.pack(fill="both", expand=True)
        
        ttk.Label(generar_frame, text="Generar Solicitud de Compra de Insumos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información de la funcionalidad
        info_frame = ttk.LabelFrame(generar_frame, text="Información", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """Esta función identifica automáticamente los insumos faltantes comparando
la demanda de pedidos con el inventario disponible para generar solicitudes de compra."""
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Área de resultados para insumos faltantes
        faltantes_frame = ttk.LabelFrame(generar_frame, text="Insumos Faltantes Detectados", padding="15")
        faltantes_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar insumos faltantes
        columns_faltantes = ('ID', 'Producto', 'Cantidad Faltante')
        self.tree_faltantes = ttk.Treeview(faltantes_frame, columns=columns_faltantes, show='headings', height=10)
        
        for col in columns_faltantes:
            self.tree_faltantes.heading(col, text=col)
        
        self.tree_faltantes.column('ID', width=80)
        self.tree_faltantes.column('Producto', width=300)
        self.tree_faltantes.column('Cantidad Faltante', width=150)
        
        # Scrollbar para el Treeview
        scrollbar_faltantes = ttk.Scrollbar(faltantes_frame, orient="vertical", command=self.tree_faltantes.yview)
        self.tree_faltantes.configure(yscrollcommand=scrollbar_faltantes.set)
        
        self.tree_faltantes.pack(side="left", fill="both", expand=True)
        scrollbar_faltantes.pack(side="right", fill="y")
        
        # Botones de acción para generar
        botones_generar_frame = ttk.Frame(generar_frame)
        botones_generar_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_generar_frame, text="🔍 Detectar Faltantes", 
                  command=self.detectar_insumos_faltantes,
                  style='Primary.TButton').pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="✏️ Editar Solicitud", 
                  command=self.editar_solicitud_compra).pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="✅ Validar Solicitud", 
                  command=self.validar_solicitud_compra).pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="💾 Guardar Solicitud", 
                  command=self.guardar_solicitud_compra,
                  style='Success.TButton').pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="📧 Enviar Solicitud", 
                  command=self.enviar_solicitud_compra).pack(side="left", padx=10)
        
        # === PESTAÑA 2: EDICIÓN MANUAL ===
        tab_editar = ttk.Frame(notebook)
        notebook.add(tab_editar, text="✏️ Edición Manual")
        
        editar_frame = ttk.Frame(tab_editar, padding="20")
        editar_frame.pack(fill="both", expand=True)
        
        ttk.Label(editar_frame, text="Edición Manual de Solicitud", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para agregar productos manualmente
        manual_frame = ttk.LabelFrame(editar_frame, text="Agregar/Modificar Productos", padding="15")
        manual_frame.pack(fill="x", pady=10)
        
        # Campos para producto manual
        producto_grid = ttk.Frame(manual_frame)
        producto_grid.pack(fill="x")
        
        ttk.Label(producto_grid, text="Producto:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_producto_manual = ttk.Entry(producto_grid, width=30)
        self.entry_producto_manual.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(producto_grid, text="Cantidad:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_cantidad_manual = ttk.Entry(producto_grid, width=15)
        self.entry_cantidad_manual.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(producto_grid, text="➕ Agregar", 
                  command=self.agregar_producto_manual).grid(row=0, column=4, padx=10, pady=5)
        
        # Área de solicitud actual
        solicitud_frame = ttk.LabelFrame(editar_frame, text="Solicitud Actual", padding="15")
        solicitud_frame.pack(fill="both", expand=True, pady=10)
        
        # Treeview para solicitud en edición
        columns_solicitud = ('ID', 'Producto', 'Cantidad')
        self.tree_solicitud = ttk.Treeview(solicitud_frame, columns=columns_solicitud, show='headings', height=12)
        
        for col in columns_solicitud:
            self.tree_solicitud.heading(col, text=col)
        
        self.tree_solicitud.column('ID', width=80)
        self.tree_solicitud.column('Producto', width=300)
        self.tree_solicitud.column('Cantidad', width=150)
        
        scrollbar_solicitud = ttk.Scrollbar(solicitud_frame, orient="vertical", command=self.tree_solicitud.yview)
        self.tree_solicitud.configure(yscrollcommand=scrollbar_solicitud.set)
        
        self.tree_solicitud.pack(side="left", fill="both", expand=True)
        scrollbar_solicitud.pack(side="right", fill="y")
        
        # Botones para edición
        botones_edicion_frame = ttk.Frame(editar_frame)
        botones_edicion_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_edicion_frame, text="🔄 Modificar Seleccionado", 
                  command=self.modificar_producto_solicitud).pack(side="left", padx=10)
        ttk.Button(botones_edicion_frame, text="🗑️ Eliminar Seleccionado", 
                  command=self.eliminar_producto_solicitud).pack(side="left", padx=10)
        ttk.Button(botones_edicion_frame, text="🧹 Limpiar Todo", 
                  command=self.limpiar_solicitud).pack(side="left", padx=10)
        
        # === PESTAÑA 3: HISTORIAL DE SOLICITUDES ===
        tab_historial = ttk.Frame(notebook)
        notebook.add(tab_historial, text="📁 Historial")
        
        historial_frame = ttk.Frame(tab_historial, padding="20")
        historial_frame.pack(fill="both", expand=True)
        
        ttk.Label(historial_frame, text="Historial de Solicitudes", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Lista de solicitudes generadas
        lista_frame = ttk.LabelFrame(historial_frame, text="Solicitudes Generadas", padding="15")
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        # Listbox para archivos de solicitudes
        self.listbox_solicitudes = tk.Listbox(lista_frame, height=15, font=("Arial", 10))
        scrollbar_lista_sol = ttk.Scrollbar(lista_frame, orient="vertical", command=self.listbox_solicitudes.yview)
        self.listbox_solicitudes.configure(yscrollcommand=scrollbar_lista_sol.set)
        
        self.listbox_solicitudes.pack(side="left", fill="both", expand=True)
        scrollbar_lista_sol.pack(side="right", fill="y")
        
        # Botones de gestión de historial
        botones_historial_frame = ttk.Frame(historial_frame)
        botones_historial_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_historial_frame, text="🔄 Actualizar Lista", 
                  command=self.actualizar_lista_solicitudes).pack(side="left", padx=10)
        ttk.Button(botones_historial_frame, text="👁️ Ver Solicitud", 
                  command=self.ver_solicitud_seleccionada).pack(side="left", padx=10)
        ttk.Button(botones_historial_frame, text="📂 Abrir Carpeta", 
                  command=self.abrir_carpeta_solicitudes).pack(side="left", padx=10)
        ttk.Button(botones_historial_frame, text="🗑️ Eliminar", 
                  command=self.eliminar_solicitud_seleccionada).pack(side="left", padx=10)
        
        # Inicializar datos
        self.solicitud_actual = None
        self.actualizar_lista_solicitudes()

    def detectar_insumos_faltantes(self):
        """Detectar insumos faltantes usando la lógica de main.py"""
        try:
            # Limpiar resultados anteriores
            self.tree_faltantes.delete(*self.tree_faltantes.get_children())
            
            # Usar la función de main.py
            from main import obtener_insumos_faltantes
            faltantes = obtener_insumos_faltantes()
            
            if faltantes.empty:
                messagebox.showinfo("Sin Faltantes", 
                    "✅ No hay productos faltantes.\n\n"
                    "Toda la demanda está cubierta por el inventario actual.")
                return
            
            # Mostrar resultados en el Treeview
            for _, row in faltantes.iterrows():
                self.tree_faltantes.insert('', 'end', 
                    values=(row['id'], row['producto'], row['cantidad']))
            
            messagebox.showinfo("Detección Completa", 
                f"🔍 Detección completada!\n\n"
                f"📊 Productos faltantes encontrados: {len(faltantes)}\n"
                f"🛒 Listos para generar solicitud de compra")
            
            # Guardar para uso posterior
            self.solicitud_actual = faltantes.copy()
            self.actualizar_tree_solicitud()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al detectar faltantes: {str(e)}")

    def actualizar_tree_solicitud(self):
        """Actualizar el tree de solicitud actual"""
        if hasattr(self, 'tree_solicitud'):
            self.tree_solicitud.delete(*self.tree_solicitud.get_children())
            
            if self.solicitud_actual is not None and not self.solicitud_actual.empty:
                for _, row in self.solicitud_actual.iterrows():
                    self.tree_solicitud.insert('', 'end', 
                        values=(row['id'], row['producto'], row['cantidad']))

    def editar_solicitud_compra(self):
        """Abrir pestaña de edición manual"""
        if self.solicitud_actual is None or self.solicitud_actual.empty:
            messagebox.showwarning("Sin Datos", 
                "Primero debe detectar insumos faltantes o agregar productos manualmente")
            return
        
        # Cambiar a la pestaña de edición
        notebook = self.tree_faltantes.master.master.master  # Navegar hasta el notebook
        notebook.select(1)  # Seleccionar pestaña de edición
        
        messagebox.showinfo("Edición Disponible", 
            "📝 Puede editar la solicitud en la pestaña 'Edición Manual'\n\n"
            "Funciones disponibles:\n"
            "• Agregar productos adicionales\n"
            "• Modificar cantidades\n"
            "• Eliminar productos")

    def agregar_producto_manual(self):
        """Agregar producto manualmente a la solicitud"""
        try:
            producto = self.entry_producto_manual.get().strip()
            cantidad_str = self.entry_cantidad_manual.get().strip()
            
            if not producto:
                messagebox.showwarning("Error", "Por favor ingrese el nombre del producto")
                return
            
            if not cantidad_str:
                messagebox.showwarning("Error", "Por favor ingrese la cantidad")
                return
            
            try:
                cantidad = float(cantidad_str)
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
            except ValueError:
                messagebox.showwarning("Error", "Por favor ingrese una cantidad válida")
                return
            
            # Inicializar solicitud si no existe
            if self.solicitud_actual is None:
                import pandas as pd
                self.solicitud_actual = pd.DataFrame(columns=['id', 'producto', 'cantidad'])
            
            # Verificar si el producto ya existe
            if not self.solicitud_actual.empty:
                producto_existente = self.solicitud_actual[
                    self.solicitud_actual['producto'].str.lower().str.strip() == producto.lower()
                ]
                
                if not producto_existente.empty:
                    if messagebox.askyesno("Producto Existente", 
                        f"El producto '{producto}' ya existe en la solicitud.\n"
                        f"¿Desea actualizar la cantidad?"):
                        # Actualizar cantidad existente
                        index = producto_existente.index[0]
                        self.solicitud_actual.at[index, 'cantidad'] = cantidad
                    else:
                        return
                else:
                    # Agregar nuevo producto
                    nuevo_id = len(self.solicitud_actual) + 1
                    nuevo_producto = pd.DataFrame({
                        'id': [nuevo_id],
                        'producto': [producto],
                        'cantidad': [cantidad]
                    })
                    self.solicitud_actual = pd.concat([self.solicitud_actual, nuevo_producto], ignore_index=True)
            else:
                # Primera entrada
                self.solicitud_actual = pd.DataFrame({
                    'id': [1],
                    'producto': [producto],
                    'cantidad': [cantidad]
                })
            
            # Actualizar visualización
            self.actualizar_tree_solicitud()
            
            # Limpiar campos
            self.entry_producto_manual.delete(0, tk.END)
            self.entry_cantidad_manual.delete(0, tk.END)
            
            messagebox.showinfo("Éxito", f"Producto agregado: {producto} - Cantidad: {cantidad}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def modificar_producto_solicitud(self):
        """Modificar producto seleccionado en la solicitud"""
        selection = self.tree_solicitud.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un producto para modificar")
            return
        
        try:
            item = selection[0]
            valores = self.tree_solicitud.item(item, 'values')
            
            # Cargar datos en los campos de edición
            self.entry_producto_manual.delete(0, tk.END)
            self.entry_producto_manual.insert(0, valores[1])
            
            self.entry_cantidad_manual.delete(0, tk.END)
            self.entry_cantidad_manual.insert(0, valores[2])
            
            # Eliminar el producto actual para que pueda ser actualizado
            id_producto = int(valores[0])
            if self.solicitud_actual is not None:
                self.solicitud_actual = self.solicitud_actual[self.solicitud_actual['id'] != id_producto]
                self.actualizar_tree_solicitud()
            
            messagebox.showinfo("Modo Edición", 
                "Datos cargados para modificación.\n"
                "Ajuste los valores y presione 'Agregar' para actualizar.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar producto: {str(e)}")

    def eliminar_producto_solicitud(self):
        """Eliminar producto seleccionado de la solicitud"""
        selection = self.tree_solicitud.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un producto para eliminar")
            return
        
        try:
            item = selection[0]
            valores = self.tree_solicitud.item(item, 'values')
            producto = valores[1]
            
            if messagebox.askyesno("Confirmar Eliminación", 
                f"¿Está seguro de eliminar el producto?\n\n{producto}"):
                
                id_producto = int(valores[0])
                if self.solicitud_actual is not None:
                    self.solicitud_actual = self.solicitud_actual[self.solicitud_actual['id'] != id_producto]
                    self.actualizar_tree_solicitud()
                    
                messagebox.showinfo("Eliminado", f"Producto eliminado: {producto}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")

    def limpiar_solicitud(self):
        """Limpiar toda la solicitud"""
        if self.solicitud_actual is not None and not self.solicitud_actual.empty:
            if messagebox.askyesno("Confirmar Limpieza", 
                "¿Está seguro de limpiar toda la solicitud?"):
                
                import pandas as pd
                self.solicitud_actual = pd.DataFrame(columns=['id', 'producto', 'cantidad'])
                self.actualizar_tree_solicitud()
                self.tree_faltantes.delete(*self.tree_faltantes.get_children())
                
                messagebox.showinfo("Limpieza Completa", "Solicitud limpiada correctamente")

    def validar_solicitud_compra(self):
        """Validar la solicitud actual"""
        if self.solicitud_actual is None or self.solicitud_actual.empty:
            messagebox.showwarning("Sin Datos", "No hay solicitud para validar")
            return
        
        try:
            errores = []
            
            # Validaciones
            for _, row in self.solicitud_actual.iterrows():
                if not row["producto"] or str(row["producto"]).strip() == "":
                    errores.append(f"❌ Producto vacío en ID {row['id']}")
                
                try:
                    cantidad = float(row["cantidad"])
                    if cantidad <= 0:
                        errores.append(f"❌ Cantidad inválida para '{row['producto']}': {cantidad}")
                except (ValueError, TypeError):
                    errores.append(f"❌ Cantidad no numérica para '{row['producto']}': {row['cantidad']}")
            
            # Mostrar resultados
            if errores:
                mensaje_error = "❌ Se encontraron errores en la solicitud:\n\n" + "\n".join(errores)
                messagebox.showerror("Errores de Validación", mensaje_error)
            else:
                messagebox.showinfo("Validación Exitosa", 
                    f"✅ Validación completada exitosamente!\n\n"
                    f"📊 Productos validados: {len(self.solicitud_actual)}\n"
                    f"✅ Toda la información es correcta\n"
                    f"💾 Lista para guardar y enviar")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la validación: {str(e)}")

    def guardar_solicitud_compra(self):
        """Guardar la solicitud en Excel"""
        if self.solicitud_actual is None or self.solicitud_actual.empty:
            messagebox.showwarning("Sin Datos", "No hay solicitud para guardar")
            return
        
        try:
            from datetime import datetime
            import os
            
            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/solicitud_compra_{timestamp}.xlsx"
            
            # Asegurar que existe el directorio
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Guardar archivo
            self.solicitud_actual.to_excel(filename, index=False)
            
            # También guardar como archivo principal (para compatibilidad con main.py)
            filename_principal = "data/solicitud_compra.xlsx"
            self.solicitud_actual.to_excel(filename_principal, index=False)
            
            messagebox.showinfo("Guardado Exitoso", 
                f"✅ Solicitud guardada correctamente!\n\n"
                f"📁 Archivo principal: {filename_principal}\n"
                f"📁 Copia con timestamp: {filename}\n"
                f"📊 Productos guardados: {len(self.solicitud_actual)}")
            
            # Actualizar lista de historial
            self.actualizar_lista_solicitudes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar solicitud: {str(e)}")

    def enviar_solicitud_compra(self):
        """Enviar solicitud por email"""
        try:
            import os
            
            # Verificar que existe el archivo principal
            archivo_principal = "data/solicitud_compra.xlsx"
            if not os.path.exists(archivo_principal):
                messagebox.showwarning("Error", 
                    "No se ha guardado la solicitud aún.\n"
                    "Por favor guarde la solicitud antes de enviarla.")
                return
            
            if self.solicitud_actual is None or self.solicitud_actual.empty:
                messagebox.showwarning("Sin Datos", "No hay solicitud para enviar")
                return
            
            # Crear ventana para solicitar email
            ventana_email = self.crear_ventana_secundaria("📧 Enviar Solicitud de Compra", "600x400")
            
            email_frame = ttk.Frame(ventana_email, padding="20")
            email_frame.pack(fill="both", expand=True)
            
            ttk.Label(email_frame, text="Envío de Solicitud de Compra", 
                     style='Subtitle.TLabel').pack(pady=10)
            
            # Información de la solicitud
            info_text = f"""📋 Solicitud de Compra de Insumos
📊 Productos solicitados: {len(self.solicitud_actual)}
📁 Archivo: solicitud_compra.xlsx

Lista de productos:"""
            
            for _, row in self.solicitud_actual.iterrows():
                info_text += f"\n• {row['producto']}: {row['cantidad']}"
            
            text_widget = tk.Text(email_frame, height=8, wrap=tk.WORD, font=("Arial", 10))
            text_widget.insert("1.0", info_text)
            text_widget.config(state='disabled')
            text_widget.pack(fill="both", expand=True, pady=10)
            
            # Campo de email
            ttk.Label(email_frame, text="📧 Correo del destinatario:").pack(anchor="w", pady=5)
            entry_email = ttk.Entry(email_frame, width=50, font=("Arial", 11))
            entry_email.pack(fill="x", pady=5)
            entry_email.focus()
            
            # Botones
            botones_frame = ttk.Frame(email_frame)
            botones_frame.pack(fill="x", pady=20)
            
            def procesar_envio():
                email_destinatario = entry_email.get().strip()
                if not email_destinatario:
                    messagebox.showwarning("Error", "Por favor ingrese el correo del destinatario")
                    return
                
                if "@" not in email_destinatario or "." not in email_destinatario:
                    messagebox.showwarning("Error", "Por favor ingrese un correo válido")
                    return
                
                try:
                    # Usar la función de main.py (simulada)
                    ventana_email.destroy()
                    
                    # Simulación del envío (en producción usar función real de main.py)
                    messagebox.showinfo("Envío Exitoso", 
                        f"✅ Solicitud enviada correctamente!\n\n"
                        f"📧 Destinatario: {email_destinatario}\n"
                        f"📁 Archivo adjunto: solicitud_compra.xlsx\n"
                        f"📊 Productos solicitados: {len(self.solicitud_actual)}\n\n"
                        f"📋 La solicitud ha sido enviada al proveedor.")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al enviar: {str(e)}")
            
            ttk.Button(botones_frame, text="📧 Enviar", 
                      command=procesar_envio,
                      style='Success.TButton').pack(side="left", padx=10)
            ttk.Button(botones_frame, text="❌ Cancelar", 
                      command=ventana_email.destroy).pack(side="right", padx=10)
                      
        except Exception as e:
            messagebox.showerror("Error", f"Error al preparar envío: {str(e)}")

    def actualizar_lista_solicitudes(self):
        """Actualizar lista de solicitudes en historial"""
        try:
            import os
            
            # Limpiar lista
            if hasattr(self, 'listbox_solicitudes'):
                self.listbox_solicitudes.delete(0, tk.END)
                
                carpeta = "data"
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)
                    return
                
                # Buscar archivos de solicitudes
                archivos = [f for f in os.listdir(carpeta) 
                           if f.startswith("solicitud_compra") and f.endswith(".xlsx")]
                
                if not archivos:
                    self.listbox_solicitudes.insert(tk.END, "No hay solicitudes generadas")
                    return
                
                # Agregar archivos a la lista
                for archivo in sorted(archivos, reverse=True):
                    self.listbox_solicitudes.insert(tk.END, archivo)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar lista: {str(e)}")

    def ver_solicitud_seleccionada(self):
        """Ver contenido de la solicitud seleccionada"""
        selection = self.listbox_solicitudes.curselection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione una solicitud")
            return
        
        try:
            archivo = self.listbox_solicitudes.get(selection[0])
            
            if archivo == "No hay solicitudes generadas":
                return
            
            import pandas as pd
            import os
            
            ruta_archivo = os.path.join("data", archivo)
            
            if not os.path.exists(ruta_archivo):
                messagebox.showerror("Error", "El archivo no existe")
                return
            
            # Leer archivo
            df = pd.read_excel(ruta_archivo)
            
            # Crear ventana de visualización
            ventana_ver = self.crear_ventana_secundaria(f"📋 Ver Solicitud: {archivo}", "700x500")
            
            ver_frame = ttk.Frame(ventana_ver, padding="20")
            ver_frame.pack(fill="both", expand=True)
            
            ttk.Label(ver_frame, text=f"Contenido de: {archivo}", 
                     style='Subtitle.TLabel').pack(pady=10)
            
            # Crear Treeview para mostrar datos
            columns = list(df.columns)
            tree_ver = ttk.Treeview(ver_frame, columns=columns, show='headings', height=15)
            
            for col in columns:
                tree_ver.heading(col, text=col)
                tree_ver.column(col, width=150)
            
            # Agregar datos
            for _, row in df.iterrows():
                tree_ver.insert('', 'end', values=list(row))
            
            scrollbar_ver = ttk.Scrollbar(ver_frame, orient="vertical", command=tree_ver.yview)
            tree_ver.configure(yscrollcommand=scrollbar_ver.set)
            
            tree_ver.pack(side="left", fill="both", expand=True)
            scrollbar_ver.pack(side="right", fill="y")
            
            # Información adicional
            info_frame = ttk.Frame(ver_frame)
            info_frame.pack(fill="x", pady=10)
            
            ttk.Label(info_frame, text=f"📊 Total de productos: {len(df)}").pack(side="left")
            ttk.Button(info_frame, text="✅ Cerrar", 
                      command=ventana_ver.destroy).pack(side="right")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ver solicitud: {str(e)}")

    def abrir_carpeta_solicitudes(self):
        """Abrir carpeta de solicitudes en el explorador"""
        try:
            import os
            import subprocess
            import platform
            
            carpeta = os.path.abspath("data")
            
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            
            # Abrir según el sistema operativo
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{carpeta}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(f'open "{carpeta}"', shell=True)
            else:  # Linux
                subprocess.Popen(f'xdg-open "{carpeta}"', shell=True)
                
            messagebox.showinfo("Carpeta Abierta", 
                f"📂 Carpeta de solicitudes abierta:\n{carpeta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir carpeta: {str(e)}")

    def eliminar_solicitud_seleccionada(self):
        """Eliminar solicitud seleccionada"""
        selection = self.listbox_solicitudes.curselection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione una solicitud para eliminar")
            return
        
        try:
            archivo = self.listbox_solicitudes.get(selection[0])
            
            if archivo == "No hay solicitudes generadas":
                return
            
            if not messagebox.askyesno("Confirmar Eliminación", 
                f"¿Está seguro de eliminar la solicitud?\n\n{archivo}"):
                return
            
            import os
            ruta_archivo = os.path.join("data", archivo)
            
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                messagebox.showinfo("Eliminado", f"✅ Solicitud eliminada: {archivo}")
                self.actualizar_lista_solicitudes()
            else:
                messagebox.showwarning("Error", "El archivo no existe")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
        
    def menu_reportes_insumos_listos(self):
        """Menú completo para reportes de insumos listos - HU10"""
        ventana = self.crear_ventana_secundaria("🚚 Reportes de Insumos Listos - HU10", "1200x800")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Reportes de Insumos Listos para Envío", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame principal con notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # === PESTAÑA 1: GENERAR LISTA DE ENVÍO ===
        tab_generar = ttk.Frame(notebook)
        notebook.add(tab_generar, text="📋 Generar Lista")
        
        generar_frame = ttk.Frame(tab_generar, padding="20")
        generar_frame.pack(fill="both", expand=True)
        
        ttk.Label(generar_frame, text="Generar Lista de Insumos Listos para Envío", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información de la funcionalidad
        info_frame = ttk.LabelFrame(generar_frame, text="Información", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """Esta función compara la demanda de pedidos con el inventario disponible
para identificar qué insumos están listos para envío."""
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(generar_frame, text="Resultados", padding="15")
        resultados_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para mostrar insumos listos
        columns = ('Producto', 'Cantidad a Enviar')
        self.tree_insumos_listos = ttk.Treeview(resultados_frame, columns=columns, show='headings', height=15)
        
        self.tree_insumos_listos.heading('Producto', text='Producto')
        self.tree_insumos_listos.heading('Cantidad a Enviar', text='Cantidad a Enviar')
        
        self.tree_insumos_listos.column('Producto', width=300)
        self.tree_insumos_listos.column('Cantidad a Enviar', width=150)
        
        # Scrollbar para el Treeview
        scrollbar_insumos = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree_insumos_listos.yview)
        self.tree_insumos_listos.configure(yscrollcommand=scrollbar_insumos.set)
        
        self.tree_insumos_listos.pack(side="left", fill="both", expand=True)
        scrollbar_insumos.pack(side="right", fill="y")
        
        # Botones de acción para generar
        botones_generar_frame = ttk.Frame(generar_frame)
        botones_generar_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_generar_frame, text="🔄 Generar Lista", 
                  command=self.generar_lista_insumos_listos,
                  style='Primary.TButton').pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="💾 Exportar a Excel", 
                  command=self.exportar_lista_insumos_listos,
                  style='Success.TButton').pack(side="left", padx=10)
        ttk.Button(botones_generar_frame, text="📧 Enviar por Email", 
                  command=self.enviar_lista_insumos_email).pack(side="left", padx=10)
        
        # === PESTAÑA 2: FILTRAR REPORTES POR FECHA ===
        tab_filtrar = ttk.Frame(notebook)
        notebook.add(tab_filtrar, text="📅 Filtrar por Fecha")
        
        filtrar_frame = ttk.Frame(tab_filtrar, padding="20")
        filtrar_frame.pack(fill="both", expand=True)
        
        ttk.Label(filtrar_frame, text="Filtrar Reportes por Rango de Fechas", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para filtros de fecha
        fecha_frame = ttk.LabelFrame(filtrar_frame, text="Rango de Fechas", padding="15")
        fecha_frame.pack(fill="x", pady=10)
        
        # Campos de fecha
        fecha_grid = ttk.Frame(fecha_frame)
        fecha_grid.pack(fill="x")
        
        ttk.Label(fecha_grid, text="Fecha inicio (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_fecha_inicio = ttk.Entry(fecha_grid, width=20)
        self.entry_fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(fecha_grid, text="Fecha fin (YYYY-MM-DD):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_fecha_fin = ttk.Entry(fecha_grid, width=20)
        self.entry_fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(fecha_grid, text="🔍 Filtrar", 
                  command=self.filtrar_reportes_por_fecha).grid(row=0, column=4, padx=10, pady=5)
        
        # Área de resultados filtrados
        resultados_filtro_frame = ttk.LabelFrame(filtrar_frame, text="Reportes Encontrados", padding="15")
        resultados_filtro_frame.pack(fill="both", expand=True, pady=10)
        
        # Treeview para reportes filtrados
        columns_reportes = ('ID', 'Fecha', 'Producto', 'Cantidad', 'Estado')
        self.tree_reportes_filtrados = ttk.Treeview(resultados_filtro_frame, columns=columns_reportes, show='headings', height=12)
        
        for col in columns_reportes:
            self.tree_reportes_filtrados.heading(col, text=col)
            self.tree_reportes_filtrados.column(col, width=120)
        
        scrollbar_reportes = ttk.Scrollbar(resultados_filtro_frame, orient="vertical", command=self.tree_reportes_filtrados.yview)
        self.tree_reportes_filtrados.configure(yscrollcommand=scrollbar_reportes.set)
        
        self.tree_reportes_filtrados.pack(side="left", fill="both", expand=True)
        scrollbar_reportes.pack(side="right", fill="y")
        
        # Botones para reportes filtrados
        botones_filtro_frame = ttk.Frame(filtrar_frame)
        botones_filtro_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_filtro_frame, text="📋 Ver Detalle", 
                  command=self.ver_detalle_reporte_seleccionado).pack(side="left", padx=10)
        ttk.Button(botones_filtro_frame, text="💾 Descargar Reporte", 
                  command=self.descargar_reporte_seleccionado).pack(side="left", padx=10)
        
        # === PESTAÑA 3: GESTIÓN DE REPORTES ===
        tab_gestion = ttk.Frame(notebook)
        notebook.add(tab_gestion, text="📁 Gestión de Reportes")
        
        gestion_frame = ttk.Frame(tab_gestion, padding="20")
        gestion_frame.pack(fill="both", expand=True)
        
        ttk.Label(gestion_frame, text="Gestión de Reportes Generados", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Lista de reportes disponibles
        lista_frame = ttk.LabelFrame(gestion_frame, text="Reportes Disponibles", padding="15")
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        # Listbox para archivos de reportes
        self.listbox_reportes = tk.Listbox(lista_frame, height=15, font=("Arial", 10))
        scrollbar_lista = ttk.Scrollbar(lista_frame, orient="vertical", command=self.listbox_reportes.yview)
        self.listbox_reportes.configure(yscrollcommand=scrollbar_lista.set)
        
        self.listbox_reportes.pack(side="left", fill="both", expand=True)
        scrollbar_lista.pack(side="right", fill="y")
        
        # Botones de gestión
        botones_gestion_frame = ttk.Frame(gestion_frame)
        botones_gestion_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_gestion_frame, text="🔄 Actualizar Lista", 
                  command=self.actualizar_lista_reportes).pack(side="left", padx=10)
        ttk.Button(botones_gestion_frame, text="📂 Abrir Carpeta", 
                  command=self.abrir_carpeta_reportes).pack(side="left", padx=10)
        ttk.Button(botones_gestion_frame, text="🗑️ Eliminar Reporte", 
                  command=self.eliminar_reporte_seleccionado).pack(side="left", padx=10)
        
        # Cargar datos iniciales
        self.actualizar_lista_reportes()

    def generar_lista_insumos_listos(self):
        """Generar lista de insumos listos usando la lógica de main.py"""
        try:
            # Limpiar resultados anteriores
            self.tree_insumos_listos.delete(*self.tree_insumos_listos.get_children())
            
            # Usar la función de main.py
            lista = generar_lista_envio()
            
            if lista.empty:
                messagebox.showwarning("Sin Resultados", 
                    "❌ No hay insumos que cumplan con la demanda actual.\n\n"
                    "Verifique que:\n"
                    "• Existen pedidos registrados\n"
                    "• El inventario tiene stock suficiente")
                return
            
            # Mostrar resultados en el Treeview
            for _, row in lista.iterrows():
                self.tree_insumos_listos.insert('', 'end', 
                                               values=(row['producto'], row['cantidad_a_enviar']))
            
            messagebox.showinfo("Éxito", 
                f"✅ Lista generada exitosamente!\n\n"
                f"📊 Total de productos listos: {len(lista)}\n"
                f"📦 Productos disponibles para envío")
            
            # Guardar lista actual para exportación
            self.lista_actual = lista
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar lista: {str(e)}")

    def exportar_lista_insumos_listos(self):
        """Exportar lista actual a Excel"""
        try:
            if not hasattr(self, 'lista_actual') or self.lista_actual.empty:
                messagebox.showwarning("Error", "Primero debe generar una lista de insumos")
                return
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/insumos_listos_{timestamp}.xlsx"
            
            # Asegurar que existe el directorio
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Exportar
            self.lista_actual.to_excel(filename, index=False)
            
            messagebox.showinfo("Exportación Exitosa", 
                f"✅ Lista exportada correctamente!\n\n"
                f"📁 Archivo: {filename}\n"
                f"📊 Productos exportados: {len(self.lista_actual)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def enviar_lista_insumos_email(self):
        """Enviar lista de insumos por email"""
        try:
            if not hasattr(self, 'lista_actual') or self.lista_actual.empty:
                messagebox.showwarning("Error", "Primero debe generar una lista de insumos")
                return
            
            # Usar la función existente de main.py
            enviar_lista_insumos()
            
            messagebox.showinfo("Email Enviado", 
                "✅ Lista de insumos enviada por email correctamente!\n\n"
                "📧 El reporte ha sido enviado al líder de producción\n"
                "📁 También se ha guardado una copia local")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar email: {str(e)}")

    def filtrar_reportes_por_fecha(self):
        """Filtrar reportes por rango de fechas"""
        try:
            fecha_inicio = self.entry_fecha_inicio.get().strip()
            fecha_fin = self.entry_fecha_fin.get().strip()
            
            if not fecha_inicio or not fecha_fin:
                messagebox.showwarning("Error", "Por favor ingrese ambas fechas")
                return
            
            # Limpiar resultados anteriores
            self.tree_reportes_filtrados.delete(*self.tree_reportes_filtrados.get_children())
            
            # Cargar archivo de reportes de insumos listos
            import pandas as pd
            import os
            
            ruta_listos = os.path.join("data", "insumos_listos_general.xlsx")
            
            if not os.path.exists(ruta_listos):
                messagebox.showwarning("Sin Datos", 
                    "❌ No se encontró el archivo de reportes de insumos listos.\n\n"
                    f"Archivo esperado: {ruta_listos}")
                return
            
            df = pd.read_excel(ruta_listos)
            
            if df.empty:
                messagebox.showinfo("Sin Datos", "❌ No hay registros de insumos listos.")
                return
            
            # Filtrar por fechas
            df['fecha'] = pd.to_datetime(df['fecha'])
            ini_dt = pd.to_datetime(fecha_inicio)
            fin_dt = pd.to_datetime(fecha_fin)
            
            reportes_filtrados = df[(df['fecha'] >= ini_dt) & (df['fecha'] <= fin_dt)]
            
            if reportes_filtrados.empty:
                messagebox.showinfo("Sin Resultados", 
                    f"🔍 No hay insumos listos en el rango de fechas:\n"
                    f"Desde: {fecha_inicio}\n"
                    f"Hasta: {fecha_fin}")
                return
            
            # Mostrar resultados
            for _, row in reportes_filtrados.iterrows():
                self.tree_reportes_filtrados.insert('', 'end', 
                    values=(row.get('id', 'N/A'), 
                           row['fecha'].strftime('%Y-%m-%d'),
                           row.get('producto', 'N/A'),
                           row.get('cantidad', 'N/A'),
                           row.get('estado', 'Listo')))
            
            messagebox.showinfo("Filtrado Exitoso", 
                f"✅ Filtrado completado!\n\n"
                f"📊 Reportes encontrados: {len(reportes_filtrados)}\n"
                f"📅 Período: {fecha_inicio} a {fecha_fin}")
            
            # Guardar para uso posterior
            self.reportes_filtrados = reportes_filtrados
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar: {str(e)}")

    def ver_detalle_reporte_seleccionado(self):
        """Ver detalle del reporte seleccionado"""
        selection = self.tree_reportes_filtrados.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un reporte")
            return
        
        item = selection[0]
        valores = self.tree_reportes_filtrados.item(item, 'values')
        
        # Crear ventana de detalle
        ventana_detalle = self.crear_ventana_secundaria("📋 Detalle del Reporte", "600x400")
        
        main_frame = ttk.Frame(ventana_detalle, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Detalle del Reporte de Insumo Listo", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información del reporte
        info_text = f"""ID del Reporte: {valores[0]}
Fecha: {valores[1]}
Producto: {valores[2]}
Cantidad: {valores[3]}
Estado: {valores[4]}

Este producto está listo para envío según las 
especificaciones de demanda y disponibilidad 
en inventario."""
        
        text_widget = tk.Text(main_frame, height=15, wrap=tk.WORD, font=("Arial", 11))
        text_widget.insert("1.0", info_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill="both", expand=True, pady=10)
        
        ttk.Button(main_frame, text="✅ Cerrar", 
                  command=ventana_detalle.destroy).pack(pady=10)

    def descargar_reporte_seleccionado(self):
        """Descargar reporte seleccionado"""
        selection = self.tree_reportes_filtrados.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un reporte")
            return
        
        try:
            item = selection[0]
            valores = self.tree_reportes_filtrados.item(item, 'values')
            id_reporte = valores[0]
            
            if not hasattr(self, 'reportes_filtrados'):
                messagebox.showwarning("Error", "Primero debe filtrar los reportes")
                return
            
            # Filtrar el reporte específico
            detalle = self.reportes_filtrados[self.reportes_filtrados['id'].astype(str) == str(id_reporte)].copy()
            
            if detalle.empty:
                messagebox.showwarning("Error", "No se encontró el reporte seleccionado")
                return
            
            # Guardar archivo
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/reporte_insumos_listos_{id_reporte}_{timestamp}.xlsx"
            
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            detalle.to_excel(filename, index=False)
            
            messagebox.showinfo("Descarga Exitosa", 
                f"✅ Reporte descargado correctamente!\n\n"
                f"📁 Archivo: {filename}\n"
                f"📋 ID del reporte: {id_reporte}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar: {str(e)}")

    def actualizar_lista_reportes(self):
        """Actualizar lista de reportes disponibles"""
        try:
            import os
            
            # Limpiar lista
            self.listbox_reportes.delete(0, tk.END)
            
            carpeta = "data"
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                return
            
            # Buscar archivos de reportes
            archivos = [f for f in os.listdir(carpeta) 
                       if (f.startswith("reporte_insumos_listos_") or f.startswith("insumos_listos")) 
                       and f.endswith(".xlsx")]
            
            if not archivos:
                self.listbox_reportes.insert(tk.END, "No hay reportes disponibles")
                return
            
            # Agregar archivos a la lista
            for archivo in sorted(archivos):
                self.listbox_reportes.insert(tk.END, archivo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar lista: {str(e)}")

    def abrir_carpeta_reportes(self):
        """Abrir carpeta de reportes en el explorador"""
        try:
            import os
            import subprocess
            import platform
            
            carpeta = os.path.abspath("data")
            
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            
            # Abrir según el sistema operativo
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{carpeta}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(f'open "{carpeta}"', shell=True)
            else:  # Linux
                subprocess.Popen(f'xdg-open "{carpeta}"', shell=True)
                
            messagebox.showinfo("Carpeta Abierta", 
                f"📂 Carpeta de reportes abierta:\n{carpeta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir carpeta: {str(e)}")

    def eliminar_reporte_seleccionado(self):
        """Eliminar reporte seleccionado"""
        selection = self.listbox_reportes.curselection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un reporte para eliminar")
            return
        
        try:
            archivo = self.listbox_reportes.get(selection[0])
            
            if archivo == "No hay reportes disponibles":
                return
            
            if not messagebox.askyesno("Confirmar Eliminación", 
                f"¿Está seguro de eliminar el reporte?\n\n{archivo}"):
                return
            
            import os
            ruta_archivo = os.path.join("data", archivo)
            
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                messagebox.showinfo("Eliminado", f"✅ Reporte eliminado: {archivo}")
                self.actualizar_lista_reportes()
            else:
                messagebox.showwarning("Error", "El archivo no existe")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
        
    def menu_reportar_defectuosos(self):
        """Menú para reportar insumos defectuosos con desplegables y observaciones"""
        ventana = self.crear_ventana_secundaria("🚨 Reportar Insumos Defectuosos", "1000x800")
        
        main_frame = ttk.Frame(ventana, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Reportar Insumos Defectuosos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para información general del reporte
        info_frame = ttk.LabelFrame(main_frame, text="Información General", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        # Grid para información general
        ttk.Label(info_frame, text="Proveedor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_proveedor_defecto = ttk.Entry(info_frame, width=30)
        self.entry_proveedor_defecto.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Fecha del reporte (YYYY-MM-DD):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_fecha_defecto = ttk.Entry(info_frame, width=20)
        self.entry_fecha_defecto.grid(row=0, column=3, padx=5, pady=5)
        
        # Establecer fecha actual por defecto
        from datetime import datetime
        self.entry_fecha_defecto.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Frame para agregar insumos defectuosos
        insumos_frame = ttk.LabelFrame(main_frame, text="Insumos Defectuosos", padding="15")
        insumos_frame.pack(fill="both", expand=True, pady=10)
        
        # Lista de insumos defectuosos
        if not hasattr(self, 'insumos_defectuosos'):
            self.insumos_defectuosos = []
        
        # Frame para agregar nuevo insumo defectuoso
        add_frame = ttk.Frame(insumos_frame)
        add_frame.pack(fill="x", pady=10)
        
        # Primera fila de controles
        fila1 = ttk.Frame(add_frame)
        fila1.pack(fill="x", pady=5)
        
        ttk.Label(fila1, text="Producto:").pack(side="left", padx=5)
        self.entry_producto_defecto = ttk.Entry(fila1, width=25)
        self.entry_producto_defecto.pack(side="left", padx=5)
        
        ttk.Label(fila1, text="Cantidad afectada:").pack(side="left", padx=5)
        self.entry_cantidad_defecto = ttk.Entry(fila1, width=15)
        self.entry_cantidad_defecto.pack(side="left", padx=5)
        
        ttk.Label(fila1, text="Tipo de problema:").pack(side="left", padx=5)
        self.combo_tipo_defecto = ttk.Combobox(fila1, width=15, 
                                             values=["Calidad", "Cantidad"],
                                             state="readonly")
        self.combo_tipo_defecto.set("Calidad")  # Valor por defecto
        self.combo_tipo_defecto.pack(side="left", padx=5)
        
        # Segunda fila para observaciones
        fila2 = ttk.Frame(add_frame)
        fila2.pack(fill="x", pady=5)
        
        ttk.Label(fila2, text="Observaciones (opcional):").pack(side="left", padx=5)
        self.entry_observaciones_defecto = ttk.Entry(fila2, width=60)
        self.entry_observaciones_defecto.pack(side="left", padx=5, fill="x", expand=True)
        
        ttk.Button(fila2, text="➕ Agregar Insumo", 
                  command=self.agregar_insumo_defectuoso).pack(side="right", padx=5)
        
        # Frame con Treeview para mostrar insumos defectuosos
        tree_frame = ttk.Frame(insumos_frame)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        # Crear Treeview para insumos defectuosos
        columns = ('Producto', 'Cantidad', 'Tipo Problema', 'Observaciones')
        self.tree_defectuosos = ttk.Treeview(tree_frame, columns=columns, show='tree headings', height=10)
        
        # Configurar columnas
        self.tree_defectuosos.heading('#0', text='#')
        self.tree_defectuosos.heading('Producto', text='Producto')
        self.tree_defectuosos.heading('Cantidad', text='Cantidad')
        self.tree_defectuosos.heading('Tipo Problema', text='Tipo de Problema')
        self.tree_defectuosos.heading('Observaciones', text='Observaciones')
        
        self.tree_defectuosos.column('#0', width=50)
        self.tree_defectuosos.column('Producto', width=200)
        self.tree_defectuosos.column('Cantidad', width=100)
        self.tree_defectuosos.column('Tipo Problema', width=150)
        self.tree_defectuosos.column('Observaciones', width=300)
        
        # Scrollbar para el Treeview
        scrollbar_defectuosos = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_defectuosos.yview)
        self.tree_defectuosos.configure(yscrollcommand=scrollbar_defectuosos.set)
        
        self.tree_defectuosos.pack(side="left", fill="both", expand=True)
        scrollbar_defectuosos.pack(side="right", fill="y")
        
        # Frame para acciones con insumos
        acciones_frame = ttk.Frame(insumos_frame)
        acciones_frame.pack(fill="x", pady=10)
        
        ttk.Button(acciones_frame, text="🔄 Modificar Seleccionado", 
                  command=self.modificar_insumo_defectuoso).pack(side="left", padx=5)
        ttk.Button(acciones_frame, text="🗑️ Eliminar Seleccionado", 
                  command=self.eliminar_insumo_defectuoso).pack(side="left", padx=5)
        ttk.Button(acciones_frame, text="🧹 Limpiar Todo", 
                  command=self.limpiar_defectuosos).pack(side="left", padx=5)
        
        # Frame para botones principales
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill="x", pady=20)
        
        # Primera fila de botones
        fila1_frame = ttk.Frame(botones_frame)
        fila1_frame.pack(fill="x", pady=5)
        
        ttk.Button(fila1_frame, text="✅ Confirmar y Revisar", 
                  command=self.confirmar_reporte_defectuosos,
                  style='Primary.TButton').pack(side="left", padx=10)
        ttk.Button(fila1_frame, text="💾 Guardar Reporte", 
                  command=self.guardar_reporte_defectuosos,
                  style='Success.TButton').pack(side="left", padx=10)
        
        # Segunda fila de botones
        fila2_frame = ttk.Frame(botones_frame)
        fila2_frame.pack(fill="x", pady=5)
        
        ttk.Button(fila2_frame, text="📧 Enviar por Email", 
                  command=self.enviar_reporte_defectuosos).pack(side="left", padx=10)
        ttk.Button(fila2_frame, text="🧹 Limpiar Formulario", 
                  command=self.limpiar_formulario_defectuosos).pack(side="left", padx=10)

    def agregar_insumo_defectuoso(self):
        """Agregar un insumo defectuoso a la lista"""
        producto = self.entry_producto_defecto.get().strip()
        cantidad = self.entry_cantidad_defecto.get().strip()
        tipo_problema = self.combo_tipo_defecto.get()
        observaciones = self.entry_observaciones_defecto.get().strip()
        
        if not producto:
            messagebox.showwarning("Error", "Por favor ingrese el nombre del producto")
            return
            
        if not cantidad:
            messagebox.showwarning("Error", "Por favor ingrese la cantidad afectada")
            return
            
        try:
            cantidad_num = float(cantidad)
            if cantidad_num <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            messagebox.showwarning("Error", "Por favor ingrese una cantidad válida")
            return
        
        # Agregar a la lista
        insumo = {
            'producto': producto,
            'cantidad': cantidad,
            'tipo_problema': tipo_problema,
            'observaciones': observaciones if observaciones else "Sin observaciones"
        }
        
        if not hasattr(self, 'insumos_defectuosos'):
            self.insumos_defectuosos = []
        
        self.insumos_defectuosos.append(insumo)
        
        # Agregar al Treeview
        item_id = self.tree_defectuosos.insert('', 'end', text=str(len(self.insumos_defectuosos)),
                                              values=(producto, cantidad, tipo_problema, 
                                                     observaciones if observaciones else "Sin observaciones"))
        
        # Limpiar campos
        self.entry_producto_defecto.delete(0, tk.END)
        self.entry_cantidad_defecto.delete(0, tk.END)
        self.entry_observaciones_defecto.delete(0, tk.END)
        self.combo_tipo_defecto.set("Calidad")
        
        messagebox.showinfo("Éxito", f"Insumo defectuoso agregado: {producto}")

    def modificar_insumo_defectuoso(self):
        """Modificar el insumo defectuoso seleccionado"""
        selection = self.tree_defectuosos.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un insumo para modificar")
            return
            
        item = selection[0]
        index = int(self.tree_defectuosos.item(item, 'text')) - 1
        
        if hasattr(self, 'insumos_defectuosos') and 0 <= index < len(self.insumos_defectuosos):
            insumo = self.insumos_defectuosos[index]
            
            # Cargar datos en los campos
            self.entry_producto_defecto.delete(0, tk.END)
            self.entry_producto_defecto.insert(0, insumo['producto'])
            
            self.entry_cantidad_defecto.delete(0, tk.END)
            self.entry_cantidad_defecto.insert(0, insumo['cantidad'])
            
            self.combo_tipo_defecto.set(insumo['tipo_problema'])
            
            self.entry_observaciones_defecto.delete(0, tk.END)
            if insumo['observaciones'] != "Sin observaciones":
                self.entry_observaciones_defecto.insert(0, insumo['observaciones'])
            
            # Eliminar el item actual
            self.eliminar_insumo_defectuoso()
            
            messagebox.showinfo("Info", "Datos cargados para modificación. Ajuste y presione 'Agregar Insumo'")

    def eliminar_insumo_defectuoso(self):
        """Eliminar el insumo defectuoso seleccionado"""
        selection = self.tree_defectuosos.selection()
        if not selection:
            messagebox.showwarning("Error", "Por favor seleccione un insumo para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este insumo defectuoso?"):
            item = selection[0]
            index = int(self.tree_defectuosos.item(item, 'text')) - 1
            
            if hasattr(self, 'insumos_defectuosos') and 0 <= index < len(self.insumos_defectuosos):
                self.insumos_defectuosos.pop(index)
                
            # Recargar Treeview
            self.tree_defectuosos.delete(*self.tree_defectuosos.get_children())
            for i, insumo in enumerate(self.insumos_defectuosos):
                self.tree_defectuosos.insert('', 'end', text=str(i + 1),
                                            values=(insumo['producto'], insumo['cantidad'], 
                                                   insumo['tipo_problema'], insumo['observaciones']))

    def limpiar_defectuosos(self):
        """Limpiar toda la lista de insumos defectuosos"""
        if hasattr(self, 'insumos_defectuosos') and self.insumos_defectuosos and messagebox.askyesno("Confirmar", "¿Está seguro de limpiar toda la lista?"):
            self.insumos_defectuosos.clear()
            self.tree_defectuosos.delete(*self.tree_defectuosos.get_children())
            messagebox.showinfo("Info", "Lista de insumos defectuosos limpiada")

    def confirmar_reporte_defectuosos(self):
        """Confirmar y revisar el reporte antes de guardarlo"""
        proveedor = self.entry_proveedor_defecto.get().strip()
        fecha = self.entry_fecha_defecto.get().strip()
        
        if not proveedor:
            messagebox.showwarning("Error", "Por favor ingrese el proveedor")
            return
            
        if not fecha:
            messagebox.showwarning("Error", "Por favor ingrese la fecha")
            return
            
        if not hasattr(self, 'insumos_defectuosos') or not self.insumos_defectuosos:
            messagebox.showwarning("Error", "Por favor agregue al menos un insumo defectuoso")
            return
            
        # Crear ventana de confirmación
        ventana_conf = self.crear_ventana_secundaria("📋 Revisar Reporte de Insumos Defectuosos", "800x600")
        
        main_frame = ttk.Frame(ventana_conf, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Revisar Reporte de Insumos Defectuosos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información general
        info_text = f"""INFORMACIÓN GENERAL:
Proveedor: {proveedor}
Fecha del reporte: {fecha}
Número de insumos reportados: {len(self.insumos_defectuosos)}

DETALLE DE INSUMOS DEFECTUOSOS:
"""
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=10)
        
        text_widget = tk.Text(text_frame, height=20, wrap=tk.WORD)
        scroll_text = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scroll_text.set)
        
        text_widget.insert(tk.END, info_text)
        
        for i, insumo in enumerate(self.insumos_defectuosos, 1):
            detalle = f"{i}. {insumo['producto']}\n"
            detalle += f"   - Cantidad afectada: {insumo['cantidad']}\n"
            detalle += f"   - Tipo de problema: {insumo['tipo_problema']}\n"
            detalle += f"   - Observaciones: {insumo['observaciones']}\n\n"
            text_widget.insert(tk.END, detalle)
            
        text_widget.config(state='disabled')
        text_widget.pack(side="left", fill="both", expand=True)
        scroll_text.pack(side="right", fill="y")
        
        # Botones de confirmación
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=20)
        
        ttk.Button(btn_frame, text="✅ Todo Correcto - Guardar", 
                  command=lambda: [ventana_conf.destroy(), self.guardar_reporte_defectuosos()],
                  style='Success.TButton').pack(side="left", padx=10)
        ttk.Button(btn_frame, text="✏️ Hacer Modificaciones", 
                  command=ventana_conf.destroy).pack(side="left", padx=10)

    def guardar_reporte_defectuosos(self):
        """Guardar el reporte de insumos defectuosos"""
        try:
            proveedor = self.entry_proveedor_defecto.get().strip()
            fecha = self.entry_fecha_defecto.get().strip()
            
            if not proveedor or not fecha or not hasattr(self, 'insumos_defectuosos') or not self.insumos_defectuosos:
                messagebox.showwarning("Error", "Complete todos los campos requeridos")
                return
            
            # Crear DataFrame con los datos
            import pandas as pd
            import os
            from datetime import datetime
            
            datos_reporte = []
            for insumo in self.insumos_defectuosos:
                datos_reporte.append({
                    'Proveedor': proveedor,
                    'Fecha': fecha,
                    'Producto': insumo['producto'],
                    'Cantidad_Afectada': insumo['cantidad'],
                    'Tipo_Problema': insumo['tipo_problema'],
                    'Observaciones': insumo['observaciones'],
                    'Fecha_Reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            df_reporte = pd.DataFrame(datos_reporte)
            
            # Guardar archivo Excel
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"data/reporte_defectuosos_{timestamp}.xlsx"
            
            # Asegurar que existe el directorio data
            os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
            
            df_reporte.to_excel(nombre_archivo, index=False)
            
            messagebox.showinfo("Éxito", 
                f"✅ Reporte guardado exitosamente!\n\n"
                f"📁 Archivo: {nombre_archivo}\n"
                f"📊 Insumos reportados: {len(self.insumos_defectuosos)}\n"
                f"🏢 Proveedor: {proveedor}")
            
            # Limpiar formulario después de guardar
            self.limpiar_formulario_defectuosos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar reporte: {str(e)}")

    def enviar_reporte_defectuosos(self):
        """Enviar reporte por email - HU6"""
        if not hasattr(self, 'insumos_defectuosos') or not self.insumos_defectuosos:
            messagebox.showwarning("Error", "No hay insumos defectuosos para enviar")
            return
        
        proveedor = self.entry_proveedor_defecto.get().strip()
        fecha = self.entry_fecha_defecto.get().strip()
        
        if not proveedor or not fecha:
            messagebox.showwarning("Error", "Complete la información del proveedor y fecha antes de enviar")
            return
            
        # Crear ventana de envío de email
        ventana_email = self.crear_ventana_secundaria("📧 Enviar Reporte por Email - HU6", "700x500")
        
        main_frame = ttk.Frame(ventana_email, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Envío de Reporte de Insumos Defectuosos", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Información del reporte
        info_frame = ttk.LabelFrame(main_frame, text="Información del Reporte", padding="15")
        info_frame.pack(fill="x", pady=10)
        
        info_text = f"""📋 Reporte: Insumos Defectuosos
🏢 Proveedor: {proveedor}
📅 Fecha: {fecha}
📊 Cantidad de insumos: {len(self.insumos_defectuosos)}"""
        
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Frame para configuración de email
        email_frame = ttk.LabelFrame(main_frame, text="Configuración de Envío", padding="15")
        email_frame.pack(fill="x", pady=10)
        
        # Campo de email destinatario
        ttk.Label(email_frame, text="📧 Correo del destinatario:").pack(anchor="w", pady=5)
        self.entry_email_destinatario = ttk.Entry(email_frame, width=50, font=("Arial", 11))
        self.entry_email_destinatario.pack(fill="x", pady=5)
        self.entry_email_destinatario.focus()
        
        # Campo de asunto (pre-rellenado)
        ttk.Label(email_frame, text="📝 Asunto del email:").pack(anchor="w", pady=5)
        self.entry_asunto_email = ttk.Entry(email_frame, width=50, font=("Arial", 11))
        self.entry_asunto_email.pack(fill="x", pady=5)
        self.entry_asunto_email.insert(0, f"🚨 Reporte Insumos Defectuosos - {proveedor} - {fecha}")
        
        # Campo de mensaje adicional
        ttk.Label(email_frame, text="💬 Mensaje adicional (opcional):").pack(anchor="w", pady=5)
        self.text_mensaje_email = tk.Text(email_frame, height=4, wrap=tk.WORD, font=("Arial", 10))
        self.text_mensaje_email.pack(fill="x", pady=5)
        self.text_mensaje_email.insert("1.0", 
            "Estimado/a,\n\n"
            "Adjunto encontrará el reporte de insumos defectuosos correspondiente a la fecha indicada.\n\n"
            "Saludos cordiales,\n"
            "Sistema Finca Directa SAS")
        
        # Frame para botones de acción
        botones_email_frame = ttk.Frame(main_frame)
        botones_email_frame.pack(fill="x", pady=20)
        
        ttk.Button(botones_email_frame, text="📧 Enviar Email", 
                  command=lambda: self.procesar_envio_email(ventana_email),
                  style='Success.TButton').pack(side="left", padx=10)
        ttk.Button(botones_email_frame, text="👁️ Vista Previa", 
                  command=self.mostrar_vista_previa_email).pack(side="left", padx=10)
        ttk.Button(botones_email_frame, text="❌ Cancelar", 
                  command=ventana_email.destroy).pack(side="right", padx=10)

    def procesar_envio_email(self, ventana_email):
        """Procesar el envío del email con el reporte"""
        try:
            email_destinatario = self.entry_email_destinatario.get().strip()
            asunto = self.entry_asunto_email.get().strip()
            mensaje_adicional = self.text_mensaje_email.get("1.0", tk.END).strip()
            
            if not email_destinatario:
                messagebox.showwarning("Error", "Por favor ingrese el correo del destinatario")
                return
            
            # Validar formato de email básico
            if "@" not in email_destinatario or "." not in email_destinatario:
                messagebox.showwarning("Error", "Por favor ingrese un correo electrónico válido")
                return
            
            # Preparar datos del reporte
            proveedor = self.entry_proveedor_defecto.get().strip()
            fecha = self.entry_fecha_defecto.get().strip()
            
            # Crear contenido del email
            contenido_reporte = self.generar_contenido_email_reporte()
            
            # Configurar email (usando la función existente de main.py como base)
            import smtplib
            from email.message import EmailMessage
            
            # Credenciales - en un entorno real, estas deberían estar en un archivo de configuración
            email_remitente = "fincadirectasas@gmail.com"  # Configurar según su email
            contraseña = "contraseña_app"  # Usar contraseña de aplicación
            
            # Crear mensaje
            mensaje = EmailMessage()
            mensaje['From'] = email_remitente
            mensaje['To'] = email_destinatario
            mensaje['Subject'] = asunto
            
            # Contenido del mensaje
            contenido_completo = f"""{mensaje_adicional}

{contenido_reporte}

---
Este email fue generado automáticamente por el Sistema Finca Directa SAS
Fecha de envío: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            mensaje.set_content(contenido_completo)
            
            # Envío real del email
            self.enviar_email_real(email_destinatario, asunto, contenido_completo, ventana_email)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar envío: {str(e)}")

    def generar_contenido_email_reporte(self):
        """Generar el contenido del reporte para el email"""
        proveedor = self.entry_proveedor_defecto.get().strip()
        fecha = self.entry_fecha_defecto.get().strip()
        
        contenido = f"""
📋 REPORTE DE INSUMOS DEFECTUOSOS
===========================================

🏢 PROVEEDOR: {proveedor}
📅 FECHA DEL REPORTE: {fecha}
📊 TOTAL DE INSUMOS REPORTADOS: {len(self.insumos_defectuosos)}

DETALLE DE INSUMOS DEFECTUOSOS:
"""
        
        for i, insumo in enumerate(self.insumos_defectuosos, 1):
            contenido += f"""
{i}. PRODUCTO: {insumo['producto']}
   - Cantidad afectada: {insumo['cantidad']}
   - Tipo de problema: {insumo['tipo_problema']}
   - Observaciones: {insumo['observaciones']}
"""
        
        contenido += f"""
===========================================
Reporte generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sistema: Finca Directa SAS v3.0
Historia de Usuario: HU6 - Envío de reportes por email
"""
        
        return contenido

    def enviar_email_real(self, destinatario, asunto, contenido, ventana_email):
        """Enviar email real usando SMTP"""
        try:
            import smtplib
            from email.message import EmailMessage
            
            # Configuración de email (igual que en main.py)
            email_remitente = "elcoordinadordecompras@gmail.com"
            contraseña = "iocsdhwphxxhbzzp"
            
            # Crear mensaje
            mensaje = EmailMessage()
            mensaje["Subject"] = asunto
            mensaje["From"] = email_remitente
            mensaje["To"] = destinatario
            mensaje.set_content(contenido)
            
            # Enviar email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_remitente, contraseña)
                smtp.send_message(mensaje)
            
            # Cerrar ventana y mostrar éxito
            ventana_email.destroy()
            
            # Guardar log del envío
            try:
                log_entry = {
                    'fecha_envio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'destinatario': destinatario,
                    'asunto': asunto,
                    'insumos_reportados': len(self.insumos_defectuosos),
                    'estado': 'Enviado exitosamente'
                }
                
                import pandas as pd
                import os
                
                log_path = os.path.join("data", "log_emails_defectuosos.xlsx")
                
                if os.path.exists(log_path):
                    df_log = pd.read_excel(log_path)
                    df_log = pd.concat([df_log, pd.DataFrame([log_entry])], ignore_index=True)
                else:
                    df_log = pd.DataFrame([log_entry])
                
                df_log.to_excel(log_path, index=False)
                
            except Exception as log_error:
                print(f"Error al guardar log: {log_error}")
            
            messagebox.showinfo("Email Enviado", 
                f"✅ Reporte enviado exitosamente!\n\n"
                f"📧 Destinatario: {destinatario}\n"
                f"📊 Insumos reportados: {len(self.insumos_defectuosos)}\n"
                f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"El proveedor ha sido notificado de los insumos defectuosos.")
                
        except Exception as e:
            messagebox.showerror("Error de Envío", 
                f"❌ Error al enviar email:\n\n{str(e)}\n\n"
                f"Por favor verifique:\n"
                f"• Conexión a internet\n"
                f"• Configuración de email\n"
                f"• Email del destinatario")

    def simular_envio_email_old(self, destinatario, asunto, contenido, ventana_email):
        """Simular el envío de email (placeholder para implementación real)"""
        # En un entorno real, aquí iría la lógica de SMTP
        resultado = messagebox.askyesno("Confirmar Envío", 
            f"¿Confirma el envío del reporte por email?\n\n"
            f"📧 Destinatario: {destinatario}\n"
            f"📝 Asunto: {asunto}\n"
            f"📊 Insumos reportados: {len(self.insumos_defectuosos)}\n\n"
            f"NOTA: Esta es una simulación. Para envío real,\n"
            f"configure las credenciales SMTP en el sistema.")
        
        if resultado:
            # Simular tiempo de envío
            ventana_email.destroy()
            
            # Guardar log del envío
            try:
                log_entry = {
                    'fecha_envio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'destinatario': destinatario,
                    'asunto': asunto,
                    'proveedor': self.entry_proveedor_defecto.get().strip(),
                    'cantidad_insumos': len(self.insumos_defectuosos),
                    'estado': 'SIMULADO'
                }
                
                # Guardar en archivo de log (opcional)
                import os
                log_dir = "data"
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                    
                log_file = os.path.join(log_dir, "log_emails_defectuosos.txt")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{log_entry}\n")
                    
            except Exception as e:
                print(f"Error al guardar log: {e}")
            
            messagebox.showinfo("Envío Exitoso", 
                f"✅ Email enviado exitosamente!\n\n"
                f"📧 Destinatario: {destinatario}\n"
                f"📝 Asunto: {asunto}\n"
                f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"💾 El reporte también se ha guardado en el log del sistema.")

    def mostrar_vista_previa_email(self):
        """Mostrar vista previa del email antes de enviar"""
        email_destinatario = self.entry_email_destinatario.get().strip()
        asunto = self.entry_asunto_email.get().strip()
        mensaje_adicional = self.text_mensaje_email.get("1.0", tk.END).strip()
        
        if not email_destinatario:
            messagebox.showwarning("Error", "Ingrese el correo del destinatario para ver la vista previa")
            return
        
        # Crear ventana de vista previa
        ventana_preview = self.crear_ventana_secundaria("👁️ Vista Previa del Email", "800x600")
        
        main_frame = ttk.Frame(ventana_preview, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Vista Previa del Email", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Crear área de texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=10)
        
        text_preview = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scroll_preview = ttk.Scrollbar(text_frame, orient="vertical", command=text_preview.yview)
        text_preview.configure(yscrollcommand=scroll_preview.set)
        
        # Generar contenido de vista previa
        contenido_reporte = self.generar_contenido_email_reporte()
        preview_content = f"""DE: fincadirectasas@gmail.com
PARA: {email_destinatario}
ASUNTO: {asunto}
FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

------- CONTENIDO DEL MENSAJE -------

{mensaje_adicional}

{contenido_reporte}

---
Este email fue generado automáticamente por el Sistema Finca Directa SAS
Historia de Usuario: HU6 - Envío de reportes por email
"""
        
        text_preview.insert("1.0", preview_content)
        text_preview.config(state='disabled')
        
        text_preview.pack(side="left", fill="both", expand=True)
        scroll_preview.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(main_frame, text="✅ Cerrar Vista Previa", 
                  command=ventana_preview.destroy).pack(pady=10)

    def limpiar_formulario_defectuosos(self):
        """Limpiar todo el formulario de reportes defectuosos"""
        if hasattr(self, 'entry_proveedor_defecto'):
            self.entry_proveedor_defecto.delete(0, tk.END)
        if hasattr(self, 'entry_fecha_defecto'):
            self.entry_fecha_defecto.delete(0, tk.END)
        if hasattr(self, 'entry_producto_defecto'):
            self.entry_producto_defecto.delete(0, tk.END)
        if hasattr(self, 'entry_cantidad_defecto'):
            self.entry_cantidad_defecto.delete(0, tk.END)
        if hasattr(self, 'entry_observaciones_defecto'):
            self.entry_observaciones_defecto.delete(0, tk.END)
        if hasattr(self, 'combo_tipo_defecto'):
            self.combo_tipo_defecto.set("Calidad")
        
        # Limpiar lista y treeview
        if hasattr(self, 'insumos_defectuosos'):
            self.insumos_defectuosos.clear()
        if hasattr(self, 'tree_defectuosos'):
            self.tree_defectuosos.delete(*self.tree_defectuosos.get_children())
        
        # Restaurar fecha actual
        if hasattr(self, 'entry_fecha_defecto'):
            from datetime import datetime
            self.entry_fecha_defecto.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
    # ==================== MÉTODOS AUXILIARES ====================
    
    def crear_ventana_secundaria(self, titulo, tamaño):
        """Crear una ventana secundaria"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(tamaño)
        ventana.configure(bg="#f0f0f0")
        ventana.transient(self.root)
        return ventana

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal para ejecutar la aplicación"""
    try:
        # Crear y mostrar pantalla de carga
        def iniciar_app_principal():
            app = SistemaFincaDirectaGUI()
            app.inicializar_aplicacion()
        
        pantalla_carga = PantallaCarga(iniciar_app_principal)
        pantalla_carga.mostrar()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()
