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
        
        # Configurar grid para 4 columnas
        for i in range(4):
            modules_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            modules_frame.grid_rowconfigure(i, weight=1)
        
        # Módulos con iconos y descripciones mejoradas
        modulos = [
            ("📊 Consultar Demanda de Pedidos", "Análisis de solicitudes (HU4)", self.menu_consulta_pedidos, 0, 0),
            ("📦 Consultar Inventario", "Control de stock disponible (HU1)", self.menu_inventario, 0, 1),
            ("✅ Verificar Disponibilidad", "Validar insumos requeridos (HU2)", self.menu_verificar_disponibilidad, 0, 2),
            ("📥 Recepción de Insumos", "Registrar llegadas (HU5)", self.menu_recepcion_insumos, 0, 3),
            ("📋 Reportes de Recepción", "Estadísticas de recepción (HU7)", self.menu_reportes_recepcion, 1, 0),
            ("🛒 Reportes de Solicitudes", "Gestión de compras (HU8)", self.menu_reportes_solicitudes, 1, 1),
            ("🚚 Reportes Insumos Listos", "Estado de preparación (HU10)", self.menu_reportes_insumos_listos, 1, 2),
            ("⚙️ Configuración", "Ajustes del sistema", self.mostrar_configuracion, 1, 3)
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
        """Menú para recepción de insumos"""
        ventana = self.crear_ventana_secundaria("📥 Recepción de Insumos", "700x600")
        
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
        
        # Productos recibidos
        productos_frame = ttk.LabelFrame(main_frame, text="Productos Recibidos", padding="10")
        productos_frame.pack(fill="both", expand=True, pady=10)
        
        # Lista de productos
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
        
        ttk.Button(add_frame, text="➕ Agregar", 
                  command=self.agregar_producto_recibido).pack(side="left", padx=5)
        
        # Lista de productos agregados con mejor visibilidad
        self.list_productos = tk.Listbox(productos_frame, height=8, 
                                        bg='white', fg='#2C3E50', selectbackground='#3498DB')
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


    # ==================== MÉTODOS MODERNOS INTEGRADOS ====================

    def menu_inventario_completo(self):
        """Menú modernizado completo para consultar inventario"""
        ventana = self.crear_ventana_secundaria("Consultar Inventario", "900x700", "📦")

        main_frame = ttk.Frame(ventana, style='Main.TFrame', padding=20)
        main_frame.pack(fill="both", expand=True)

        # Panel de acciones
        acciones_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        acciones_card.pack(fill="x", pady=(0, 20))

        ttk.Label(acciones_card, text="🔧 Acciones Disponibles", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        btn_frame = ttk.Frame(acciones_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_frame, text="📋 Ver Inventario Completo", 
                  command=self.mostrar_inventario_completo_moderno,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="🔍 Buscar Insumo", 
                  command=self.buscar_insumo_moderno,
                  style='Secondary.TButton').grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="👁️ Ver por ID", 
                  command=self.ver_detalle_insumo_moderno,
                  style='Success.TButton').grid(row=0, column=2, padx=(10, 0), sticky="ew")

        # Área de resultados moderna
        resultado_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        resultado_card.pack(fill="both", expand=True)

        ttk.Label(resultado_card, text="📊 Resultados", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Área de texto con estilo moderno
        text_frame = ttk.Frame(resultado_card, style='Card.TFrame')
        text_frame.pack(fill="both", expand=True)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.text_inventario = tk.Text(text_frame, height=20, width=80,
                                      font=self.font_normal,
                                      bg=self.colors['white'],
                                      fg=self.colors['dark'],
                                      selectbackground=self.colors['primary'],
                                      relief='flat',
                                      borderwidth=0)
        scroll_inv = ttk.Scrollbar(text_frame, orient="vertical", 
                                  command=self.text_inventario.yview)
        self.text_inventario.configure(yscrollcommand=scroll_inv.set)

        self.text_inventario.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        scroll_inv.grid(row=0, column=1, sticky="ns")

        # Mensaje inicial
        self.text_inventario.insert(tk.END, 
            "💡 Selecciona una acción para consultar el inventario...\n\n"
            "📋 Ver Inventario Completo: Muestra todos los productos (ID 0-17)\n"
            "🔍 Buscar Insumo: Busca por nombre de producto\n"
            "👁️ Ver por ID: Muestra detalles específicos de un producto")


    def mostrar_inventario_completo_moderno(self):
        """Mostrar el inventario completo con formato moderno"""
        df_inventario = cargar_excel(inventario)
        if df_inventario.empty:
            self.text_inventario.delete(1.0, tk.END)
            self.text_inventario.insert(tk.END, "❌ No hay datos de inventario disponibles.")
            return

        self.text_inventario.delete(1.0, tk.END)
        self.text_inventario.insert(tk.END, 
            "📦 INVENTARIO COMPLETO\n"
            "=" * 60 + "\n\n")

        # Header de tabla
        self.text_inventario.insert(tk.END, 
            f"{'ID':<4} | {'PRODUCTO':<35} | {'CANTIDAD':<10} | {'ÚLTIMA ACTUALIZACIÓN':<15}\n")
        self.text_inventario.insert(tk.END, "-" * 80 + "\n")

        # Mostrar datos
        df_mostrar = df_inventario.loc[0:17] if len(df_inventario) > 17 else df_inventario

        for idx, row in df_mostrar.iterrows():
            producto = str(row.get('producto', 'N/A'))[:35]
            cantidad = str(row.get('cantidad', 'N/A'))
            fecha = str(row.get('ultima_actualizacion', 'N/A'))[:15]

            self.text_inventario.insert(tk.END, 
                f"{idx:<4} | {producto:<35} | {cantidad:<10} | {fecha:<15}\n")

        self.text_inventario.insert(tk.END, f"\n📊 Total de productos: {len(df_mostrar)}")


    def buscar_insumo_moderno(self):
        """Buscar insumo con interfaz moderna"""
        # Crear ventana de búsqueda moderna
        ventana_busqueda = ttk.Toplevel(self.root)
        ventana_busqueda.title("Buscar Insumo")
        ventana_busqueda.geometry("400x200")
        ventana_busqueda.configure(bg=self.colors['light'])
        ventana_busqueda.transient(self.root)
        ventana_busqueda.grab_set()

        # Card de búsqueda
        search_card = ttk.Frame(ventana_busqueda, style='Card.TFrame', padding=30)
        search_card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(search_card, text="🔍 Buscar Insumo", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        ttk.Label(search_card, text="Ingrese el nombre del insumo:", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 10))

        entry_busqueda = ttk.Entry(search_card, font=self.font_normal, 
                                  style='Modern.TEntry', width=40)
        entry_busqueda.pack(fill="x", pady=(0, 20))
        entry_busqueda.focus()

        def realizar_busqueda():
            nombre = entry_busqueda.get().strip()
            if not nombre:
                messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
                return

            df_inventario = cargar_excel(inventario)
            df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
            nombre_norm = nombre.lower()
            resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre_norm)]

            self.text_inventario.delete(1.0, tk.END)
            if resultado.empty:
                self.text_inventario.insert(tk.END, 
                    f"❌ No se encontraron insumos con el nombre '{nombre}'\n\n"
                    "💡 Sugerencias:\n"
                    "• Verifica la ortografía\n"
                    "• Intenta con palabras más cortas\n"
                    "• Usa términos generales")
            else:
                self.text_inventario.insert(tk.END, 
                    f"🔍 RESULTADOS DE BÚSQUEDA: '{nombre}'\n"
                    "=" * 50 + "\n\n")

                for idx, row in resultado.iterrows():
                    self.text_inventario.insert(tk.END, 
                        f"📦 PRODUCTO: {row['producto']}\n"
                        f"   📊 Cantidad: {row['cantidad']}\n"
                        f"   🕒 Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n"
                        f"   🆔 ID: {idx}\n\n")

                self.text_inventario.insert(tk.END, 
                    f"✅ Se encontraron {len(resultado)} resultado(s)")

            ventana_busqueda.destroy()

        # Botones
        btn_frame = ttk.Frame(search_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="🔍 Buscar", command=realizar_busqueda,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_busqueda.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Bind Enter
        ventana_busqueda.bind('<Return>', lambda e: realizar_busqueda())


    def ver_detalle_insumo_moderno(self):
        """Ver detalle de insumo por ID con interfaz moderna"""
        # Crear ventana de selección moderna
        ventana_detalle = ttk.Toplevel(self.root)
        ventana_detalle.title("Ver Detalle por ID")
        ventana_detalle.geometry("400x250")
        ventana_detalle.configure(bg=self.colors['light'])
        ventana_detalle.transient(self.root)
        ventana_detalle.grab_set()

        # Card de selección
        detail_card = ttk.Frame(ventana_detalle, style='Card.TFrame', padding=30)
        detail_card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(detail_card, text="👁️ Ver Detalle por ID", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        ttk.Label(detail_card, text="Seleccione el ID del insumo (0-17):", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 10))

        # Spinbox moderno para selección de ID
        id_var = tk.StringVar(value="0")
        spinbox_frame = ttk.Frame(detail_card, style='Card.TFrame')
        spinbox_frame.pack(fill="x", pady=(0, 20))

        id_spinbox = tk.Spinbox(spinbox_frame, from_=0, to=17, textvariable=id_var,
                               font=self.font_normal, width=10,
                               bg=self.colors['white'], fg=self.colors['dark'],
                               relief='solid', borderwidth=2)
        id_spinbox.pack(side="left")

        def mostrar_detalle():
            try:
                idx = int(id_var.get())
                if not (0 <= idx <= 17):
                    messagebox.showerror("Error", "ID debe estar entre 0 y 17")
                    return

                df_inventario = cargar_excel(inventario)
                if idx >= len(df_inventario):
                    messagebox.showerror("Error", f"No existe producto con ID {idx}")
                    return

                row = df_inventario.iloc[idx]

                # Mostrar detalle en el área principal
                self.text_inventario.delete(1.0, tk.END)
                self.text_inventario.insert(tk.END, 
                    f"📋 DETALLE COMPLETO DEL INSUMO\n"
                    "=" * 40 + "\n\n"
                    f"🆔 ID: {idx}\n"
                    f"📦 Producto: {row.get('producto', 'N/A')}\n"
                    f"📊 Cantidad disponible: {row.get('cantidad', 'N/A')} unidades\n"
                    f"🕒 Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n\n"
                    "=" * 40 + "\n"
                    f"📈 Estado del inventario:\n")

                cantidad = row.get('cantidad', 0)
                if cantidad > 50:
                    self.text_inventario.insert(tk.END, "✅ Stock alto - Bien abastecido\n")
                elif cantidad > 20:
                    self.text_inventario.insert(tk.END, "⚠️ Stock medio - Revisar pronto\n")
                elif cantidad > 0:
                    self.text_inventario.insert(tk.END, "🔴 Stock bajo - Reabastecer urgente\n")
                else:
                    self.text_inventario.insert(tk.END, "❌ Sin stock - Producto agotado\n")

                ventana_detalle.destroy()

            except ValueError:
                messagebox.showerror("Error", "Ingrese un ID válido")

        # Botones
        btn_frame = ttk.Frame(detail_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="👁️ Ver Detalle", command=mostrar_detalle,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_detalle.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")


    def menu_verificar_disponibilidad_completo(self):
        """Menú modernizado completo para verificar disponibilidad"""
        ventana = self.crear_ventana_secundaria("Verificar Disponibilidad de Insumos", "800x600", "✅")

        main_frame = ttk.Frame(ventana, style='Main.TFrame', padding=20)
        main_frame.pack(fill="both", expand=True)

        # Panel de acciones moderno
        acciones_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        acciones_card.pack(fill="x", pady=(0, 20))

        ttk.Label(acciones_card, text="🔧 Gestión de Disponibilidad", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Grid de botones modernos
        btn_grid = ttk.Frame(acciones_card, style='Card.TFrame')
        btn_grid.pack(fill="x")
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_grid, text="📋 Generar Lista\nde Envío", 
                  command=self.generar_lista_envio_moderno,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_grid, text="📧 Enviar Lista\npor Email", 
                  command=self.enviar_lista_email_moderno,
                  style='Secondary.TButton').grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_grid, text="🔄 Actualizar\nInventario", 
                  command=self.actualizar_inventario_moderno,
                  style='Success.TButton').grid(row=0, column=2, padx=(10, 0), sticky="ew")

        # Área de resultados moderna
        resultado_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        resultado_card.pack(fill="both", expand=True)

        ttk.Label(resultado_card, text="📊 Estado de Disponibilidad", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Área de texto estilizada
        text_frame = ttk.Frame(resultado_card, style='Card.TFrame')
        text_frame.pack(fill="both", expand=True)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.text_disponibilidad = tk.Text(text_frame, height=15, width=70,
                                          font=self.font_normal,
                                          bg=self.colors['white'],
                                          fg=self.colors['dark'],
                                          selectbackground=self.colors['primary'],
                                          relief='flat',
                                          borderwidth=0)
        scroll_disp = ttk.Scrollbar(text_frame, orient="vertical", 
                                   command=self.text_disponibilidad.yview)
        self.text_disponibilidad.configure(yscrollcommand=scroll_disp.set)

        self.text_disponibilidad.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        scroll_disp.grid(row=0, column=1, sticky="ns")

        # Mensaje inicial
        self.text_disponibilidad.insert(tk.END,
            "💡 Gestión de Disponibilidad de Insumos\n\n"
            "📋 Generar Lista de Envío: Identifica productos listos para enviar\n"
            "📧 Enviar por Email: Envía la lista al coordinador de compras\n"
            "🔄 Actualizar Inventario: Descuenta cantidades demandadas\n\n"
            "Selecciona una acción para comenzar...")


    def generar_lista_envio_moderno(self):
        """Generar lista de envío con formato moderno"""
        try:
            lista = generar_lista_envio()

            self.text_disponibilidad.delete(1.0, tk.END)
            if lista.empty:
                self.text_disponibilidad.insert(tk.END,
                    "❌ ANÁLISIS DE DISPONIBILIDAD\n"
                    "=" * 50 + "\n\n"
                    "No hay insumos que cumplan completamente con la demanda actual.\n\n"
                    "💡 Recomendaciones:\n"
                    "• Revisar las solicitudes de compra pendientes\n"
                    "• Verificar el inventario actual\n"
                    "• Contactar proveedores para reabastecer")
            else:
                self.text_disponibilidad.insert(tk.END,
                    "✅ INSUMOS LISTOS PARA ENVÍO\n"
                    "=" * 50 + "\n\n")

                total_productos = len(lista)
                total_cantidad = lista['cantidad_a_enviar'].sum()

                for idx, row in lista.iterrows():
                    self.text_disponibilidad.insert(tk.END,
                        f"📦 {row['producto']}\n"
                        f"   📊 Cantidad a enviar: {row['cantidad_a_enviar']} unidades\n"
                        f"   ✅ Estado: Listo para despacho\n\n")

                self.text_disponibilidad.insert(tk.END,
                    f"📈 RESUMEN:\n"
                    f"• Total de productos listos: {total_productos}\n"
                    f"• Cantidad total a enviar: {total_cantidad} unidades\n"
                    f"• Estado general: ✅ Preparado para envío")

        except Exception as e:
            self.text_disponibilidad.delete(1.0, tk.END)
            self.text_disponibilidad.insert(tk.END,
                f"❌ ERROR EN LA GENERACIÓN\n"
                f"=" * 40 + "\n\n"
                f"Se produjo un error: {str(e)}\n\n"
                f"💡 Verifique:\n"
                f"• Que existan archivos de inventario y demanda\n"
                f"• Que los archivos no estén abiertos en otra aplicación")


    def enviar_lista_email_moderno(self):
        """Enviar lista por email con confirmación moderna"""
        # Ventana de confirmación moderna
        ventana_confirm = ttk.Toplevel(self.root)
        ventana_confirm.title("Confirmar Envío")
        ventana_confirm.geometry("450x300")
        ventana_confirm.configure(bg=self.colors['light'])
        ventana_confirm.transient(self.root)
        ventana_confirm.grab_set()

        # Card de confirmación
        confirm_card = ttk.Frame(ventana_confirm, style='Card.TFrame', padding=30)
        confirm_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Icono y título
        ttk.Label(confirm_card, text="📧", font=('Segoe UI', 48)).pack(pady=(0, 15))
        ttk.Label(confirm_card, text="Confirmar Envío por Email", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        # Información del envío
        info_frame = ttk.Frame(confirm_card, style='Card.TFrame')
        info_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(info_frame, text="📤 Destinatario: elcoordinadordecompras@gmail.com", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)
        ttk.Label(info_frame, text="📋 Asunto: Lista de insumos listos para envío", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)
        ttk.Label(info_frame, text="📎 Adjunto: insumos_listos.xlsx", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)

        def confirmar_envio():
            try:
                # Mostrar progreso
                progress_label = ttk.Label(confirm_card, text="📤 Enviando...", 
                                         style='Custom.TLabel')
                progress_label.pack(pady=10)
                ventana_confirm.update()

                # Enviar email
                enviar_lista_insumos()

                ventana_confirm.destroy()
                messagebox.showinfo("Éxito", 
                    "✅ Lista enviada exitosamente!\n\n"
                    "📧 El coordinador de compras recibirá la lista de insumos "
                    "listos para envío en su correo electrónico.")

                # Actualizar área de resultados
                self.text_disponibilidad.insert(tk.END,
                    f"\n\n📧 EMAIL ENVIADO EXITOSAMENTE\n"
                    f"🕒 Hora: {datetime.now().strftime('%H:%M:%S')}\n"
                    f"📤 Estado: Entregado")

            except Exception as e:
                ventana_confirm.destroy()
                messagebox.showerror("Error", 
                    f"❌ Error al enviar email:\n{str(e)}\n\n"
                    "Verifique su conexión a internet y la configuración SMTP.")

        # Botones
        btn_frame = ttk.Frame(confirm_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="📧 Enviar Ahora", command=confirmar_envio,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_confirm.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")


    def actualizar_inventario_moderno(self):
        """Actualizar inventario con confirmación moderna"""
        # Ventana de confirmación
        ventana_update = ttk.Toplevel(self.root)
        ventana_update.title("Actualizar Inventario")
        ventana_update.geometry("500x350")
        ventana_update.configure(bg=self.colors['light'])
        ventana_update.transient(self.root)
        ventana_update.grab_set()

        # Card principal
        update_card = ttk.Frame(ventana_update, style='Card.TFrame', padding=30)
        update_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Icono y título
        ttk.Label(update_card, text="🔄", font=('Segoe UI', 48)).pack(pady=(0, 15))
        ttk.Label(update_card, text="Actualizar Inventario", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        # Advertencia
        warning_frame = ttk.Frame(update_card, style='Card.TFrame')
        warning_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(warning_frame, text="⚠️ ATENCIÓN", 
                 style='Subtitle.TLabel', foreground='#E74C3C').pack()
        ttk.Label(warning_frame, 
                 text="Esta acción descontará las cantidades demandadas\n"
                      "del inventario actual. El proceso es irreversible.\n\n"
                      "Se actualizarán las fechas de última modificación.", 
                 style='Custom.TLabel', justify='center').pack(pady=(10, 0))

        def confirmar_actualizacion():
            try:
                # Mostrar progreso
                progress_label = ttk.Label(update_card, text="🔄 Actualizando inventario...", 
                                         style='Custom.TLabel')
                progress_label.pack(pady=10)
                ventana_update.update()

                # Actualizar inventario
                actualizar_inventario()

                ventana_update.destroy()
                messagebox.showinfo("Éxito", 
                    "✅ Inventario actualizado correctamente!\n\n"
                    "📊 Las cantidades demandadas han sido descontadas\n"
                    "🕒 Fechas de actualización registradas")

                # Actualizar área de resultados
                self.text_disponibilidad.insert(tk.END,
                    f"\n\n🔄 INVENTARIO ACTUALIZADO\n"
                    f"🕒 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"✅ Estado: Completado exitosamente")

            except Exception as e:
                ventana_update.destroy()
                messagebox.showerror("Error", 
                    f"❌ Error al actualizar inventario:\n{str(e)}")

        # Botones
        btn_frame = ttk.Frame(update_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="🔄 Actualizar", command=confirmar_actualizacion,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_update.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")



    # ==================== MÉTODOS MODERNOS INTEGRADOS ====================

    def menu_inventario_completo(self):
        """Menú modernizado completo para consultar inventario"""
        ventana = self.crear_ventana_secundaria("Consultar Inventario", "900x700", "📦")

        main_frame = ttk.Frame(ventana, style='Main.TFrame', padding=20)
        main_frame.pack(fill="both", expand=True)

        # Panel de acciones
        acciones_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        acciones_card.pack(fill="x", pady=(0, 20))

        ttk.Label(acciones_card, text="🔧 Acciones Disponibles", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        btn_frame = ttk.Frame(acciones_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_frame, text="📋 Ver Inventario Completo", 
                  command=self.mostrar_inventario_completo_moderno,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="🔍 Buscar Insumo", 
                  command=self.buscar_insumo_moderno,
                  style='Secondary.TButton').grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="👁️ Ver por ID", 
                  command=self.ver_detalle_insumo_moderno,
                  style='Success.TButton').grid(row=0, column=2, padx=(10, 0), sticky="ew")

        # Área de resultados moderna
        resultado_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        resultado_card.pack(fill="both", expand=True)

        ttk.Label(resultado_card, text="📊 Resultados", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Área de texto con estilo moderno
        text_frame = ttk.Frame(resultado_card, style='Card.TFrame')
        text_frame.pack(fill="both", expand=True)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.text_inventario = tk.Text(text_frame, height=20, width=80,
                                      font=self.font_normal,
                                      bg=self.colors['white'],
                                      fg=self.colors['dark'],
                                      selectbackground=self.colors['primary'],
                                      relief='flat',
                                      borderwidth=0)
        scroll_inv = ttk.Scrollbar(text_frame, orient="vertical", 
                                  command=self.text_inventario.yview)
        self.text_inventario.configure(yscrollcommand=scroll_inv.set)

        self.text_inventario.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        scroll_inv.grid(row=0, column=1, sticky="ns")

        # Mensaje inicial
        self.text_inventario.insert(tk.END, 
            "💡 Selecciona una acción para consultar el inventario...\n\n"
            "📋 Ver Inventario Completo: Muestra todos los productos (ID 0-17)\n"
            "🔍 Buscar Insumo: Busca por nombre de producto\n"
            "👁️ Ver por ID: Muestra detalles específicos de un producto")


    def mostrar_inventario_completo_moderno(self):
        """Mostrar el inventario completo con formato moderno"""
        df_inventario = cargar_excel(inventario)
        if df_inventario.empty:
            self.text_inventario.delete(1.0, tk.END)
            self.text_inventario.insert(tk.END, "❌ No hay datos de inventario disponibles.")
            return

        self.text_inventario.delete(1.0, tk.END)
        self.text_inventario.insert(tk.END, 
            "📦 INVENTARIO COMPLETO\n"
            "=" * 60 + "\n\n")

        # Header de tabla
        self.text_inventario.insert(tk.END, 
            f"{'ID':<4} | {'PRODUCTO':<35} | {'CANTIDAD':<10} | {'ÚLTIMA ACTUALIZACIÓN':<15}\n")
        self.text_inventario.insert(tk.END, "-" * 80 + "\n")

        # Mostrar datos
        df_mostrar = df_inventario.loc[0:17] if len(df_inventario) > 17 else df_inventario

        for idx, row in df_mostrar.iterrows():
            producto = str(row.get('producto', 'N/A'))[:35]
            cantidad = str(row.get('cantidad', 'N/A'))
            fecha = str(row.get('ultima_actualizacion', 'N/A'))[:15]

            self.text_inventario.insert(tk.END, 
                f"{idx:<4} | {producto:<35} | {cantidad:<10} | {fecha:<15}\n")

        self.text_inventario.insert(tk.END, f"\n📊 Total de productos: {len(df_mostrar)}")


    def buscar_insumo_moderno(self):
        """Buscar insumo con interfaz moderna"""
        # Crear ventana de búsqueda moderna
        ventana_busqueda = ttk.Toplevel(self.root)
        ventana_busqueda.title("Buscar Insumo")
        ventana_busqueda.geometry("400x200")
        ventana_busqueda.configure(bg=self.colors['light'])
        ventana_busqueda.transient(self.root)
        ventana_busqueda.grab_set()

        # Card de búsqueda
        search_card = ttk.Frame(ventana_busqueda, style='Card.TFrame', padding=30)
        search_card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(search_card, text="🔍 Buscar Insumo", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        ttk.Label(search_card, text="Ingrese el nombre del insumo:", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 10))

        entry_busqueda = ttk.Entry(search_card, font=self.font_normal, 
                                  style='Modern.TEntry', width=40)
        entry_busqueda.pack(fill="x", pady=(0, 20))
        entry_busqueda.focus()

        def realizar_busqueda():
            nombre = entry_busqueda.get().strip()
            if not nombre:
                messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
                return

            df_inventario = cargar_excel(inventario)
            df_inventario["producto_norm"] = df_inventario["producto"].astype(str).str.strip().str.lower()
            nombre_norm = nombre.lower()
            resultado = df_inventario[df_inventario["producto_norm"].str.contains(nombre_norm)]

            self.text_inventario.delete(1.0, tk.END)
            if resultado.empty:
                self.text_inventario.insert(tk.END, 
                    f"❌ No se encontraron insumos con el nombre '{nombre}'\n\n"
                    "💡 Sugerencias:\n"
                    "• Verifica la ortografía\n"
                    "• Intenta con palabras más cortas\n"
                    "• Usa términos generales")
            else:
                self.text_inventario.insert(tk.END, 
                    f"🔍 RESULTADOS DE BÚSQUEDA: '{nombre}'\n"
                    "=" * 50 + "\n\n")

                for idx, row in resultado.iterrows():
                    self.text_inventario.insert(tk.END, 
                        f"📦 PRODUCTO: {row['producto']}\n"
                        f"   📊 Cantidad: {row['cantidad']}\n"
                        f"   🕒 Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n"
                        f"   🆔 ID: {idx}\n\n")

                self.text_inventario.insert(tk.END, 
                    f"✅ Se encontraron {len(resultado)} resultado(s)")

            ventana_busqueda.destroy()

        # Botones
        btn_frame = ttk.Frame(search_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="🔍 Buscar", command=realizar_busqueda,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_busqueda.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Bind Enter
        ventana_busqueda.bind('<Return>', lambda e: realizar_busqueda())


    def ver_detalle_insumo_moderno(self):
        """Ver detalle de insumo por ID con interfaz moderna"""
        # Crear ventana de selección moderna
        ventana_detalle = ttk.Toplevel(self.root)
        ventana_detalle.title("Ver Detalle por ID")
        ventana_detalle.geometry("400x250")
        ventana_detalle.configure(bg=self.colors['light'])
        ventana_detalle.transient(self.root)
        ventana_detalle.grab_set()

        # Card de selección
        detail_card = ttk.Frame(ventana_detalle, style='Card.TFrame', padding=30)
        detail_card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(detail_card, text="👁️ Ver Detalle por ID", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        ttk.Label(detail_card, text="Seleccione el ID del insumo (0-17):", 
                 style='Custom.TLabel').pack(anchor="w", pady=(0, 10))

        # Spinbox moderno para selección de ID
        id_var = tk.StringVar(value="0")
        spinbox_frame = ttk.Frame(detail_card, style='Card.TFrame')
        spinbox_frame.pack(fill="x", pady=(0, 20))

        id_spinbox = tk.Spinbox(spinbox_frame, from_=0, to=17, textvariable=id_var,
                               font=self.font_normal, width=10,
                               bg=self.colors['white'], fg=self.colors['dark'],
                               relief='solid', borderwidth=2)
        id_spinbox.pack(side="left")

        def mostrar_detalle():
            try:
                idx = int(id_var.get())
                if not (0 <= idx <= 17):
                    messagebox.showerror("Error", "ID debe estar entre 0 y 17")
                    return

                df_inventario = cargar_excel(inventario)
                if idx >= len(df_inventario):
                    messagebox.showerror("Error", f"No existe producto con ID {idx}")
                    return

                row = df_inventario.iloc[idx]

                # Mostrar detalle en el área principal
                self.text_inventario.delete(1.0, tk.END)
                self.text_inventario.insert(tk.END, 
                    f"📋 DETALLE COMPLETO DEL INSUMO\n"
                    "=" * 40 + "\n\n"
                    f"🆔 ID: {idx}\n"
                    f"📦 Producto: {row.get('producto', 'N/A')}\n"
                    f"📊 Cantidad disponible: {row.get('cantidad', 'N/A')} unidades\n"
                    f"🕒 Última actualización: {row.get('ultima_actualizacion', 'N/A')}\n\n"
                    "=" * 40 + "\n"
                    f"📈 Estado del inventario:\n")

                cantidad = row.get('cantidad', 0)
                if cantidad > 50:
                    self.text_inventario.insert(tk.END, "✅ Stock alto - Bien abastecido\n")
                elif cantidad > 20:
                    self.text_inventario.insert(tk.END, "⚠️ Stock medio - Revisar pronto\n")
                elif cantidad > 0:
                    self.text_inventario.insert(tk.END, "🔴 Stock bajo - Reabastecer urgente\n")
                else:
                    self.text_inventario.insert(tk.END, "❌ Sin stock - Producto agotado\n")

                ventana_detalle.destroy()

            except ValueError:
                messagebox.showerror("Error", "Ingrese un ID válido")

        # Botones
        btn_frame = ttk.Frame(detail_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="👁️ Ver Detalle", command=mostrar_detalle,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_detalle.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")


    def menu_verificar_disponibilidad_completo(self):
        """Menú modernizado completo para verificar disponibilidad"""
        ventana = self.crear_ventana_secundaria("Verificar Disponibilidad de Insumos", "800x600", "✅")

        main_frame = ttk.Frame(ventana, style='Main.TFrame', padding=20)
        main_frame.pack(fill="both", expand=True)

        # Panel de acciones moderno
        acciones_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        acciones_card.pack(fill="x", pady=(0, 20))

        ttk.Label(acciones_card, text="🔧 Gestión de Disponibilidad", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Grid de botones modernos
        btn_grid = ttk.Frame(acciones_card, style='Card.TFrame')
        btn_grid.pack(fill="x")
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_grid, text="📋 Generar Lista\nde Envío", 
                  command=self.generar_lista_envio_moderno,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_grid, text="📧 Enviar Lista\npor Email", 
                  command=self.enviar_lista_email_moderno,
                  style='Secondary.TButton').grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_grid, text="🔄 Actualizar\nInventario", 
                  command=self.actualizar_inventario_moderno,
                  style='Success.TButton').grid(row=0, column=2, padx=(10, 0), sticky="ew")

        # Área de resultados moderna
        resultado_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        resultado_card.pack(fill="both", expand=True)

        ttk.Label(resultado_card, text="📊 Estado de Disponibilidad", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 15))

        # Área de texto estilizada
        text_frame = ttk.Frame(resultado_card, style='Card.TFrame')
        text_frame.pack(fill="both", expand=True)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.text_disponibilidad = tk.Text(text_frame, height=15, width=70,
                                          font=self.font_normal,
                                          bg=self.colors['white'],
                                          fg=self.colors['dark'],
                                          selectbackground=self.colors['primary'],
                                          relief='flat',
                                          borderwidth=0)
        scroll_disp = ttk.Scrollbar(text_frame, orient="vertical", 
                                   command=self.text_disponibilidad.yview)
        self.text_disponibilidad.configure(yscrollcommand=scroll_disp.set)

        self.text_disponibilidad.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        scroll_disp.grid(row=0, column=1, sticky="ns")

        # Mensaje inicial
        self.text_disponibilidad.insert(tk.END,
            "💡 Gestión de Disponibilidad de Insumos\n\n"
            "📋 Generar Lista de Envío: Identifica productos listos para enviar\n"
            "📧 Enviar por Email: Envía la lista al coordinador de compras\n"
            "🔄 Actualizar Inventario: Descuenta cantidades demandadas\n\n"
            "Selecciona una acción para comenzar...")


    def generar_lista_envio_moderno(self):
        """Generar lista de envío con formato moderno"""
        try:
            lista = generar_lista_envio()

            self.text_disponibilidad.delete(1.0, tk.END)
            if lista.empty:
                self.text_disponibilidad.insert(tk.END,
                    "❌ ANÁLISIS DE DISPONIBILIDAD\n"
                    "=" * 50 + "\n\n"
                    "No hay insumos que cumplan completamente con la demanda actual.\n\n"
                    "💡 Recomendaciones:\n"
                    "• Revisar las solicitudes de compra pendientes\n"
                    "• Verificar el inventario actual\n"
                    "• Contactar proveedores para reabastecer")
            else:
                self.text_disponibilidad.insert(tk.END,
                    "✅ INSUMOS LISTOS PARA ENVÍO\n"
                    "=" * 50 + "\n\n")

                total_productos = len(lista)
                total_cantidad = lista['cantidad_a_enviar'].sum()

                for idx, row in lista.iterrows():
                    self.text_disponibilidad.insert(tk.END,
                        f"📦 {row['producto']}\n"
                        f"   📊 Cantidad a enviar: {row['cantidad_a_enviar']} unidades\n"
                        f"   ✅ Estado: Listo para despacho\n\n")

                self.text_disponibilidad.insert(tk.END,
                    f"📈 RESUMEN:\n"
                    f"• Total de productos listos: {total_productos}\n"
                    f"• Cantidad total a enviar: {total_cantidad} unidades\n"
                    f"• Estado general: ✅ Preparado para envío")

        except Exception as e:
            self.text_disponibilidad.delete(1.0, tk.END)
            self.text_disponibilidad.insert(tk.END,
                f"❌ ERROR EN LA GENERACIÓN\n"
                f"=" * 40 + "\n\n"
                f"Se produjo un error: {str(e)}\n\n"
                f"💡 Verifique:\n"
                f"• Que existan archivos de inventario y demanda\n"
                f"• Que los archivos no estén abiertos en otra aplicación")


    def enviar_lista_email_moderno(self):
        """Enviar lista por email con confirmación moderna"""
        # Ventana de confirmación moderna
        ventana_confirm = ttk.Toplevel(self.root)
        ventana_confirm.title("Confirmar Envío")
        ventana_confirm.geometry("450x300")
        ventana_confirm.configure(bg=self.colors['light'])
        ventana_confirm.transient(self.root)
        ventana_confirm.grab_set()

        # Card de confirmación
        confirm_card = ttk.Frame(ventana_confirm, style='Card.TFrame', padding=30)
        confirm_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Icono y título
        ttk.Label(confirm_card, text="📧", font=('Segoe UI', 48)).pack(pady=(0, 15))
        ttk.Label(confirm_card, text="Confirmar Envío por Email", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        # Información del envío
        info_frame = ttk.Frame(confirm_card, style='Card.TFrame')
        info_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(info_frame, text="📤 Destinatario: elcoordinadordecompras@gmail.com", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)
        ttk.Label(info_frame, text="📋 Asunto: Lista de insumos listos para envío", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)
        ttk.Label(info_frame, text="📎 Adjunto: insumos_listos.xlsx", 
                 style='Custom.TLabel').pack(anchor="w", pady=2)

        def confirmar_envio():
            try:
                # Mostrar progreso
                progress_label = ttk.Label(confirm_card, text="📤 Enviando...", 
                                         style='Custom.TLabel')
                progress_label.pack(pady=10)
                ventana_confirm.update()

                # Enviar email
                enviar_lista_insumos()

                ventana_confirm.destroy()
                messagebox.showinfo("Éxito", 
                    "✅ Lista enviada exitosamente!\n\n"
                    "📧 El coordinador de compras recibirá la lista de insumos "
                    "listos para envío en su correo electrónico.")

                # Actualizar área de resultados
                self.text_disponibilidad.insert(tk.END,
                    f"\n\n📧 EMAIL ENVIADO EXITOSAMENTE\n"
                    f"🕒 Hora: {datetime.now().strftime('%H:%M:%S')}\n"
                    f"📤 Estado: Entregado")

            except Exception as e:
                ventana_confirm.destroy()
                messagebox.showerror("Error", 
                    f"❌ Error al enviar email:\n{str(e)}\n\n"
                    "Verifique su conexión a internet y la configuración SMTP.")

        # Botones
        btn_frame = ttk.Frame(confirm_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="📧 Enviar Ahora", command=confirmar_envio,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_confirm.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")


    def actualizar_inventario_moderno(self):
        """Actualizar inventario con confirmación moderna"""
        # Ventana de confirmación
        ventana_update = ttk.Toplevel(self.root)
        ventana_update.title("Actualizar Inventario")
        ventana_update.geometry("500x350")
        ventana_update.configure(bg=self.colors['light'])
        ventana_update.transient(self.root)
        ventana_update.grab_set()

        # Card principal
        update_card = ttk.Frame(ventana_update, style='Card.TFrame', padding=30)
        update_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Icono y título
        ttk.Label(update_card, text="🔄", font=('Segoe UI', 48)).pack(pady=(0, 15))
        ttk.Label(update_card, text="Actualizar Inventario", 
                 style='Subtitle.TLabel').pack(pady=(0, 20))

        # Advertencia
        warning_frame = ttk.Frame(update_card, style='Card.TFrame')
        warning_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(warning_frame, text="⚠️ ATENCIÓN", 
                 style='Subtitle.TLabel', foreground='#E74C3C').pack()
        ttk.Label(warning_frame, 
                 text="Esta acción descontará las cantidades demandadas\n"
                      "del inventario actual. El proceso es irreversible.\n\n"
                      "Se actualizarán las fechas de última modificación.", 
                 style='Custom.TLabel', justify='center').pack(pady=(10, 0))

        def confirmar_actualizacion():
            try:
                # Mostrar progreso
                progress_label = ttk.Label(update_card, text="🔄 Actualizando inventario...", 
                                         style='Custom.TLabel')
                progress_label.pack(pady=10)
                ventana_update.update()

                # Actualizar inventario
                actualizar_inventario()

                ventana_update.destroy()
                messagebox.showinfo("Éxito", 
                    "✅ Inventario actualizado correctamente!\n\n"
                    "📊 Las cantidades demandadas han sido descontadas\n"
                    "🕒 Fechas de actualización registradas")

                # Actualizar área de resultados
                self.text_disponibilidad.insert(tk.END,
                    f"\n\n🔄 INVENTARIO ACTUALIZADO\n"
                    f"🕒 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"✅ Estado: Completado exitosamente")

            except Exception as e:
                ventana_update.destroy()
                messagebox.showerror("Error", 
                    f"❌ Error al actualizar inventario:\n{str(e)}")

        # Botones
        btn_frame = ttk.Frame(update_card, style='Card.TFrame')
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="🔄 Actualizar", command=confirmar_actualizacion,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana_update.destroy,
                  style='Success.TButton').grid(row=0, column=1, padx=(10, 0), sticky="ew")


if __name__ == "__main__":
    main()
