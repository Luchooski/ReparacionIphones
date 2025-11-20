# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """
    Hook que se ejecuta DESPUÉS de instalar el módulo
    Carga las vistas cuando los modelos ya están registrados
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Cargar vistas de payment.qr.transaction
    env['ir.ui.view'].create({
        'name': 'payment.qr.transaction.tree',
        'model': 'payment.qr.transaction',
        'arch': """
            <tree string="Transacciones QR" decoration-success="state=='done'"
                  decoration-danger="state=='error'" decoration-info="state=='pending'">
                <field name="name"/>
                <field name="create_date"/>
                <field name="pos_order_id"/>
                <field name="payment_method_id"/>
                <field name="amount" sum="Total"/>
                <field name="currency_id" column_invisible="1"/>
                <field name="state"/>
                <field name="provider_reference"/>
                <field name="webhook_received"/>
            </tree>
        """,
    })

    env['ir.ui.view'].create({
        'name': 'payment.qr.transaction.form',
        'model': 'payment.qr.transaction',
        'arch': """
            <form string="Transacción QR">
                <header>
                    <field name="state" widget="statusbar"
                           statusbar_visible="draft,pending,done"/>
                </header>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="pos_order_id"/>
                            <field name="pos_payment_id"/>
                            <field name="payment_method_id"/>
                        </group>
                        <group>
                            <field name="amount"/>
                            <field name="currency_id"/>
                            <field name="provider_reference"/>
                            <field name="webhook_received"/>
                            <field name="webhook_date"/>
                        </group>
                    </group>
                    <group string="Datos Técnicos">
                        <field name="qr_data"/>
                        <field name="provider_response"/>
                        <field name="error_message" invisible="not error_message"/>
                    </group>
                </sheet>
            </form>
        """,
    })

    # Crear acción para transacciones
    action = env['ir.actions.act_window'].create({
        'name': 'Transacciones QR',
        'res_model': 'payment.qr.transaction',
        'view_mode': 'tree,form',
        'help': """
            <p class="o_view_nocontent_smiling_face">
                No hay transacciones QR registradas
            </p>
            <p>
                Las transacciones QR aparecerán aquí cuando se realicen pagos
                mediante código QR en el Punto de Venta.
            </p>
        """,
    })

    # Crear menú
    pos_menu = env.ref('point_of_sale.menu_point_of_sale')
    env['ir.ui.menu'].create({
        'name': 'Transacciones QR',
        'parent_id': pos_menu.id,
        'action': f'ir.actions.act_window,{action.id}',
        'sequence': 10,
    })

    # Cargar vista para pos.payment.method con herencia
    env['ir.ui.view'].create({
        'name': 'pos.payment.method.form.qr',
        'model': 'pos.payment.method',
        'inherit_id': env.ref('point_of_sale.view_pos_payment_method_form').id,
        'arch': """
            <data>
                <xpath expr="//sheet" position="inside">
                    <group string="Configuración de Pago QR" invisible="not use_payment_qr">
                        <field name="use_payment_qr"/>
                        <group>
                            <field name="qr_provider"/>
                            <field name="qr_environment"/>
                            <field name="qr_api_key" password="True"/>
                            <field name="qr_secret_key" password="True"/>
                        </group>
                        <group>
                            <field name="qr_webhook_url" readonly="1"/>
                            <field name="qr_timeout"/>
                            <field name="qr_auto_print"/>
                        </group>
                    </group>
                </xpath>
            </data>
        """,
    })

    # Cargar permisos de seguridad
    model_transaction = env['ir.model'].search([('model', '=', 'payment.qr.transaction')], limit=1)

    if model_transaction:
        # Acceso para usuarios POS
        env['ir.model.access'].create({
            'name': 'payment.qr.transaction.user',
            'model_id': model_transaction.id,
            'group_id': env.ref('point_of_sale.group_pos_user').id,
            'perm_read': True,
            'perm_write': True,
            'perm_create': True,
            'perm_unlink': False,
        })

        # Acceso para managers POS
        env['ir.model.access'].create({
            'name': 'payment.qr.transaction.manager',
            'model_id': model_transaction.id,
            'group_id': env.ref('point_of_sale.group_pos_manager').id,
            'perm_read': True,
            'perm_write': True,
            'perm_create': True,
            'perm_unlink': True,
        })

        # Acceso público (para webhooks)
        env['ir.model.access'].create({
            'name': 'payment.qr.transaction.public',
            'model_id': model_transaction.id,
            'perm_read': True,
            'perm_write': False,
            'perm_create': False,
            'perm_unlink': False,
        })
