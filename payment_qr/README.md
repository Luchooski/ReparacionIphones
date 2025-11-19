# Payment QR - Módulo de Pago con Código QR para Odoo

## 📋 Descripción

Módulo para Odoo que permite realizar pagos mediante código QR en el Punto de Venta (POS). El módulo genera códigos QR dinámicos con el monto exacto de la venta y recibe confirmaciones automáticas mediante webhook cuando el pago es completado.

## ✨ Características

- ✅ Generación dinámica de códigos QR con el monto de la venta
- ✅ Integración con múltiples proveedores de pago (MercadoPago, PayPal, Stripe, Yappy, personalizado)
- ✅ Webhook para confirmación automática de pagos
- ✅ Verificación de estado de pago en tiempo real mediante polling
- ✅ Impresión automática de recibo tras confirmación
- ✅ Interfaz amigable en el POS
- ✅ Registro completo de transacciones
- ✅ Soporte para ambientes de prueba y producción

## 📦 Requisitos

- Odoo 16.0 o superior
- Python 3.8 o superior
- Dependencias de Python:
  - `qrcode[pil]>=7.3.1`
  - `Pillow>=9.0.0`

## 🚀 Instalación

### 1. Instalar el módulo

```bash
# Copiar el módulo a la carpeta de addons de Odoo
cp -r payment_qr /ruta/a/odoo/addons/

# O crear un symlink
ln -s /ruta/al/modulo/payment_qr /ruta/a/odoo/addons/payment_qr
```

### 2. Instalar dependencias de Python

```bash
pip install -r payment_qr/requirements.txt
```

### 3. Actualizar la lista de módulos en Odoo

1. Ir a **Aplicaciones**
2. Hacer clic en **Actualizar lista de aplicaciones**
3. Buscar "Payment QR Code"
4. Hacer clic en **Instalar**

## ⚙️ Configuración

### 1. Configurar método de pago

1. Ir a **Punto de Venta > Configuración > Métodos de Pago**
2. Crear o editar un método de pago
3. Activar **"Usar Pago QR"**
4. Configurar los siguientes campos:

   - **Proveedor QR**: Seleccionar el proveedor de pagos
   - **API Key**: Clave API del proveedor
   - **Secret Key**: Clave secreta del proveedor
   - **Ambiente**: Seleccionar "Pruebas" o "Producción"
   - **Timeout**: Tiempo máximo de espera en segundos (default: 300)
   - **Impresión Automática**: Activar para imprimir recibo automáticamente

5. Copiar la **URL Webhook** que se genera automáticamente

### 2. Configurar webhook en el proveedor

Configurar la URL webhook en el panel del proveedor de pagos para recibir notificaciones:

```
https://tu-dominio.com/payment_qr/webhook/{payment_method_id}
```

### 3. Asignar método de pago al POS

1. Ir a **Punto de Venta > Configuración > Puntos de Venta**
2. Editar el punto de venta
3. En la pestaña **Pagos**, agregar el método de pago QR configurado

## 🎯 Uso

### En el Punto de Venta

1. Agregar productos a la venta
2. Hacer clic en **Pagar**
3. Seleccionar el método de pago **QR**
4. Se generará automáticamente un código QR con el monto exacto
5. El cliente escanea el código QR con su aplicación de pago
6. El cliente confirma el pago en su aplicación
7. El sistema recibe la confirmación automáticamente mediante webhook
8. El recibo se imprime automáticamente (si está configurado)

### Verificar transacciones

1. Ir a **Punto de Venta > Transacciones QR**
2. Ver el historial completo de todas las transacciones QR
3. Filtrar por estado: Pendiente, Realizado, Cancelado, Error

## 🔌 Integración con proveedores

### MercadoPago

```python
# Configuración en el método de pago:
# - Proveedor: MercadoPago
# - API Key: Tu Access Token de MercadoPago
# - Secret Key: Tu Client Secret
# - URL Webhook: Configurar en el panel de MercadoPago
```

### PayPal

