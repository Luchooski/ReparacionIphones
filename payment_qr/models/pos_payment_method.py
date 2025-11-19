# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    use_payment_qr = fields.Boolean(
        string='Usar Pago QR',
        help='Habilitar pago mediante código QR'
    )

    qr_provider = fields.Selection([
        ('mercadopago', 'MercadoPago'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('yappy', 'Yappy'),
        ('custom', 'Personalizado'),
    ], string='Proveedor QR', default='mercadopago')

    qr_api_key = fields.Char(
        string='API Key',
        help='Clave API del proveedor de pagos'
    )

    qr_secret_key = fields.Char(
        string='Secret Key',
        help='Clave secreta del proveedor de pagos'
    )

    qr_webhook_url = fields.Char(
        string='URL Webhook',
        compute='_compute_webhook_url',
        store=False,
        help='URL donde el proveedor enviará las notificaciones de pago'
    )

    qr_environment = fields.Selection([
        ('test', 'Pruebas'),
        ('production', 'Producción'),
    ], string='Ambiente', default='test')

    qr_timeout = fields.Integer(
        string='Timeout (segundos)',
        default=300,
        help='Tiempo máximo de espera para confirmar el pago'
    )

    qr_auto_print = fields.Boolean(
        string='Impresión Automática',
        default=True,
        help='Imprimir recibo automáticamente tras confirmar el pago'
    )

    @api.depends('company_id')
    def _compute_webhook_url(self):
        """Compute the webhook URL for payment confirmations"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            record.qr_webhook_url = f"{base_url}/payment_qr/webhook/{record.id}"

    def _get_payment_qr_info(self, amount, currency, reference):
        """
        Genera la información necesaria para crear el QR de pago

        :param amount: Monto a cobrar
        :param currency: Moneda
        :param reference: Referencia del pago
        :return: dict con la información del QR
        """
        self.ensure_one()

        if not self.use_payment_qr:
            return {}

        # Aquí se implementa la lógica específica de cada proveedor
        if self.qr_provider == 'mercadopago':
            return self._get_mercadopago_qr(amount, currency, reference)
        elif self.qr_provider == 'paypal':
            return self._get_paypal_qr(amount, currency, reference)
        elif self.qr_provider == 'stripe':
            return self._get_stripe_qr(amount, currency, reference)
        elif self.qr_provider == 'yappy':
            return self._get_yappy_qr(amount, currency, reference)
        else:
            return self._get_custom_qr(amount, currency, reference)

    def _get_mercadopago_qr(self, amount, currency, reference):
        """Implementación para MercadoPago"""
        # TODO: Implementar integración con MercadoPago
        import qrcode
        from io import BytesIO
        import base64

        # URL de pago de MercadoPago (ejemplo)
        payment_url = f"https://www.mercadopago.com/checkout/v1/payment?amount={amount}&reference={reference}"

        # Generar QR
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
            'reference': reference,
            'amount': amount,
            'currency': currency.name,
        }

    def _get_paypal_qr(self, amount, currency, reference):
        """Implementación para PayPal"""
        # TODO: Implementar integración con PayPal
        return self._get_generic_qr(amount, currency, reference, 'paypal')

    def _get_stripe_qr(self, amount, currency, reference):
        """Implementación para Stripe"""
        # TODO: Implementar integración con Stripe
        return self._get_generic_qr(amount, currency, reference, 'stripe')

    def _get_yappy_qr(self, amount, currency, reference):
        """Implementación para Yappy"""
        # TODO: Implementar integración con Yappy
        return self._get_generic_qr(amount, currency, reference, 'yappy')

    def _get_custom_qr(self, amount, currency, reference):
        """Implementación personalizada"""
        return self._get_generic_qr(amount, currency, reference, 'custom')

    def _get_generic_qr(self, amount, currency, reference, provider):
        """Generador genérico de QR"""
        import qrcode
        from io import BytesIO
        import base64

        # Datos del pago en formato JSON
        payment_data = f"provider={provider}&amount={amount}&currency={currency.name}&ref={reference}"

        # Generar QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(payment_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_image = base64.b64encode(buffer.getvalue()).decode()

        return {
            'qr_image': qr_image,
            'payment_data': payment_data,
            'reference': reference,
            'amount': amount,
            'currency': currency.name,
        }
