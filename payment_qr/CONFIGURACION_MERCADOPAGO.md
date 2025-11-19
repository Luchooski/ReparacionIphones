# Guía de Configuración para MercadoPago

Esta guía te ayudará a configurar el módulo Payment QR con MercadoPago en Odoo 17.

## 📋 Requisitos previos

- Odoo 17 Community instalado y funcionando
- Una cuenta de MercadoPago (puede ser de prueba o producción)
- Acceso a las credenciales de MercadoPago
- Servidor Odoo accesible desde internet (para recibir webhooks)

## 🔐 Paso 1: Obtener credenciales de MercadoPago

### Para ambiente de pruebas

1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers/panel)
2. Inicia sesión con tu cuenta de MercadoPago
3. Ve a **"Tus integraciones" > "Credenciales"**
4. Selecciona **"Credenciales de prueba"**
5. Copia el **Access Token de prueba** (comienza con `TEST-`)

### Para ambiente de producción

1. En el mismo panel de MercadoPago Developers
2. Ve a **"Credenciales de producción"**
3. Completa el formulario "Quiero ir a producción"
4. Una vez aprobado, copia el **Access Token de producción** (comienza con `APP_USR-`)

## 📦 Paso 2: Instalar el módulo en Odoo

### 2.1 Copiar el módulo

```bash
# Copiar el módulo a la carpeta de addons
cp -r payment_qr /ruta/a/odoo/addons/

# O crear un symlink
ln -s /ruta/completa/al/modulo/payment_qr /ruta/a/odoo/addons/payment_qr
```

### 2.2 Instalar dependencias de Python

```bash
# Activar el entorno virtual de Odoo (si usas uno)
source /ruta/a/venv/bin/activate

# Instalar dependencias
pip install -r /ruta/a/odoo/addons/payment_qr/requirements.txt
```

### 2.3 Actualizar Odoo

```bash
# Reiniciar Odoo con actualización de módulo
/ruta/a/odoo-bin -u payment_qr -d nombre_base_datos

# O reiniciar el servicio
sudo systemctl restart odoo
```

### 2.4 Activar modo desarrollador

1. En Odoo, ve a **Ajustes**
2. Baja hasta el final y haz clic en **"Activar el modo desarrollador"**

### 2.5 Actualizar lista de aplicaciones

1. Ve a **Aplicaciones**
2. Haz clic en los tres puntos (⋮) > **"Actualizar lista de aplicaciones"**
3. Haz clic en **"Actualizar"** en el diálogo

### 2.6 Instalar el módulo

1. Busca "Payment QR Code" en la lista de aplicaciones
2. Haz clic en **"Instalar"**

## ⚙️ Paso 3: Configurar el método de pago

### 3.1 Crear el método de pago QR

1. Ve a **Punto de Venta > Configuración > Métodos de Pago**
2. Haz clic en **"Crear"**
3. Completa los campos:
   - **Nombre**: `MercadoPago QR` (o el nombre que prefieras)
   - **Diario**: Selecciona el diario bancario donde se registrarán los pagos
   - **Identificar Cliente**: Desmarcado (opcional)

### 3.2 Configurar Payment QR

En la misma pantalla, configura los siguientes campos:

- **☑ Usar Pago QR**: Activar
- **Proveedor QR**: Seleccionar `MercadoPago`
- **Ambiente**:
  - `Pruebas` - Para testing (usa credenciales de prueba)
  - `Producción` - Para uso real (usa credenciales de producción)
- **API Key**: Pegar tu Access Token de MercadoPago
  - Para pruebas: `TEST-1234567890-123456-abcdef...`
  - Para producción: `APP_USR-1234567890-123456-abcdef...`
- **Secret Key**: Dejar vacío (no es necesario para MercadoPago)
- **Timeout (segundos)**: `300` (5 minutos - tiempo máximo para completar el pago)
- **☑ Impresión Automática**: Activar si quieres imprimir el recibo automáticamente

