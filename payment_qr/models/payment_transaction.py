# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentQRTransaction(models.Model):
    _name = 'payment.qr.transaction'
    _description = 'Transacción de Pago QR'
    _order = 'create_date desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        readonly=True,
        copy=False,
        default='/'
    )

    pos_payment_id = fields.Many2one(
        'pos.payment',
        string='Pago POS',
        ondelete='cascade'
    )

    pos_order_id = fields.Many2one(
        'pos.order',
        string='Orden POS',
        related='pos_payment_id.pos_order_id',
        store=True
    )

    payment_method_id = fields.Many2one(
        'pos.payment.method',
        string='Método de Pago',
        required=True
    )

    amount = fields.Monetary(
        string='Monto',
        required=True,
        currency_field='currency_id'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('pending', 'Pendiente'),
        ('done', 'Realizado'),
        ('cancelled', 'Cancelado'),
        ('error', 'Error'),
    ], string='Estado', default='draft', required=True)

    provider_reference = fields.Char(
        string='Referencia del Proveedor',
        help='ID de transacción del proveedor de pagos'
    )

    provider_response = fields.Text(
        string='Respuesta del Proveedor',
        help='Respuesta completa del proveedor de pagos'
    )

    qr_data = fields.Text(
        string='Datos QR',
        help='Datos codificados en el QR'
    )

    webhook_received = fields.Boolean(
        string='Webhook Recibido',
        default=False
    )

    webhook_date = fields.Datetime(
        string='Fecha Webhook'
    )

    error_message = fields.Text(
        string='Mensaje de Error'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.qr.transaction') or '/'
        return super(PaymentQRTransaction, self).create(vals)

    def process_webhook(self, webhook_data):
        """Procesa los datos recibidos del webhook"""
        self.ensure_one()

        self.webhook_received = True
        self.webhook_date = fields.Datetime.now()
        self.provider_response = str(webhook_data)

        # Extraer información relevante según el proveedor
        status = webhook_data.get('status')
        transaction_id = webhook_data.get('transaction_id') or webhook_data.get('id')

        if transaction_id:
            self.provider_reference = transaction_id

        # Actualizar estado según la respuesta
        if status in ['approved', 'success', 'completed']:
            self.state = 'done'
            if self.pos_payment_id:
                self.pos_payment_id.confirm_qr_payment({
                    'transaction_id': transaction_id,
                    'status': status
                })
        elif status in ['rejected', 'failed']:
            self.state = 'error'
            self.error_message = webhook_data.get('error_message', 'Pago rechazado')
        elif status in ['pending', 'in_process']:
            self.state = 'pending'
        elif status in ['cancelled']:
            self.state = 'cancelled'

        return True
