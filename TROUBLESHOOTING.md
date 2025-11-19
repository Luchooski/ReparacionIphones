# 🔧 Solución de Problemas - Payment QR MercadoPago

## Problema 1: El módulo no aparece en Aplicaciones

**Síntomas**: No encuentro "Payment QR" en la lista de aplicaciones

**Soluciones**:
```bash
# 1. Verificar que el módulo esté en addons
ls -la /opt/odoo/addons/payment_qr

# 2. Verificar permisos
sudo chown -R odoo:odoo /opt/odoo/addons/payment_qr

# 3. Revisar logs de Odoo
sudo tail -100 /var/log/odoo/odoo.log

# 4. Reiniciar Odoo con actualización
sudo systemctl restart odoo
```

En Odoo:
```
1. Asegúrate de estar en modo desarrollador
2. Aplicaciones → ⋮ → Actualizar lista de aplicaciones
3. Espera 1 minuto
4. Busca "Payment QR"
```

---

## Problema 2: Error al instalar el módulo

**Síntomas**: Error al hacer clic en "Instalar"

**Causa común**: Faltan dependencias de Python

**Solución**:
```bash
# Activar virtualenv de Odoo (si usas)
source /opt/odoo/venv/bin/activate

# Instalar dependencias
pip install qrcode[pil] Pillow requests

# Reiniciar Odoo
sudo systemctl restart odoo
```

---

## Problema 3: No se genera el código QR

**Síntomas**: Al seleccionar el método de pago, no aparece el QR

**Revisar**:
```bash
# Ver logs en tiempo real
sudo tail -f /var/log/odoo/odoo.log
```

**Causas posibles**:

### 3.1 Access Token incorrecto
```
Solución:
1. Ve a MercadoPago Developers
2. Verifica que copiaste el Access Token completo
3. Debe empezar con TEST- o APP_USR-
4. Vuelve a pegarlo en Odoo
```

### 3.2 Sin conexión a MercadoPago
```bash
# Probar conexión desde el servidor
curl -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  https://api.mercadopago.com/v1/payment_methods

# Debe retornar JSON, no error
```

### 3.3 Librerías de QR no instaladas
```bash
# Verificar instalación
python3 -c "import qrcode; import PIL; print('OK')"

# Si falla, instalar
pip3 install qrcode[pil] Pillow
```

---

## Problema 4: El webhook no recibe notificaciones

**Síntomas**: El pago no se confirma automáticamente en Odoo

### 4.1 Verificar que Odoo sea accesible desde internet

```bash
# Desde FUERA del servidor, probar:
curl https://tu-dominio.com/payment_qr/webhook/1/mercadopago

# Debe retornar "OK" o error de Odoo (no error de conexión)
```

### 4.2 Verificar firewall

```bash
# Ver estado del firewall
sudo ufw status

# Debe tener abierto el puerto de Odoo (ej: 8069)
# Si no está:
sudo ufw allow 8069
```

### 4.3 Verificar SSL/HTTPS

```
MercadoPago REQUIERE HTTPS para webhooks en producción.

Solución:
1. Instala certificado SSL (Let's Encrypt es gratis)
2. Configura nginx/apache como proxy reverso con HTTPS
```

**Instalar SSL con Let's Encrypt**:
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovar automáticamente
sudo certbot renew --dry-run
```

### 4.4 Verificar URL en MercadoPago

```
1. Ve a MercadoPago Developers
2. Tu aplicación → Webhooks
3. Verifica que la URL sea EXACTAMENTE:
   https://tu-dominio.com/payment_qr/webhook/1/mercadopago
4. Debe tener https:// (no http://)
5. No debe tener espacios ni caracteres extra
```

### 4.5 Ver logs del webhook

```bash
# Logs de webhooks recibidos
sudo grep "MercadoPago webhook" /var/log/odoo/odoo.log

# Debe aparecer algo como:
# INFO payment_qr.webhook: MercadoPago webhook received - Topic: payment, ID: 123456
```

---

## Problema 5: Error "No reference found in webhook"

**Síntomas**: El webhook llega pero no encuentra el pago

**Causa**: La referencia no coincide

**Solución**:
```bash
# Ver logs completos del webhook
sudo grep -A 20 "MercadoPago webhook" /var/log/odoo/odoo.log | tail -50

# Buscar:
# - external_reference en el log
# - qr_reference en la base de datos
```

En Odoo:
```
1. Ve a Transacciones QR
2. Busca la transacción pendiente
3. Revisa el campo "Referencia"
4. Debe coincidir con external_reference del webhook
```

---

## Problema 6: El pago se confirma pero no avanza el POS

**Síntomas**: El webhook funciona, pero el POS sigue esperando

**Causa**: Problema con el polling del frontend

**Revisar**:
```
1. Abre las herramientas de desarrollador del navegador (F12)
2. Ve a la pestaña "Console"
3. Busca errores en rojo
4. Debería haber llamadas cada 5 segundos a /payment_qr/check_payment
```

**Solución**:
```bash
# Limpiar caché del navegador
Ctrl + Shift + R (o Cmd + Shift + R en Mac)

