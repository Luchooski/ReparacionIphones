# -*- coding: utf-8 -*-
{
    'name': 'Payment QR Code - MercadoPago',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Método de pago mediante código QR para POS con MercadoPago',
    'description': """
        Módulo de Pago con Código QR para Odoo 17
        ==========================================

        Este módulo permite:
        * Pagos mediante código QR en el Punto de Venta
        * Generación dinámica de QR con el monto exacto
        * Integración completa con MercadoPago (Checkout Pro API)
        * Webhook para confirmación automática de pago
        * Impresión automática de recibo tras confirmación
        * Soporte para ambientes de prueba y producción
        * Compatible con Odoo 17 Community

        Proveedores soportados:
        * MercadoPago (Argentina, Brasil, Chile, Colombia, México, Perú, Uruguay)
        * PayPal
        * Stripe
        * Yappy
        * Personalizado
    """,
    'author': 'Tu Empresa',
    'website': 'https://www.tuempresa.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',
        'payment',
    ],
    'data': [
        'data/pos_payment_method_data.xml',
        'views/pos_payment_method_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'payment_qr/static/src/js/**/*',
            'payment_qr/static/src/xml/**/*',
            'payment_qr/static/src/css/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
