# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaymentQRWebhook(http.Controller):

    @http.route('/payment_qr/webhook/<int:payment_method_id>/mercadopago', type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def mercadopago_webhook(self, payment_method_id, **kwargs):
        """
        Endpoint específico para notificaciones IPN de MercadoPago
        MercadoPago envía notificaciones con parámetros en query string
        """
        try:
            # MercadoPago envía parámetros en query string
            topic = kwargs.get('topic') or kwargs.get('type')
            resource_id = kwargs.get('id')

            _logger.info(f"MercadoPago webhook received - Topic: {topic}, ID: {resource_id}")

            if not topic or not resource_id:
                _logger.warning("MercadoPago webhook sin topic o ID")
                return "OK"  # MercadoPago requiere respuesta 200

            # Buscar el método de pago
            payment_method = request.env['pos.payment.method'].sudo().browse(payment_method_id)

            if not payment_method.exists():
                _logger.error(f"Payment method {payment_method_id} not found")
                return "Payment method not found"

            # Procesar según el tipo de notificación
            if topic in ['payment', 'merchant_order']:
                self._process_mercadopago_payment(payment_method, resource_id, topic)

            # MercadoPago requiere respuesta 200 OK
            return "OK"

        except Exception as e:
            _logger.error(f"Error processing MercadoPago webhook: {str(e)}", exc_info=True)
            return "OK"  # Aún así retornar OK para evitar reintentos

    def _process_mercadopago_payment(self, payment_method, resource_id, topic):
        """Procesa una notificación de pago de MercadoPago"""
        import requests

        try:
            # Obtener información del pago desde la API de MercadoPago
            if topic == 'payment':
                api_url = f"https://api.mercadopago.com/v1/payments/{resource_id}"
            else:  # merchant_order
                api_url = f"https://api.mercadopago.com/merchant_orders/{resource_id}"

            headers = {
                'Authorization': f'Bearer {payment_method.qr_api_key}'
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code != 200:
                _logger.error(f"Error al consultar MercadoPago API: {response.text}")
                return False

            payment_data = response.json()

            # Extraer external_reference
            external_reference = payment_data.get('external_reference')

            if not external_reference:
                _logger.warning(f"No external_reference en pago MercadoPago {resource_id}")
                return False

            # Buscar el pago en Odoo
            payment = request.env['pos.payment'].sudo().search([
                ('qr_reference', '=', external_reference)
            ], limit=1)

            if not payment:
                _logger.warning(f"Payment with reference {external_reference} not found")
                return False

            # Verificar estado del pago
            status = payment_data.get('status')
            _logger.info(f"MercadoPago payment {resource_id} status: {status}")

            # Buscar o crear transacción
            transaction = request.env['payment.qr.transaction'].sudo().search([
                ('pos_payment_id', '=', payment.id)
            ], limit=1)

            if not transaction:
                transaction = request.env['payment.qr.transaction'].sudo().create({
                    'name': external_reference,
                    'pos_payment_id': payment.id,
                    'payment_method_id': payment_method.id,
                    'amount': payment.amount,
                    'currency_id': payment.currency_id.id,
                    'state': 'pending',
                })

            # Actualizar transacción con datos de MercadoPago
            transaction.provider_reference = str(resource_id)
            transaction.provider_response = json.dumps(payment_data)

            # Procesar según estado
            if status == 'approved':
                payment.qr_payment_status = 'approved'
                payment.qr_transaction_id = str(resource_id)
                transaction.state = 'done'
                transaction.webhook_received = True
                transaction.webhook_date = fields.Datetime.now()

                _logger.info(f"Payment {payment.id} approved by MercadoPago")

            elif status in ['pending', 'in_process']:
                payment.qr_payment_status = 'processing'
                transaction.state = 'pending'

            elif status in ['rejected', 'cancelled']:
                payment.qr_payment_status = 'rejected'
                transaction.state = 'error'
                transaction.error_message = payment_data.get('status_detail', 'Pago rechazado')

            return True

        except Exception as e:
            _logger.error(f"Error processing MercadoPago payment: {str(e)}", exc_info=True)
            return False

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
