#!/bin/bash

# Script de instalación del módulo Payment QR para Odoo 17
# Ejecutar como: bash install_payment_qr.sh

echo "======================================"
echo "Instalación Payment QR para Odoo 17"
echo "======================================"

# Variables (MODIFICA ESTAS RUTAS SEGÚN TU INSTALACIÓN)
ODOO_ADDONS_PATH="/opt/odoo/addons"  # Ruta a tus addons de Odoo
MODULE_SOURCE="./payment_qr"          # Ruta donde está el módulo
ODOO_USER="odoo"                      # Usuario de Odoo
PYTHON_ENV="/opt/odoo/venv/bin/python3"  # Python de Odoo (o python3 si no usas venv)

echo ""
echo "1. Verificando permisos..."
if [ "$EUID" -ne 0 ]; then
    echo "ADVERTENCIA: Puede que necesites ejecutar con sudo"
fi

echo ""
echo "2. Copiando módulo a $ODOO_ADDONS_PATH..."
if [ -d "$MODULE_SOURCE" ]; then
    sudo cp -r "$MODULE_SOURCE" "$ODOO_ADDONS_PATH/"
    echo "✓ Módulo copiado exitosamente"
else
    echo "✗ Error: No se encuentra el directorio $MODULE_SOURCE"
    exit 1
fi

echo ""
echo "3. Instalando dependencias de Python..."
$PYTHON_ENV -m pip install -r "$ODOO_ADDONS_PATH/payment_qr/requirements.txt"

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas exitosamente"
else
    echo "✗ Error al instalar dependencias"
    exit 1
fi

echo ""
echo "4. Ajustando permisos..."
sudo chown -R $ODOO_USER:$ODOO_USER "$ODOO_ADDONS_PATH/payment_qr"
sudo chmod -R 755 "$ODOO_ADDONS_PATH/payment_qr"
echo "✓ Permisos ajustados"

echo ""
echo "5. Reiniciando servicio Odoo..."
sudo systemctl restart odoo

if [ $? -eq 0 ]; then
    echo "✓ Odoo reiniciado exitosamente"
else
    echo "! Reinicia Odoo manualmente si es necesario"
fi

echo ""
echo "======================================"
echo "INSTALACIÓN COMPLETADA"
echo "======================================"
echo ""
echo "Próximos pasos:"
echo "1. Ve a Odoo → Aplicaciones"
echo "2. Activa el modo desarrollador"
echo "3. Actualiza la lista de aplicaciones"
echo "4. Busca 'Payment QR Code - MercadoPago'"
echo "5. Haz clic en 'Instalar'"
echo ""
