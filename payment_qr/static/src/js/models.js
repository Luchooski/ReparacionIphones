/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

/**
 * Extender PosStore para manejar métodos de pago QR
 */
patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);

        // Procesar métodos de pago QR
        if (loadedData['pos.payment.method']) {
            for (const method of loadedData['pos.payment.method']) {
                if (method.use_payment_qr) {
                    method.use_payment_terminal = true;
                    method.payment_terminal_interface = 'payment_qr';
                }
            }
        }
    },
});

/**
 * Extender Payment para agregar campos QR
 */
patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.qr_reference = this.qr_reference || null;
        this.qr_transaction_id = this.qr_transaction_id || null;
        this.qr_payment_status = this.qr_payment_status || 'pending';
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.qr_reference = this.qr_reference;
        json.qr_transaction_id = this.qr_transaction_id;
        json.qr_payment_status = this.qr_payment_status;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.qr_reference = json.qr_reference;
        this.qr_transaction_id = json.qr_transaction_id;
        this.qr_payment_status = json.qr_payment_status;
    },

    setQRReference(reference) {
        this.qr_reference = reference;
    },

    setQRTransactionId(transactionId) {
        this.qr_transaction_id = transactionId;
    },

    setQRPaymentStatus(status) {
        this.qr_payment_status = status;
    },
});
