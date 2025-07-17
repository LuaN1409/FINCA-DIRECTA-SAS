# 🚨 Módulo: Reportar Insumos Defectuosos

## Descripción
El módulo "Reportar Insumos Defectuosos" permite registrar y gestionar productos que presenten problemas de calidad o cantidad durante la recepción o almacenamiento.

## Características Principales

### ✨ Funcionalidades Implementadas

1. **Registro de Insumos Defectuosos**
   - Formulario para capturar información del proveedor
   - Campo de fecha (auto-relleno con fecha actual)
   - Campos para producto y cantidad afectada
   - Dropdown para tipo de problema: "Calidad" o "Cantidad"
   - Campo opcional para observaciones detalladas

2. **Gestión de Lista de Defectuosos**
   - Vista en tabla (TreeView) de todos los insumos reportados
   - Opciones para modificar, eliminar o limpiar registros
   - Numeración automática de items
   - Validación de datos antes de agregar

3. **Reportes y Confirmación**
   - Ventana de revisión antes de guardar
   - Guardado automático en archivo Excel con timestamp
   - Preparado para envío por email (próximamente)
   - Limpieza automática del formulario después de guardar

### 🎯 Cómo Usar el Módulo

#### Paso 1: Acceder al Módulo
- Inicie la aplicación con `python app.py`
- Autentíquese en el sistema
- En el menú principal, haga clic en "🚨 Reportar Insumos Defectuosos"

#### Paso 2: Completar Información General
- **Proveedor**: Ingrese el nombre del proveedor responsable
- **Fecha**: Se auto-completa con la fecha actual (puede modificarse)

#### Paso 3: Agregar Insumos Defectuosos
- **Producto**: Nombre del insumo con problemas
- **Cantidad afectada**: Número de unidades con defecto
- **Tipo de problema**: Seleccione "Calidad" o "Cantidad"
- **Observaciones**: Detalles adicionales (opcional)
- Haga clic en "➕ Agregar Insumo"

#### Paso 4: Gestionar la Lista
- **Modificar**: Seleccione un item y haga clic en "🔄 Modificar Seleccionado"
- **Eliminar**: Seleccione un item y haga clic en "🗑️ Eliminar Seleccionado"
- **Limpiar Todo**: Use "🧹 Limpiar Todo" para vaciar la lista completa

#### Paso 5: Finalizar Reporte
- **Revisar**: Haga clic en "✅ Confirmar y Revisar" para ver el resumen
- **Guardar**: Use "💾 Guardar Reporte" para crear archivo Excel
- **Email**: "📧 Enviar por Email" (próximamente disponible)

### 📁 Archivos Generados

Los reportes se guardan en la carpeta `data/` con el formato:
```
reporte_defectuosos_YYYYMMDD_HHMMSS.xlsx
```

**Estructura del archivo Excel:**
- Proveedor
- Fecha
- Producto
- Cantidad_Afectada
- Tipo_Problema
- Observaciones
- Fecha_Reporte (timestamp de creación)

### 🔧 Validaciones Implementadas

- **Campos requeridos**: Proveedor, fecha, al menos un insumo
- **Cantidad numérica**: Debe ser un número mayor a 0
- **Producto no vacío**: Nombre del producto es obligatorio
- **Confirmación antes de eliminar**: Previene borrado accidental

### 🚀 Funcionalidades Avanzadas

1. **Auto-limpieza**: El formulario se limpia automáticamente después de guardar
2. **Timestamps**: Cada reporte incluye marca de tiempo de creación
3. **Interfaz intuitiva**: Iconos y colores para fácil navegación
4. **Validación robusta**: Previene errores de entrada de datos
5. **Estructura modular**: Fácil mantenimiento y extensión

### 📋 Próximas Mejoras

- [ ] Envío automático por email
- [ ] Integración con sistema de notificaciones
- [ ] Reportes estadísticos de defectuosos
- [ ] Fotografías adjuntas para evidencia
- [ ] Dashboard de calidad de proveedores

### 🐛 Solución de Problemas

**Problema**: No puedo agregar un insumo
- **Solución**: Verifique que todos los campos requeridos estén completos

**Problema**: Error al guardar reporte
- **Solución**: Asegúrese de que la carpeta `data/` existe y tiene permisos de escritura

**Problema**: La aplicación no responde
- **Solución**: Reinicie la aplicación y verifique las dependencias

### 📞 Soporte

Para reportar problemas o sugerir mejoras, contacte al equipo de desarrollo.

---
**Versión**: 1.0  
**Fecha**: 2024  
**Compatible con**: Sistema Finca Directa SAS v3.0+
