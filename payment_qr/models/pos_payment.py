# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    qr_transaction_id = fields.Char(
        string='ID Transacción QR',
        help='ID de la transacción del proveedor QR'
    )

    qr_payment_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado Pago QR', default='pending')

    qr_image_data = fields.Text(
        string='Datos Imagen QR',
        help='Datos de la imagen QR en base64'
    )

    qr_payment_url = fields.Char(
        string='URL de Pago',
        help='URL para realizar el pago'
    )

    qr_reference = fields.Char(
        string='Referencia QR',
        help='Referencia única del pago QR'
    )

    qr_preference_id = fields.Char(
        string='Preference ID',
        help='ID de preferencia de MercadoPago (o equivalente del proveedor)'
    )

    def generate_qr_payment(self):
        """Genera el código QR para el pago"""
        self.ensure_one()

        if not self.payment_method_id.use_payment_qr:
            return False

        # Generar referencia única
        reference = f"POS-{self.pos_order_id.id}-{self.id}-{fields.Datetime.now().timestamp()}"
        self.qr_reference = reference

        # Obtener información del QR del método de pago
        qr_info = self.payment_method_id._get_payment_qr_info(
            amount=self.amount,
            currency=self.currency_id,
            reference=reference
        )

        if qr_info:
            self.qr_image_data = qr_info.get('qr_image', '')
            self.qr_payment_url = qr_info.get('payment_url', '')
            self.qr_preference_id = qr_info.get('preference_id', '')
            self.qr_payment_status = 'pending'

            _logger.info(f"QR payment generated for order {self.pos_order_id.name}: {reference}")

            return qr_info

        return False

    def confirm_qr_payment(self, transaction_data):
        """Confirma el pago QR recibido desde el webhook"""
        self.ensure_one()

        _logger.info(f"Confirming QR payment for reference: {self.qr_reference}")

        self.qr_transaction_id = transaction_data.get('transaction_id')
        self.qr_payment_status = 'approved'

        # Marcar el pago como realizado
        if self.pos_order_id:
            self.pos_order_id.action_pos_order_paid()

        return True

    def cancel_qr_payment(self):
        """Cancela el pago QR"""
        self.ensure_one()
        self.qr_payment_status = 'cancelled'
        _logger.info(f"QR payment cancelled for reference: {self.qr_reference}")
