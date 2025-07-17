"""
Módulos adicionales modernizados para el Sistema Finca Directa SAS
Este archivo contiene las implementaciones modernas de todos los módulos restantes
"""

# Imports necesarios
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import sys
import os

# Importar funciones del main si están disponibles
try:
    from main import (cargar_excel, generar_lista_envio, enviar_lista_insumos, 
                     actualizar_inventario, inventario, pedidos)
except ImportError:
    # Definir variables dummy si no están disponibles
    inventario = "data/inventario.xlsx"
    pedidos = "data/pedidos.xlsx"
    
    def cargar_excel(file_path):
        """Función dummy para cargar Excel"""
        try:
            return pd.read_excel(file_path)
        except:
            return pd.DataFrame()
    
    def generar_lista_envio():
        """Función dummy para generar lista de envío"""
        return pd.DataFrame()
    
    def enviar_lista_insumos():
        """Función dummy para enviar lista por email"""
        pass
    
    def actualizar_inventario():
        """Función dummy para actualizar inventario"""
        pass

# Métodos adicionales para la clase SistemaFincaDirectaGUI

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

# Estas funciones se deben agregar a la clase SistemaFincaDirectaGUI reemplazando las versiones simplificadas