### 3.3 Copiar la URL del Webhook

Después de guardar, aparecerá un campo de solo lectura:

- **URL Webhook**: `https://tu-dominio.com/payment_qr/webhook/1/mercadopago`

**¡IMPORTANTE!** Copia esta URL, la necesitarás en el siguiente paso.

## 🔔 Paso 4: Configurar webhook en MercadoPago

### 4.1 Acceder al panel de webhooks

1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers/panel)
2. Ve a **"Tus integraciones"**
3. Selecciona tu aplicación o crea una nueva
4. Ve a la pestaña **"Webhooks"** o **"IPN"**

### 4.2 Agregar la URL del webhook

1. Haz clic en **"Configurar notificaciones"** o **"Agregar webhook"**
2. Pega la URL que copiaste de Odoo:
   ```
   https://tu-dominio.com/payment_qr/webhook/1/mercadopago
   ```
3. Selecciona los eventos a notificar:
   - ☑ **Pagos** (Payments)
   - ☑ **Órdenes de pago** (Merchant Orders)
4. Haz clic en **"Guardar"**

### 4.3 Verificar el webhook

MercadoPago enviará una petición de prueba. Si todo está correcto, verás un estado "Activo" o un checkmark verde.

**Si falla la verificación:**
- Verifica que tu servidor Odoo sea accesible desde internet
- Verifica que no haya firewall bloqueando las peticiones
- Verifica que el certificado SSL esté configurado correctamente

## 🏪 Paso 5: Configurar el Punto de Venta

### 5.1 Asignar método de pago al POS

1. Ve a **Punto de Venta > Configuración > Puntos de Venta**
2. Selecciona tu punto de venta o crea uno nuevo
3. En la pestaña **"Pagos"**, haz clic en **"Agregar una línea"**
4. Selecciona el método `MercadoPago QR` que creaste
5. Haz clic en **"Guardar"**

### 5.2 Abrir sesión POS

1. Ve a **Punto de Venta > Panel**
2. Haz clic en **"Nueva Sesión"**
3. El POS se abrirá en una nueva ventana

## 🧪 Paso 6: Realizar una venta de prueba

### 6.1 Crear venta

1. En el POS, agrega uno o varios productos
2. Haz clic en **"Pago"**
3. Selecciona el método **"MercadoPago QR"**
4. Ingresa el monto

### 6.2 Escanear el QR

Se mostrará un código QR en pantalla:

1. Abre la app de MercadoPago en tu celular
2. Toca en **"Pagar con QR"** o el ícono de QR
3. Escanea el código QR mostrado en pantalla
4. Verás el monto exacto de la compra
5. Confirma el pago

