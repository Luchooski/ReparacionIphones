# ⚡ Instalación Rápida - Payment QR MercadoPago

## 📋 Requisitos previos
- ✅ Odoo 17 Community instalado y funcionando
- ✅ Acceso SSH al servidor
- ✅ Cuenta de MercadoPago
- ✅ Dominio con HTTPS (para producción)

---

## 🚀 Instalación en 10 minutos

### 1️⃣ Clonar repositorio (1 min)
```bash
cd /tmp
git clone https://github.com/TU_USUARIO/ReparacionIphones.git
cd ReparacionIphones
```

### 2️⃣ Copiar módulo a Odoo (1 min)
```bash
# Ajusta la ruta según tu instalación
sudo cp -r payment_qr /opt/odoo/addons/
sudo chown -R odoo:odoo /opt/odoo/addons/payment_qr
```

### 3️⃣ Instalar dependencias (1 min)
```bash
# Con virtualenv
source /opt/odoo/venv/bin/activate
pip install qrcode[pil] Pillow requests

# Sin virtualenv
pip3 install qrcode[pil] Pillow requests
```

### 4️⃣ Reiniciar Odoo (1 min)
```bash
sudo systemctl restart odoo
# Espera 30 segundos
```

### 5️⃣ Obtener credenciales MercadoPago (2 min)
```
1. Ve a: https://www.mercadopago.com.ar/developers/panel
2. Inicia sesión
3. Credenciales → Credenciales de prueba
4. Copia el "Access Token" (TEST-...)
```

### 6️⃣ Instalar módulo en Odoo (2 min)
```
1. Odoo → Ajustes → Activar modo desarrollador
2. Aplicaciones → ⋮ → Actualizar lista
3. Buscar "Payment QR"
4. Instalar
```

### 7️⃣ Configurar método de pago (1 min)
```
1. Punto de Venta → Configuración → Métodos de Pago → Crear
2. Nombre: MercadoPago QR
3. ✅ Usar Pago QR
4. Proveedor: MercadoPago
5. API Key: (pegar Access Token)
6. Ambiente: Pruebas
7. Guardar
8. COPIAR la URL Webhook que aparece
```

### 8️⃣ Configurar webhook en MercadoPago (1 min)
```
1. MercadoPago Developers → Tu app → Webhooks
2. Pegar URL de Odoo
3. Eventos: ✅ Pagos ✅ Merchant Orders
4. Guardar
```

### 9️⃣ Asignar al POS (30 seg)
```
1. Punto de Venta → Configuración → Puntos de Venta
2. Editar tu POS
3. Pestaña Pagos → Agregar línea
4. Seleccionar "MercadoPago QR"
5. Guardar
```

### 🔟 ¡PROBAR! (30 seg)
```
1. Punto de Venta → Panel → Nueva Sesión
2. Agregar producto
3. Pago → MercadoPago QR
4. Escanear QR con app MercadoPago
5. Pagar con tarjeta de prueba:
   Número: 5031 7557 3453 0604
   CVV: 123
   Nombre: APRO
```

---

## ✅ Checklist de instalación

Marca cada paso completado:

- [ ] Módulo copiado a /opt/odoo/addons/
- [ ] Dependencias instaladas (qrcode, Pillow, requests)
- [ ] Odoo reiniciado
- [ ] Access Token de MercadoPago obtenido
- [ ] Módulo instalado en Odoo
- [ ] Método de pago creado y configurado
- [ ] URL Webhook copiada
- [ ] Webhook configurado en MercadoPago
- [ ] Webhook verificado (✅ activo)
- [ ] Método asignado al POS
- [ ] Venta de prueba exitosa

---

## 🎯 URLs importantes

### MercadoPago
- Panel: https://www.mercadopago.com.ar/developers/panel
- Tarjetas de prueba: https://www.mercadopago.com.ar/developers/es/docs/checkout-api/testing

### Tu Odoo
- Métodos de pago: https://tu-dominio.com/web#menu_id=XXX&model=pos.payment.method
- Transacciones QR: https://tu-dominio.com/web#menu_id=XXX&model=payment.qr.transaction
- Webhook: https://tu-dominio.com/payment_qr/webhook/1/mercadopago

---

## 🆘 Si algo falla

**No se genera el QR**:
```bash
# Ver logs
sudo tail -f /var/log/odoo/odoo.log | grep -i payment_qr

# Verificar dependencias
python3 -c "import qrcode; import PIL; import requests; print('OK')"
```

**Webhook no funciona**:
```bash
# Probar desde fuera del servidor
curl https://tu-dominio.com/payment_qr/webhook/1/mercadopago
# Debe retornar "OK"

# Verificar firewall
sudo ufw status
```

**Más ayuda**:
- Ver: `TROUBLESHOOTING.md` (solución de problemas completa)
- Ver: `CONFIGURACION_MERCADOPAGO.md` (guía detallada)

---

## 📞 Soporte

¿Problemas? Revisa en orden:
1. `TROUBLESHOOTING.md` - Soluciones a problemas comunes
2. `CONFIGURACION_MERCADOPAGO.md` - Guía paso a paso detallada
3. Logs de Odoo: `/var/log/odoo/odoo.log`
4. Panel de MercadoPago → Webhooks → Ver logs

---

## 🎉 ¡Listo!

Si completaste todos los pasos del checklist, tu sistema de pagos QR con MercadoPago está funcionando.

**Próximos pasos para producción**:
1. Obtener credenciales de producción en MercadoPago
2. Cambiar "Ambiente" a "Producción" en Odoo
3. Actualizar Access Token con credencial de producción
4. Verificar que tienes HTTPS configurado
5. Hacer ventas de prueba reales
6. ¡Empezar a vender!
