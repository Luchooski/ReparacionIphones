# 🚀 Guía de Instalación Completa - Payment QR MercadoPago

## ✨ ¿Qué hay de nuevo en esta versión mejorada?

Esta versión mejorada del módulo ahora incluye **todas las funcionalidades completas**:

### Mejoras implementadas:
- ✅ **Vistas completas**: Ahora tendrás acceso a todas las vistas de transacciones QR
- ✅ **Menús funcionales**: Menú "Transacciones QR" bajo Punto de Venta
- ✅ **Seguridad configurada**: Permisos para usuarios POS y managers
- ✅ **Configuración de métodos de pago**: Vista mejorada para configurar QR en métodos de pago
- ✅ **Compatible con instalación ZIP**: Usa hooks post-instalación para cargar todo correctamente

### Cómo funciona la mejora:
El módulo ahora usa un **post_init_hook** que se ejecuta DESPUÉS de que todos los modelos están registrados. Esto soluciona el problema de timing que ocurría al instalar desde ZIP.

---

## 📋 Paso 1: Desinstalar versión anterior (si existe)

Si ya instalaste la versión básica del módulo:

1. Ve a **Aplicaciones** en Odoo
2. Busca "Payment QR"
3. Haz clic en el módulo y selecciona **Desinstalar**
4. Confirma la desinstalación

---

## 📦 Paso 2: Instalar el módulo mejorado

1. **Descarga el archivo**: `payment_qr_mejorado.zip`

2. **Importar en Odoo**:
   - Ve a **Aplicaciones**
   - Activa el modo desarrollador (si no está activo)
   - Actualiza la lista de aplicaciones
   - Busca la opción de **importar módulo** o **subir módulo**
   - Selecciona el archivo `payment_qr_mejorado.zip`
   - Haz clic en **Importar**

3. **Instalar**:
   - Una vez importado, busca "Payment QR Code - MercadoPago"
   - Haz clic en **Instalar**
   - El módulo se instalará y ejecutará automáticamente el hook de post-instalación

4. **Verificar instalación**:
   - Ve a **Punto de Venta** en el menú principal
   - Deberías ver un nuevo submenú: **Transacciones QR**
   - Si lo ves, ¡la instalación fue exitosa!

---

## 🐍 Paso 3: Instalar dependencias de Python

**IMPORTANTE**: El módulo necesita 3 librerías de Python para funcionar. Necesitarás contactar al administrador del servidor.

### Envía este mensaje al administrador:

```
Hola,

Necesito instalar las siguientes dependencias de Python para el módulo
"Payment QR Code - MercadoPago" en Odoo 17:

pip install qrcode[pil]>=7.3.1 Pillow>=9.0.0 requests>=2.28.0

Después de instalar, por favor reinicia el servicio de Odoo.

Gracias
```

### Instrucciones para el administrador:

**Si usa virtualenv de Odoo:**
```bash
source /ruta/al/venv/bin/activate
pip install qrcode[pil] Pillow requests
sudo systemctl restart odoo
```

**Si NO usa virtualenv:**
```bash
pip3 install qrcode[pil] Pillow requests
sudo systemctl restart odoo
```

**Si es Odoo.sh:**
Crea un archivo `requirements.txt` en la raíz con:
```
qrcode[pil]>=7.3.1
Pillow>=9.0.0
requests>=2.28.0
```

### Verificar instalación de dependencias:
El administrador puede verificar con:
```bash
python3 -c "import qrcode; import PIL; import requests; print('✅ OK')"
```

---

## 🔑 Paso 4: Configurar MercadoPago

### 4.1 Obtener credenciales de MercadoPago

1. **Accede a tu cuenta de MercadoPago**:
   - Argentina: https://www.mercadopago.com.ar
   - México: https://www.mercadopago.com.mx
   - (otros países: usa tu dominio local)

2. **Ve a "Tus integraciones"**:
   - Menú → Configuración → Tus integraciones
   - O directamente: https://www.mercadopago.com/developers/panel

3. **Crea una aplicación**:
   - Clic en "Crear aplicación"
   - Nombre: "POS Odoo - [Tu negocio]"
   - Tipo: "Pagos online"

4. **Obtén tus credenciales**:
   - **Access Token de Prueba**: Para testing
   - **Access Token de Producción**: Para uso real

---

### 4.2 Configurar método de pago en Odoo

1. **Ve a Punto de Venta → Configuración → Métodos de Pago**

2. **Crea un nuevo método de pago**:
   - Haz clic en **Crear**
   - **Nombre**: "MercadoPago QR"

3. **Configuración QR**:
   - ✅ Activa: **Usar Pago QR**
   - **Proveedor QR**: Selecciona "MercadoPago"
   - **Ambiente**:
     - Selecciona "Prueba" para testing
     - Selecciona "Producción" cuando estés listo
   - **API Key**: Pega tu Access Token de MercadoPago
   - **Secret Key**: (Opcional, solo si usas validación adicional)

