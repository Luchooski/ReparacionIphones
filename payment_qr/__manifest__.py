# -*- coding: utf-8 -*-
{
    'name': 'Payment QR Code',
    'version': '1.0.0',
    'category': 'Point of Sale',
    'summary': 'Método de pago mediante código QR para POS',
    'description': """
        Módulo de Pago con Código QR
        =============================

        Este módulo permite:
        * Pagos mediante código QR en el Punto de Venta
        * Generación dinámica de QR con el monto exacto
        * Webhook para confirmación automática de pago
        * Impresión automática de recibo tras confirmación

        El módulo soporta integración con diversos proveedores de pago QR.
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
        'security/ir.model.access.csv',
        'views/pos_payment_method_views.xml',
        'data/pos_payment_method_data.xml',
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
