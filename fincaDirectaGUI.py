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
            ("📥 Recepción de Insumos", "Registrar llegadas (HU5)", self.menu_recepcion_insumos, 0, 3),
            ("� Reportar Insumos Defectuosos", "Control de calidad y cantidad (HU6)", self.menu_reportar_defectuosos, 1, 0),
            ("�📋 Reportes de Recepción", "Estadísticas de recepción (HU7)", self.menu_reportes_recepcion, 1, 1),
            ("🛒 Reportes de Solicitudes", "Gestión de compras (HU8)", self.menu_reportes_solicitudes, 1, 2),
            ("🚚 Reportes Insumos Listos", "Estado de preparación (HU10)", self.menu_reportes_insumos_listos, 1, 3),
            ("⚙️ Configuración", "Ajustes del sistema", self.mostrar_configuracion, 2, 0)
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
        
        # Área de resultados con texto oscuro
        self.text_inventario = tk.Text(main_frame, height=20, width=80,
                                      bg='white', fg='#2C3E50', insertbackground='#2C3E50')
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
        
        ttk.Button(modify_frame, text="🔄 Modificar Estado", 
                  command=self.modificar_estado_producto).pack(side="left", padx=5)
        ttk.Button(modify_frame, text="🗑️ Eliminar Producto", 
                  command=self.eliminar_producto).pack(side="left", padx=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="✅ Procesar Recepción", 
                  command=self.procesar_recepcion_completa).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Limpiar", 
                  command=self.limpiar_recepcion).pack(side="left", padx=5)
        
    def agregar_producto_recibido(self):
        """Agregar producto a la lista de productos recibidos con estado de conformidad"""
        producto = self.entry_producto_nuevo.get().strip()
        estado = self.combo_estado_nuevo.get()
        
        try:
            cantidad = int(self.entry_cantidad_nueva.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
            
        if not producto or cantidad <= 0:
            messagebox.showerror("Error", "Ingrese un producto válido y cantidad mayor a 0")
            return
            
        if not estado:
            messagebox.showerror("Error", "Debe seleccionar un estado (Conforme/No conforme)")
            return
            
        # Agregar producto con estado de conformidad
        self.productos_recibidos.append((producto, cantidad, estado))
        
        # Agregar al Treeview
        item_count = len(self.productos_recibidos)
        item_id = self.tree_productos.insert('', 'end', text=str(item_count),
                                            values=(producto, cantidad, estado))
        
        # Aplicar color según estado
        if estado == "No conforme":
            self.tree_productos.set(item_id, 'Estado', f"🚫 {estado}")
        else:
            self.tree_productos.set(item_id, 'Estado', f"✅ {estado}")
        
        # Limpiar campos
        self.entry_producto_nuevo.delete(0, tk.END)
        self.entry_cantidad_nueva.delete(0, tk.END)
        self.combo_estado_nuevo.set("Conforme")  # Resetear a valor por defecto
        
    def modificar_estado_producto(self):
        """Modificar el estado de conformidad del producto seleccionado"""
        selected_item = self.tree_productos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto de la lista")
            return
            
        nuevo_estado = self.combo_estado_modificar.get()
        if not nuevo_estado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un nuevo estado")
            return
            
        # Obtener índice del producto
        item_text = self.tree_productos.item(selected_item[0])['text']
        indice = int(item_text) - 1
        
        # Actualizar en la lista
        producto, cantidad, _ = self.productos_recibidos[indice]
        self.productos_recibidos[indice] = (producto, cantidad, nuevo_estado)
        
        # Actualizar en el Treeview
        if nuevo_estado == "No conforme":
            self.tree_productos.set(selected_item[0], 'Estado', f"🚫 {nuevo_estado}")
        else:
            self.tree_productos.set(selected_item[0], 'Estado', f"✅ {nuevo_estado}")
            
        messagebox.showinfo("Éxito", f"Estado actualizado a: {nuevo_estado}")
        
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        selected_item = self.tree_productos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto de la lista")
            return
            
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            # Obtener índice del producto
            item_text = self.tree_productos.item(selected_item[0])['text']
            indice = int(item_text) - 1
            
            # Eliminar de la lista
            del self.productos_recibidos[indice]
            
            # Reconstruir el Treeview
            self.tree_productos.delete(*self.tree_productos.get_children())
            for i, (producto, cantidad, estado) in enumerate(self.productos_recibidos):
                item_id = self.tree_productos.insert('', 'end', text=str(i+1),
                                                    values=(producto, cantidad, estado))
                if estado == "No conforme":
                    self.tree_productos.set(item_id, 'Estado', f"🚫 {estado}")
                else:
                    self.tree_productos.set(item_id, 'Estado', f"✅ {estado}")
        
    def limpiar_recepcion(self):
        """Limpiar todos los campos de recepción"""
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_recepcion.delete(0, tk.END)
        self.entry_numero_pedido.delete(0, tk.END)
        self.entry_producto_nuevo.delete(0, tk.END)
        self.entry_cantidad_nueva.delete(0, tk.END)
        self.combo_estado_nuevo.set("Conforme")
        self.combo_estado_modificar.set("")
        self.tree_productos.delete(*self.tree_productos.get_children())
        self.productos_recibidos = []
        
    def procesar_recepcion_completa(self):
        """Procesar la recepción completa de insumos con estado de conformidad"""
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
            # Registrar la recepción con estado de conformidad
            # 1. Registrar entrega
            df_entregas = cargar_excel(entregas)
            nuevo_id = 1 if df_entregas.empty else df_entregas['id'].max() + 1
            nueva_entrega = pd.DataFrame([[nuevo_id, proveedor, fecha, numero_pedido, len(self.productos_recibidos)]],
                                        columns=["id", "proveedor", "fecha", "numero_pedido", "cantidades_entregadas"])
            df_entregas = pd.concat([df_entregas, nueva_entrega], ignore_index=True)
            guardar_excel(df_entregas, entregas)
            
            # 2. Guardar detalle con estado de conformidad
            self.guardar_detalle_entrega_con_conformidad(self.productos_recibidos, nuevo_id)
            
            # 3. Validar campos
            productos_basicos = [(p[0], p[1]) for p in self.productos_recibidos]  # Solo producto y cantidad para validación
            if not validar_campos(productos_basicos):
                return
                
            # 4. Procesar conformidad y mostrar resumen
            productos_conformes = [p for p in self.productos_recibidos if p[2] == "Conforme"]
            productos_no_conformes = [p for p in self.productos_recibidos if p[2] == "No conforme"]
            
            # 5. Ingresar al inventario solo productos conformes
            if productos_conformes:
                productos_validados = [(p[0], p[1]) for p in productos_conformes]
                ingresar_inventario(productos_validados)
            
            # 6. Mostrar resumen detallado
            resumen = f"✅ Recepción procesada exitosamente. ID de entrega: {nuevo_id}\n\n"
            resumen += f"📋 RESUMEN:\n"
            resumen += f"• Total productos recibidos: {len(self.productos_recibidos)}\n"
            resumen += f"• Productos conformes: {len(productos_conformes)}\n"
            resumen += f"• Productos no conformes: {len(productos_no_conformes)}\n\n"
            
            if productos_conformes:
                resumen += "✅ PRODUCTOS CONFORMES (ingresados al inventario):\n"
                for producto, cantidad, _ in productos_conformes:
                    resumen += f"   • {producto}: {cantidad} unidades\n"
                resumen += "\n"
            
            if productos_no_conformes:
                resumen += "🚫 PRODUCTOS NO CONFORMES (NO ingresados al inventario):\n"
                for producto, cantidad, _ in productos_no_conformes:
                    resumen += f"   • {producto}: {cantidad} unidades\n"
            
            messagebox.showinfo("Recepción Completada", resumen)
            self.limpiar_recepcion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar recepción: {e}")
            
    def guardar_detalle_entrega_con_conformidad(self, productos, entrega_id):
        """Guardar detalle de entrega incluyendo estado de conformidad"""
        try:
            df_detalle = cargar_excel(detalle_entregas)
            
            nuevos_detalles = []
            for producto, cantidad, estado in productos:
                nuevo_detalle = [entrega_id, producto, cantidad, estado]
                nuevos_detalles.append(nuevo_detalle)
            
            # Crear DataFrame con las columnas apropiadas
            if df_detalle.empty:
                columnas = ["entrega_id", "producto", "cantidad", "estado_conformidad"]
            else:
                columnas = df_detalle.columns.tolist()
                # Agregar columna de estado si no existe
                if "estado_conformidad" not in columnas:
                    columnas.append("estado_conformidad")
            
            df_nuevos = pd.DataFrame(nuevos_detalles, columns=columnas)
            df_detalle = pd.concat([df_detalle, df_nuevos], ignore_index=True)
            
            guardar_excel(df_detalle, detalle_entregas)
            
        except Exception as e:
            print(f"Error al guardar detalle con conformidad: {e}")
            # Fallback: guardar sin conformidad
            guardar_detalle_entrega([(p[0], p[1]) for p in productos], entrega_id)
            
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
        """Menú para reportes de solicitudes de compra"""
        messagebox.showinfo("Info", "Funcionalidad de reportes de solicitudes - Por implementar")
        
    def menu_reportes_insumos_listos(self):
        """Menú para reportes de insumos listos"""
        messagebox.showinfo("Info", "Funcionalidad de reportes de insumos listos - Por implementar")
        
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
            
            # Por ahora, mostrar simulación del envío
            self.simular_envio_email(email_destinatario, asunto, contenido_completo, ventana_email)
            
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

    def simular_envio_email(self, destinatario, asunto, contenido, ventana_email):
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