4. **Configuración avanzada**:
   - **Timeout**: 300 segundos (5 minutos por defecto)
   - **Auto-imprimir**: ✅ Activar si quieres impresión automática

5. **URL del Webhook**:
   - Se generará automáticamente
   - Copia esta URL (la necesitarás en el siguiente paso)

6. **Guarda** el método de pago

---

### 4.3 Configurar Webhook en MercadoPago

1. **Accede al panel de desarrolladores de MercadoPago**:
   - https://www.mercadopago.com/developers/panel/app

2. **Selecciona tu aplicación**

3. **Ve a "Webhooks" o "Notificaciones IPN"**

4. **Configura la URL de notificación**:
   - **URL**: Pega la URL que copiaste de Odoo
   - Formato: `https://tu-servidor.com/payment_qr/webhook/[ID]/mercadopago`
   - **Eventos**: Selecciona "Pagos"

5. **Guarda** la configuración

---

## 🛒 Paso 5: Configurar en tu sesión de POS

1. **Ve a Punto de Venta → Configuración → Punto de Venta**

2. **Edita tu punto de venta activo**

3. **En la pestaña "Pagos"**:
   - Añade el método de pago "MercadoPago QR"

4. **Guarda** la configuración

5. **Abre una nueva sesión de POS**

---

## ✅ Paso 6: Probar el sistema

### Prueba básica:

1. **Abre el POS**

2. **Crea una venta de prueba**:
   - Añade un producto
   - Haz clic en **Pago**

3. **Selecciona "MercadoPago QR"**

4. **Debería aparecer**:
   - Un código QR en pantalla
   - Instrucciones para el cliente

5. **Escanea el QR con tu app de MercadoPago**:
   - Usa la app de MercadoPago en modo prueba
   - Completa el pago

6. **Verifica la confirmación**:
   - El sistema debería detectar el pago automáticamente (cada 5 segundos)
   - El recibo se imprimirá automáticamente (si está configurado)
   - La venta se completará

---

## 🔍 Verificar transacciones

Después de realizar pagos, puedes ver todas las transacciones:

1. **Ve a Punto de Venta → Transacciones QR**

2. **Verás una lista con**:
   - Fecha y hora
   - Orden POS asociada
   - Monto
   - Estado (Pendiente, Completado, Error)
   - Referencia del proveedor
   - Si se recibió el webhook

3. **Haz clic en una transacción** para ver detalles completos:
   - Datos QR generados
   - Respuesta del proveedor
   - Mensajes de error (si hubo)

---

## 🆘 Solución de problemas

### Problema 1: No aparece el código QR
**Causa**: Dependencias de Python no instaladas
**Solución**: Verifica que el administrador instaló qrcode, Pillow y requests

### Problema 2: El webhook no se recibe
**Causa**: URL del webhook no configurada en MercadoPago
**Solución**: Verifica la configuración del webhook en el panel de MercadoPago

### Problema 3: Error "API Key inválida"
**Causa**: Token incorrecto o ambiente incorrecto
**Solución**:
- Verifica que usas el Access Token correcto
- Si estás en "Prueba", usa el token de prueba
- Si estás en "Producción", usa el token de producción

### Problema 4: El pago no se confirma automáticamente
**Causa**: Webhook no configurado o firewall bloqueando
**Solución**:
- Verifica que MercadoPago puede acceder a tu servidor
- Revisa los logs de Odoo para ver si llegó la notificación
- Verifica que el puerto HTTPS (443) esté abierto

---

## 📞 Soporte

Si tienes problemas con la instalación o configuración:

1. **Revisa los logs de Odoo** (pide al administrador):
   ```bash
   tail -f /var/log/odoo/odoo-server.log
   ```

2. **Verifica el estado del módulo**:
   - Ve a Aplicaciones
   - Busca "Payment QR"
   - Verifica que está instalado y actualizado

3. **Comprueba las transacciones**:
   - Ve a Punto de Venta → Transacciones QR
   - Revisa los mensajes de error en transacciones fallidas

---

## 📚 Documentación adicional

- **CONFIGURACION_MERCADOPAGO.md**: Guía detallada de MercadoPago
- **INTEGRACIONES.md**: Cómo integrar otros proveedores
- **MENSAJE_PARA_ADMINISTRADOR.md**: Instrucciones para el administrador del servidor

---

## 🎉 ¡Listo!

Si seguiste todos los pasos, tu sistema de pagos QR con MercadoPago debería estar funcionando perfectamente.

**Características disponibles**:
- ✅ Generación dinámica de QR con monto exacto
- ✅ Confirmación automática vía webhook
- ✅ Impresión automática de recibos
- ✅ Tracking completo de transacciones
- ✅ Soporte para ambiente de pruebas y producción
- ✅ Interfaz intuitiva en el POS

**¡Disfruta de tu nuevo sistema de pagos!**