# Verificar que el endpoint funcione
sudo grep "check_payment" /var/log/odoo/odoo.log

# Debe aparecer llamadas cada 5 segundos
```

---

## Problema 7: Timeout - Pago no confirmado a tiempo

**Síntomas**: "Tiempo de espera agotado"

**Causas**:
1. El cliente tardó mucho en pagar
2. El webhook llegó tarde
3. Timeout muy corto

**Solución**:
```
1. Ve a: Punto de Venta → Configuración → Métodos de Pago
2. Edita "MercadoPago QR"
3. Aumenta "Timeout" de 300 a 600 segundos (10 minutos)
4. Guardar
```

**Verificar estado manualmente**:
```
1. Ve a: Punto de Venta → Transacciones QR
2. Busca la transacción
3. Si dice "Realizado" pero el POS no avanzó:
   - Refresca el POS
   - Verifica el estado en MercadoPago
```

---

## Problema 8: Error de moneda no soportada

**Síntomas**: Error al generar QR con moneda no soportada

**Monedas soportadas por MercadoPago**:
- ARS (Argentina)
- BRL (Brasil)
- CLP (Chile)
- COP (Colombia)
- MXN (México)
- PEN (Perú)
- UYU (Uruguay)

**Solución**:
```
1. Ve a: Ajustes → General → Monedas
2. Activa la moneda de tu país
3. Ve a: Contabilidad → Configuración → Diarios
4. Edita el diario del método de pago
5. Configura la moneda correcta
```

---

## Problema 9: QR genérico en lugar de QR de MercadoPago

**Síntomas**: Se genera un QR pero no lleva a MercadoPago

**Causa**: La API de MercadoPago falló y usó fallback

**Revisar logs**:
```bash
sudo grep "Error.*MercadoPago\|Fallback" /var/log/odoo/odoo.log
```

**Causas comunes**:
1. Access Token expirado o inválido
2. Sin conexión a internet
3. API de MercadoPago caída

**Solución**:
```
1. Verifica tu Access Token en MercadoPago Developers
2. Prueba la conexión:
   curl -H "Authorization: Bearer TU_TOKEN" \
     https://api.mercadopago.com/v1/payment_methods
3. Si falla, puede ser problema temporal de MercadoPago
```

---

## Problema 10: Impresora no imprime automáticamente

**Síntomas**: El pago se confirma pero no se imprime el recibo

**Revisar configuración**:
```
1. Ve a: Punto de Venta → Configuración → Métodos de Pago
2. Edita "MercadoPago QR"
3. Verifica que "Impresión Automática" esté ✅
4. Guardar
```

**Verificar impresora del POS**:
```
1. Ve a: Punto de Venta → Configuración → Puntos de Venta
2. Edita tu POS
3. Pestaña "Recibos y facturas"
4. Verifica configuración de impresora
5. Haz una impresión de prueba
```

---

## 📊 Comandos útiles para debugging

### Ver logs en tiempo real
```bash
sudo tail -f /var/log/odoo/odoo.log | grep -i "payment_qr\|mercadopago"
```

### Ver errores recientes
```bash
sudo grep -i "error.*payment_qr" /var/log/odoo/odoo.log | tail -50
```

### Ver webhooks recibidos
```bash
sudo grep "webhook received" /var/log/odoo/odoo.log | tail -20
```

### Ver transacciones QR generadas
```bash
sudo grep "QR payment generated" /var/log/odoo/odoo.log | tail -20
```

### Verificar dependencias de Python
```bash
python3 -c "import qrcode; import PIL; import requests; print('Todas las dependencias OK')"
```

### Ver estado de Odoo
```bash
sudo systemctl status odoo
```

### Reiniciar Odoo
```bash
sudo systemctl restart odoo
```

---

## 🆘 Si nada funciona

1. **Revisa los logs completos**:
```bash
sudo tail -200 /var/log/odoo/odoo.log
```

2. **Verifica la instalación del módulo**:
```bash
ls -la /opt/odoo/addons/payment_qr
python3 -m py_compile /opt/odoo/addons/payment_qr/models/*.py
```

3. **Reinstala el módulo**:
```
En Odoo:
1. Aplicaciones → Buscar "Payment QR"
2. Desinstalar
3. Reiniciar Odoo
4. Volver a instalar
```

4. **Contacta soporte**:
- Revisa documentación: payment_qr/README.md
- Revisa guía MercadoPago: payment_qr/CONFIGURACION_MERCADOPAGO.md
- Logs de MercadoPago: https://www.mercadopago.com.ar/developers/panel

---

## ✅ Checklist de verificación

Antes de pedir ayuda, verifica:

- [ ] Módulo instalado en Odoo
- [ ] Dependencias Python instaladas (qrcode, Pillow, requests)
- [ ] Access Token correcto de MercadoPago
- [ ] Método de pago configurado con "Usar Pago QR" activado
- [ ] Webhook configurado en MercadoPago
- [ ] Servidor accesible desde internet (para webhooks)
- [ ] HTTPS configurado (para producción)
- [ ] Firewall permite tráfico al puerto de Odoo
- [ ] Método de pago asignado al POS
- [ ] Logs no muestran errores críticos