**Para testing:**
- Usa las [tarjetas de prueba de MercadoPago](https://www.mercadopago.com.ar/developers/es/docs/checkout-api/testing)
- Tarjeta aprobada: `5031 7557 3453 0604` CVV: `123`

### 6.3 Confirmación automática

- El sistema verificará el pago cada 5 segundos
- Cuando MercadoPago confirme el pago, el POS avanzará automáticamente
- Si está configurado, se imprimirá el recibo automáticamente

## 🔍 Paso 7: Verificar transacciones

### Ver historial de transacciones

1. Ve a **Punto de Venta > Transacciones QR**
2. Verás todas las transacciones con su estado:
   - 🟢 **Realizado**: Pago completado
   - 🟡 **Pendiente**: Esperando confirmación
   - 🔴 **Error**: Pago rechazado

### Ver detalles de una transacción

1. Haz clic en cualquier transacción
2. Verás:
   - ID de referencia
   - Monto
   - Estado
   - Datos del webhook de MercadoPago
   - Fecha y hora

## 🚨 Solución de problemas

### El QR no se genera

**Problema**: Al seleccionar el método de pago no aparece el QR

**Soluciones:**
1. Verifica que las dependencias estén instaladas:
   ```bash
   pip install qrcode[pil] Pillow requests
   ```
2. Revisa los logs de Odoo:
   ```bash
   tail -f /var/log/odoo/odoo.log
   ```
3. Verifica que el Access Token sea correcto
4. Verifica la conectividad con la API de MercadoPago

### El webhook no recibe notificaciones

**Problema**: El pago no se confirma automáticamente

**Soluciones:**
1. Verifica que el servidor Odoo sea accesible desde internet:
   ```bash
   curl https://tu-dominio.com/payment_qr/webhook/1/mercadopago
   ```
2. Verifica el firewall:
   ```bash
   sudo ufw status
   # Asegúrate de que el puerto de Odoo esté abierto (ej: 8069)
   ```
3. Revisa los logs de webhooks en MercadoPago
4. Verifica que la URL del webhook en MercadoPago sea exactamente la misma que en Odoo

### Error de certificado SSL

**Problema**: MercadoPago no puede conectarse por SSL

**Soluciones:**
1. Instala un certificado SSL válido (Let's Encrypt es gratis):
   ```bash
   sudo certbot --nginx -d tu-dominio.com
   ```
2. Configura Odoo para usar HTTPS en el proxy (nginx/apache)

### Timeout - Pago no confirmado

**Problema**: Se agota el tiempo de espera

**Soluciones:**
1. Aumenta el timeout en la configuración del método de pago (de 300 a 600 segundos)
2. Verifica el estado manualmente en **Transacciones QR**
3. Revisa si el webhook llegó tarde (ver logs)

## 📱 Países soportados por MercadoPago

MercadoPago está disponible en:
- 🇦🇷 Argentina (ARS)
- 🇧🇷 Brasil (BRL)
- 🇨🇱 Chile (CLP)
- 🇨🇴 Colombia (COP)
- 🇲🇽 México (MXN)
- 🇵🇪 Perú (PEN)
- 🇺🇾 Uruguay (UYU)

Asegúrate de configurar la moneda correcta en Odoo.

## 📊 Monitoreo en producción

### Logs importantes

```bash
# Ver logs en tiempo real
tail -f /var/log/odoo/odoo.log | grep "MercadoPago\|payment_qr"

# Buscar errores
grep "ERROR.*payment_qr" /var/log/odoo/odoo.log
```

### Métricas recomendadas

- Tasa de éxito de pagos
- Tiempo promedio de confirmación
- Errores de webhook
- Timeouts

## 🔒 Seguridad

### Buenas prácticas

1. **Nunca** compartas tu Access Token de producción
2. Usa HTTPS obligatoriamente en producción
3. Mantén actualizadas las dependencias:
   ```bash
   pip install --upgrade qrcode Pillow requests
   ```
4. Revisa periódicamente los logs de seguridad
5. Usa credenciales de prueba solo en ambiente de testing

## 📞 Soporte

### Recursos de MercadoPago

- [Documentación oficial](https://www.mercadopago.com.ar/developers/es/docs)
- [Centro de ayuda](https://www.mercadopago.com.ar/ayuda)
- [Comunidad de desarrolladores](https://www.mercadopago.com.ar/developers/es/support)

### Recursos del módulo

- Ver logs: `/var/log/odoo/odoo.log`
- GitHub Issues: [Reportar problema](#)
- Email: soporte@tuempresa.com

## ✅ Checklist de configuración

Marca cada paso completado:

- [ ] Cuenta de MercadoPago creada
- [ ] Access Token obtenido
- [ ] Módulo instalado en Odoo
- [ ] Método de pago configurado
- [ ] Webhook configurado en MercadoPago
- [ ] Webhook verificado (activo)
- [ ] Método asignado al POS
- [ ] Venta de prueba realizada exitosamente
- [ ] Pago confirmado automáticamente
- [ ] Recibo impreso (si está configurado)

¡Felicitaciones! Tu sistema de pagos con QR está listo para usar. 🎉