```python
# Configuración en el método de pago:
# - Proveedor: PayPal
# - API Key: Tu Client ID de PayPal
# - Secret Key: Tu Secret
# - URL Webhook: Configurar en el dashboard de PayPal
```

### Yappy (Panamá)

```python
# Configuración en el método de pago:
# - Proveedor: Yappy
# - API Key: Tu API Key de Yappy
# - Secret Key: Tu Secret Key
# - URL Webhook: Configurar en el portal de Yappy
```

### Personalizado

Para integrar un proveedor personalizado, editar el método `_get_custom_qr` en el archivo:
`payment_qr/models/pos_payment_method.py`

## 🔧 API y Webhooks

### Endpoint de Webhook

```
POST /payment_qr/webhook/<payment_method_id>
Content-Type: application/json

{
  "reference": "POS-123-456-789",
  "status": "approved",
  "transaction_id": "ABC123",
  "amount": 100.00
}
```

### Verificar estado de pago

```
GET /payment_qr/webhook/<payment_method_id>/status?reference=POS-123-456-789
```

### Check payment desde POS

```javascript
// Llamada RPC desde el frontend
this.env.services.rpc({
    route: '/payment_qr/check_payment',
    params: { reference: 'POS-123-456-789' }
});
```

## 📁 Estructura del módulo

```
payment_qr/
├── __init__.py
├── __manifest__.py
├── README.md
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── pos_payment_method.py      # Configuración del método de pago
│   ├── pos_payment.py              # Gestión de pagos individuales
│   └── payment_transaction.py     # Registro de transacciones
├── controllers/
│   ├── __init__.py
│   └── webhook.py                  # Endpoints para webhooks
├── views/
│   └── pos_payment_method_views.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── pos_payment_method_data.xml
└── static/
    └── src/
        ├── js/
        │   ├── PaymentQR.js        # Lógica frontend del pago
        │   └── models.js           # Extensión de modelos POS
        ├── xml/
        │   └── PaymentScreen.xml   # Vista del código QR
        └── css/
            └── payment_qr.css      # Estilos
```

## 🐛 Solución de problemas

### El código QR no se genera

- Verificar que las dependencias de Python estén instaladas (`qrcode`, `Pillow`)
- Revisar los logs de Odoo para errores
- Verificar que el método de pago tenga configurado correctamente el proveedor y las credenciales

### El webhook no recibe notificaciones

- Verificar que la URL webhook esté correctamente configurada en el proveedor
- Verificar que el servidor Odoo sea accesible desde internet
- Revisar los logs del servidor para ver si las peticiones están llegando
- Verificar que el firewall permita conexiones al puerto de Odoo

### El pago no se confirma automáticamente

- Verificar que el webhook esté funcionando correctamente
- Revisar el estado de la transacción en **Punto de Venta > Transacciones QR**
- Verificar que el proveedor esté enviando el campo `reference` correcto
- Aumentar el tiempo de timeout si es necesario

## 🔐 Seguridad

- Las claves API y Secret Keys se almacenan de forma segura en la base de datos
- Los webhooks validan la autenticidad de las peticiones
- Las transacciones se registran con timestamp para auditoría
- Soporte para ambientes de prueba separados de producción

## 📝 Desarrollo

### Agregar un nuevo proveedor

1. Editar `models/pos_payment_method.py`
2. Agregar el proveedor en el campo `qr_provider`
3. Implementar el método `_get_<proveedor>_qr()`
4. Actualizar la documentación

### Personalizar la vista del QR

Editar los archivos:
- `static/src/xml/PaymentScreen.xml` - Estructura HTML
- `static/src/css/payment_qr.css` - Estilos

## 📄 Licencia

LGPL-3

## 👥 Autor

Tu Empresa

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📧 Soporte

Para soporte técnico o preguntas, contactar a: soporte@tuempresa.com

## 🔄 Changelog

### v1.0.0 (2025-01-19)

- ✅ Primera versión estable
- ✅ Soporte para múltiples proveedores de pago
- ✅ Generación dinámica de códigos QR
- ✅ Webhook para confirmación automática
- ✅ Registro completo de transacciones
- ✅ Impresión automática de recibos
