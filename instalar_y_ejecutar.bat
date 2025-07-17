@echo off
echo ========================================
echo  FINCA DIRECTA SAS - INSTALADOR RAPIDO
echo ========================================
echo.
echo Instalando dependencias automaticamente...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando pandas...
python -m pip install pandas>=1.5.0

echo Instalando openpyxl...
python -m pip install openpyxl>=3.0.0

echo Instalando ttkbootstrap...
python -m pip install ttkbootstrap>=1.10.0

echo.
echo ========================================
echo  INSTALACION COMPLETADA
echo ========================================
echo.
echo Ejecutando aplicacion...
python app.py

pause
