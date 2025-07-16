# Sistema Finca Directa SAS - Interfaz Gráfica

## Descripción

Esta aplicación convierte el sistema de consola original en una interfaz gráfica moderna usando tkinter, manteniendo toda la funcionalidad original del sistema de gestión de finca.

## Estructura del Proyecto

- **`main.py`**: Contiene toda la lógica del negocio, funciones de procesamiento de datos y operaciones del sistema
- **`intento.py`**: Interfaz gráfica de usuario (GUI) que conecta con la lógica en main.py
- **`data/`**: Carpeta con archivos Excel que contienen los datos del sistema

## Funcionalidades Implementadas

### 🔐 Autenticación
- **Inicio de sesión**: Con correo y contraseña
- **Crear cuenta nueva**: Requiere clave maestra para seguridad
- **Gestión de usuarios**: Los usuarios se almacenan en `data/usuarios.xlsx`

### 📊 Consultar Demanda de Pedidos (HU4)
- **Filtros disponibles**:
  - Por fecha (desde/hasta)
  - Por nombre de producto
  - Combinado (fecha + producto)
- **Visualización**: Tabla con ID, Fecha, Cliente, Producto, Cantidad
- **Acciones**:
  - Ver detalle del pedido seleccionado
  - Exportar resultados a Excel
  - Reiniciar filtros

### 📦 Consultar Inventario (HU1)
- **Mostrar inventario completo**: Lista de todos los productos (ID 0-17)
- **Buscar insumo**: Por nombre (búsqueda parcial)
- **Ver detalle por ID**: Información completa del insumo

### ✅ Verificar Disponibilidad de Insumos (HU2)
- **Generar lista de envío**: Productos que cumplen la demanda
- **Enviar por email**: Lista automática al correo configurado
- **Actualizar inventario**: Resta cantidades demandadas del stock

### 📥 Recepción de Insumos (HU5)
- **Registro de información**:
  - Proveedor
  - Fecha de recepción
  - Número de pedido
- **Gestión de productos**:
  - Agregar productos con cantidades
  - Lista visual de productos agregados
- **Procesamiento completo**:
  - Validación de campos
  - Verificación de calidad (simplificada)
  - Ingreso automático al inventario

### 📋 Reportes de Recepción (HU7)
- **Filtrar por fechas**: Rangos específicos de recepción
- **Listar reportes disponibles**: Visualización de entregas
- **Ver reporte específico**: Detalle completo con estado de conformidad
- **Generar archivos Excel**: Exportación automática

### 🛒 Reportes de Solicitudes de Compra (HU8)
- Funcionalidad base implementada (por completar)

### 🚚 Reportes de Insumos Listos (HU10)
- Funcionalidad base implementada (por completar)

## Cómo Usar la Aplicación

### 1. Ejecutar la Aplicación
```bash
python intento.py
```

### 2. Inicio de Sesión
- **Usuario por defecto**: Crea una cuenta nueva usando la clave maestra `FDsas/25`
- O usa credenciales existentes si ya tienes una cuenta

### 3. Navegación
- **Menú Principal**: 8 botones principales para acceder a cada funcionalidad
- **Ventanas Secundarias**: Cada módulo se abre en su propia ventana
- **Controles Intuitivos**: Botones con íconos y descripciones claras

### 4. Flujo de Trabajo Típico
1. **Consultar demanda** → Filtrar pedidos → Exportar a Excel
2. **Verificar disponibilidad** → Generar lista → Enviar por email
3. **Recibir insumos** → Registrar información → Procesar recepción
4. **Generar reportes** → Filtrar por fecha → Descargar archivos

## Características de la Interfaz

### 🎨 Diseño Moderno
- **Fuentes legibles**: Arial en diferentes tamaños
- **Colores coherentes**: Esquema de colores profesional
- **Íconos descriptivos**: Emojis para mejor identificación visual
- **Layout responsivo**: Uso correcto de grid y pack

### 🔄 Separación de Responsabilidades (MVC Básico)
- **Modelo**: Lógica de negocio en `main.py`
- **Vista**: Interfaz gráfica en `intento.py`
- **Controlador**: Métodos de la clase GUI que conectan vista y modelo

### ⚡ Funcionalidades Mejoradas
- **Validación en tiempo real**: Verificación de campos antes de procesar
- **Mensajes informativos**: Notificaciones claras de éxito/error
- **Manejo de errores**: Try-catch robusto con mensajes descriptivos
- **Navegación fluida**: Ventanas modales y secundarias organizadas

## Archivos de Datos Requeridos

La aplicación espera encontrar los siguientes archivos en la carpeta `data/`:
- `pedidos_granja.xlsx`
- `inventario.xlsx`
- `demanda.xlsx`
- `entregas.xlsx`
- `detalle_entregas.xlsx`
- `usuarios.xlsx`
- `solicitudes_compras.xlsx`
- `insumos_listos_general.xlsx`

## Dependencias

```python
- tkinter (incluido con Python)
- pandas
- openpyxl
- datetime
- os
- smtplib
```

## Configuración de Email

Para el envío automático de listas, la aplicación usa:
- **SMTP**: Gmail (smtp.gmail.com:465)
- **Remitente**: elcoordinadordecompras@gmail.com
- **Contraseña**: Configurada en el código (contraseña de aplicación)

## Próximas Mejoras

1. **Completar HU8 y HU10**: Funcionalidades de reportes faltantes
2. **Validación de email mejorada**: Configuración de SMTP más flexible
3. **Temas visuales**: Soporte para modo oscuro/claro
4. **Exportación avanzada**: Más formatos (PDF, CSV)
5. **Gráficos y estadísticas**: Visualización de datos con matplotlib

## Solución de Problemas

### Error al importar main.py
- Verificar que ambos archivos estén en el mismo directorio
- Asegurar que main.py no tenga errores de sintaxis

### Error de archivos Excel
- Verificar que la carpeta `data/` exista
- Asegurar que los archivos Excel no estén abiertos en otra aplicación

### Error de envío de email
- Verificar conexión a internet
- Revisar configuración SMTP en main.py

---

**Desarrollado para**: Sistema Finca Directa SAS  
**Versión**: 1.0  
**Tecnología**: Python + tkinter  
**Arquitectura**: MVC básico con separación de lógica y presentación
