# -*- coding: utf-8 -*-

import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaymentQRWebhook(http.Controller):

    @http.route('/payment_qr/webhook/<int:payment_method_id>', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_payment_confirmation(self, payment_method_id, **kwargs):
        """
        Endpoint para recibir webhooks de confirmación de pago

        El proveedor de pagos debe enviar un POST a esta URL con los datos de la transacción
        """
        try:
            # Obtener datos del webhook
            data = json.loads(request.httprequest.data.decode('utf-8')) if request.httprequest.data else {}

            _logger.info(f"Webhook received for payment method {payment_method_id}: {data}")

            # Buscar el método de pago
            payment_method = request.env['pos.payment.method'].sudo().browse(payment_method_id)

            if not payment_method.exists():
                _logger.error(f"Payment method {payment_method_id} not found")
                return {'status': 'error', 'message': 'Payment method not found'}

            # Extraer referencia del pago
            reference = data.get('reference') or data.get('external_reference') or data.get('merchant_order_id')

            if not reference:
                _logger.error("No reference found in webhook data")
                return {'status': 'error', 'message': 'No reference provided'}

            # Buscar el pago correspondiente
            payment = request.env['pos.payment'].sudo().search([
                ('qr_reference', '=', reference)
            ], limit=1)

            if not payment:
                _logger.error(f"Payment with reference {reference} not found")
                return {'status': 'error', 'message': 'Payment not found'}

            # Buscar o crear transacción
            transaction = request.env['payment.qr.transaction'].sudo().search([
                ('pos_payment_id', '=', payment.id)
            ], limit=1)

            if not transaction:
                transaction = request.env['payment.qr.transaction'].sudo().create({
                    'name': reference,
                    'pos_payment_id': payment.id,
                    'payment_method_id': payment_method.id,
                    'amount': payment.amount,
                    'currency_id': payment.currency_id.id,
                    'state': 'pending',
                })

            # Procesar webhook
            transaction.process_webhook(data)

            _logger.info(f"Webhook processed successfully for payment {payment.id}")

            return {
                'status': 'success',
                'message': 'Payment confirmed',
                'payment_id': payment.id,
                'transaction_id': transaction.id
            }

        except Exception as e:
            _logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
            return {'status': 'error', 'message': str(e)}

    @http.route('/payment_qr/webhook/<int:payment_method_id>/status', type='http', auth='public', methods=['GET'])
    def webhook_status(self, payment_method_id, **kwargs):
        """
        Endpoint para verificar el estado de un pago mediante referencia
        """
        reference = kwargs.get('reference')

        if not reference:
            return json.dumps({'status': 'error', 'message': 'No reference provided'})

        payment = request.env['pos.payment'].sudo().search([
            ('qr_reference', '=', reference)
        ], limit=1)

        if not payment:
            return json.dumps({'status': 'error', 'message': 'Payment not found'})

        return json.dumps({
            'status': 'success',
            'payment_status': payment.qr_payment_status,
            'amount': payment.amount,
            'reference': payment.qr_reference,
        })

    @http.route('/payment_qr/check_payment', type='json', auth='user', methods=['POST'])
    def check_payment_status(self, reference, **kwargs):
        """
        Endpoint para que el POS verifique el estado de un pago
        Usado por polling desde el frontend
        """
        try:
            payment = request.env['pos.payment'].sudo().search([
                ('qr_reference', '=', reference)
            ], limit=1)

            if not payment:
                return {'status': 'error', 'message': 'Payment not found'}

            return {
                'status': 'success',
                'payment_status': payment.qr_payment_status,
                'approved': payment.qr_payment_status == 'approved',
                'transaction_id': payment.qr_transaction_id,
            }

        except Exception as e:
            _logger.error(f"Error checking payment status: {str(e)}", exc_info=True)
            return {'status': 'error', 'message': str(e)}
