# Guía de Integraciones con Proveedores de Pago QR

Esta guía detalla cómo implementar integraciones específicas con diferentes proveedores de pago QR.

## 📱 MercadoPago (América Latina)

### Configuración

1. Crear una cuenta en [MercadoPago Developers](https://www.mercadopago.com/developers)
2. Obtener las credenciales:
   - **Access Token** (API Key)
   - **Public Key** (opcional, para frontend)

### Implementación

```python
# En models/pos_payment_method.py - Método _get_mercadopago_qr()

import mercadopago

def _get_mercadopago_qr(self, amount, currency, reference):
    """Implementación para MercadoPago"""

    # Inicializar SDK
    sdk = mercadopago.SDK(self.qr_api_key)

    # Crear preferencia de pago
    preference_data = {
        "items": [
            {
                "title": f"Pago POS - {reference}",
                "quantity": 1,
                "unit_price": float(amount),
                "currency_id": currency.name
            }
        ],
        "external_reference": reference,
        "notification_url": self.qr_webhook_url,
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    # Generar QR con la URL de pago
    import qrcode
    from io import BytesIO
    import base64

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(preference["init_point"])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return {
        'qr_image': qr_image,
        'payment_url': preference["init_point"],
        'preference_id': preference["id"],
        'reference': reference,
        'amount': amount,
        'currency': currency.name,
    }
```

### Webhook MercadoPago

```python
# En controllers/webhook.py - Agregar validación de firma

import hashlib
import hmac

def _validate_mercadopago_webhook(self, data, signature):
    """Valida la firma del webhook de MercadoPago"""
    secret = self.payment_method_id.qr_secret_key

    # Construir string a firmar
    data_string = f"{data['id']}{data['external_reference']}"

    # Calcular firma
    expected_signature = hmac.new(
        secret.encode(),
        data_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature == expected_signature
```

### Dependencias adicionales

```bash
pip install mercadopago
```

---

## 💳 PayPal

### Configuración

1. Crear una cuenta en [PayPal Developer](https://developer.paypal.com/)
2. Crear una aplicación en el Dashboard
3. Obtener:
   - **Client ID** (API Key)
   - **Client Secret** (Secret Key)

### Implementación

```python
def _get_paypal_qr(self, amount, currency, reference):
    """Implementación para PayPal"""
    import requests
    from requests.auth import HTTPBasicAuth

    # Obtener token de acceso
    auth_url = "https://api-m.paypal.com/v1/oauth2/token"
    if self.qr_environment == 'test':
        auth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

    auth_response = requests.post(
        auth_url,
        auth=HTTPBasicAuth(self.qr_api_key, self.qr_secret_key),
        data={'grant_type': 'client_credentials'}
    )

    access_token = auth_response.json()['access_token']

    # Crear orden de pago
    order_url = "https://api-m.paypal.com/v2/checkout/orders"
    if self.qr_environment == 'test':
        order_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "reference_id": reference,
            "amount": {
                "currency_code": currency.name,
                "value": f"{amount:.2f}"
            }
        }],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "return_url": f"{self.qr_webhook_url}/success",
                    "cancel_url": f"{self.qr_webhook_url}/cancel",
                }
            }
        }
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    order_response = requests.post(order_url, json=order_data, headers=headers)
    order = order_response.json()

    # Obtener link de pago
    payment_url = next(
        link['href'] for link in order['links']
        if link['rel'] == 'approve'
    )

    # Generar QR
    import qrcode
    from io import BytesIO
    import base64

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payment_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return {
        'qr_image': qr_image,
        'payment_url': payment_url,
        'order_id': order['id'],
        'reference': reference,
        'amount': amount,
        'currency': currency.name,
    }
```

---

## 🇵🇦 Yappy (Panamá)

### Configuración

1. Solicitar acceso a la API de Yappy para comercios
2. Obtener credenciales de la plataforma Yappy Business

### Implementación

```python
def _get_yappy_qr(self, amount, currency, reference):
    """Implementación para Yappy"""
    import requests

    # API de Yappy (ejemplo - verificar documentación oficial)
    api_url = "https://api.yappy.com.pa/v1/payment/qr"

    payload = {
        "merchantId": self.qr_api_key,
        "amount": float(amount),
        "reference": reference,
        "callbackUrl": self.qr_webhook_url,
    }

    headers = {
        'Authorization': f'Bearer {self.qr_secret_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    data = response.json()

    # Yappy retorna directamente el QR en base64
    return {
        'qr_image': data['qrImage'],
        'payment_id': data['paymentId'],
        'reference': reference,
        'amount': amount,
        'currency': currency.name,
    }
```

---

## 🔄 Stripe

### Configuración

1. Crear cuenta en [Stripe](https://stripe.com/)
2. Obtener las API keys desde el Dashboard
3. Activar Stripe Payment Links o QR Codes

### Implementación

```python
def _get_stripe_qr(self, amount, currency, reference):
    """Implementación para Stripe"""
    import stripe

    stripe.api_key = self.qr_secret_key

    # Crear una sesión de checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currency.name.lower(),
                'product_data': {
                    'name': f'Pago POS - {reference}',
                },
                'unit_amount': int(amount * 100),  # Stripe usa centavos
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{self.qr_webhook_url}/success',
        cancel_url=f'{self.qr_webhook_url}/cancel',
        client_reference_id=reference,
    )

    # Generar QR con la URL de la sesión
    import qrcode
    from io import BytesIO
    import base64

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(session.url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return {
        'qr_image': qr_image,
        'payment_url': session.url,
        'session_id': session.id,
        'reference': reference,
        'amount': amount,
        'currency': currency.name,
    }
```

### Dependencias

```bash
pip install stripe
```

---

## 🔧 Proveedor Personalizado

### Plantilla de implementación

```python
def _get_custom_qr(self, amount, currency, reference):
    """Implementación personalizada"""
    import requests
    import qrcode
    from io import BytesIO
    import base64

    # 1. Llamar a tu API de pagos
    api_url = "https://tu-proveedor.com/api/create-payment"

    payload = {
        "amount": float(amount),
        "currency": currency.name,
        "reference": reference,
        "webhook_url": self.qr_webhook_url,
    }

    headers = {
        'Authorization': f'Bearer {self.qr_api_key}',
        'X-Secret-Key': self.qr_secret_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    payment_data = response.json()

    # 2. Generar QR con la URL o datos del pago
    payment_url = payment_data.get('payment_url')

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payment_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    # 3. Retornar datos
    return {
        'qr_image': qr_image,
        'payment_url': payment_url,
        'payment_id': payment_data.get('id'),
        'reference': reference,
        'amount': amount,
        'currency': currency.name,
    }
```

---

## 🔐 Validación de Webhooks

### Ejemplo de validación con firma HMAC

```python
import hmac
import hashlib

def validate_webhook_signature(data, signature, secret_key):
    """Valida la firma del webhook"""

    # Crear string a firmar (ajustar según proveedor)
    message = f"{data['reference']}{data['amount']}{data['status']}"

    # Calcular firma
    expected_signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)
```

---

## 🧪 Testing

### Webhook de prueba con curl

```bash
curl -X POST \
  https://tu-dominio.com/payment_qr/webhook/1 \
  -H 'Content-Type: application/json' \
  -d '{
    "reference": "POS-1-123-456789",
    "status": "approved",
    "transaction_id": "TEST-123",
    "amount": 100.00
  }'
```

### Verificar estado de pago

```bash
curl https://tu-dominio.com/payment_qr/webhook/1/status?reference=POS-1-123-456789
```

---

## 📚 Recursos adicionales

### MercadoPago
- [Documentación oficial](https://www.mercadopago.com/developers/es/docs)
- [SDK Python](https://github.com/mercadopago/sdk-python)

### PayPal
- [Documentación oficial](https://developer.paypal.com/docs/)
- [API Reference](https://developer.paypal.com/api/rest/)

### Stripe
- [Documentación oficial](https://stripe.com/docs)
- [Python Library](https://github.com/stripe/stripe-python)

### Yappy
- Contactar a Yappy Business para documentación de API

---

## ⚠️ Notas importantes

1. **Seguridad**: Siempre validar las firmas de los webhooks
2. **Timeouts**: Configurar timeouts apropiados para cada proveedor
3. **Logs**: Registrar todas las transacciones para auditoría
4. **Testing**: Probar exhaustivamente en ambiente de pruebas antes de producción
5. **Certificados SSL**: Asegurar que el servidor tenga un certificado SSL válido
