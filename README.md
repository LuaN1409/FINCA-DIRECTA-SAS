# 🌾 Sistema Finca Directa SAS

Sistema de gestión de insumos agrícolas con interfaz moderna y instalación automática de dependencias.

## 🚀 Ejecución Rápida

### Opción 1: Instalación Automática (Recomendada)
```bash
python app.py
```
El sistema detectará e instalará automáticamente todas las dependencias necesarias.

### Opción 2: Script de Instalación (Windows)
```bash
instalar_y_ejecutar.bat
```
Script que instala dependencias y ejecuta la aplicación automáticamente.

### Opción 3: Instalación Manual
```bash
pip install -r requirements.txt
python app.py
```

## 📋 Dependencias

- **pandas** >= 1.5.0 - Manejo de datos
- **openpyxl** >= 3.0.0 - Lectura/escritura de Excel
- **ttkbootstrap** >= 1.10.0 - Interfaz moderna

## 👤 Credenciales de Prueba

- **Usuario:** admin
- **Contraseña:** admin123

## 🎨 Características

- ✅ **Instalación automática de dependencias**
- 🎨 **Interfaz moderna con colores corporativos**
- 📊 **8 módulos integrados de gestión**
- 🔄 **Sistema de respaldo multi-nivel**
- 📱 **Diseño responsivo**

## 📦 Módulos Disponibles

1. 📊 **Consultar Demanda de Pedidos** - Análisis de solicitudes
2. 📦 **Consultar Inventario** - Control de stock disponible
3. ✅ **Verificar Disponibilidad** - Validar insumos requeridos
4. 📥 **Recepción de Insumos** - Registrar llegadas
5. 📋 **Reportes de Recepción** - Estadísticas de recepción
6. 🛒 **Reportes de Solicitudes** - Gestión de compras
7. 🚚 **Reportes Insumos Listos** - Estado de preparación
8. ⚙️ **Configuración** - Ajustes del sistema

## 🔧 Solución de Problemas

Si encuentras errores:

1. **Verifica Python:** `python --version`
2. **Instala dependencias:** `pip install -r requirements.txt`
3. **Ejecuta directamente:** `python fincaDirectaGUI.py`

## 📁 Estructura del Proyecto

```
FINCA-DIRECTA-SAS/
├── app.py                    # Launcher principal con auto-instalación
├── fincaDirectaGUI.py       # Interfaz gráfica moderna
├── main.py                  # Lógica de negocio
├── requirements.txt         # Dependencias del proyecto
├── instalar_y_ejecutar.bat  # Script de instalación Windows
├── data/                    # Archivos de datos Excel
├── gui/                     # Módulos de interfaz
├── core/                    # Lógica central
└── utils/                   # Utilidades
```

## 🌟 Versión

**v3.0** - Interfaz modernizada con instalación automática

---
**Finca Directa SAS** - Sistema de Gestión de Insumos Agrícolas
