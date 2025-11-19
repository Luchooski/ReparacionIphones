/** @odoo-module **/

import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

/**
 * Payment QR Interface
 * Maneja la lógica de pagos mediante código QR
 */
export class PaymentQR extends PaymentInterface {
    setup() {
        super.setup();
        this.pollingInterval = null;
        this.maxPollingAttempts = 60; // 60 intentos = 5 minutos (5 segundos por intento)
        this.pollingAttempts = 0;
    }

    /**
     * Envía el pago al servidor
     */
    async send_payment_request(cid) {
        await super.send_payment_request(cid);

        const line = this.pos.get_order().get_paymentline(cid);
        const order = this.pos.get_order();

        if (!line || !line.payment_method.use_payment_qr) {
            return this._handle_odoo_connection_failure();
        }

        try {
            // Generar el QR en el servidor
            const qrData = await this._generateQRCode(line, order);

            if (!qrData || !qrData.qr_image) {
                return this._showErrorMessage(_t("Error al generar el código QR"));
            }

            // Mostrar el QR en pantalla
            this._displayQRCode(qrData);

            // Iniciar polling para verificar el estado del pago
            this._startPaymentPolling(qrData.reference);

            return true;

        } catch (error) {
            console.error("Error en send_payment_request:", error);
            return this._showErrorMessage(_t("Error al procesar el pago QR"));
        }
    }

    /**
     * Genera el código QR en el servidor
     */
    async _generateQRCode(line, order) {
        try {
            const data = {
                payment_method_id: line.payment_method.id,
                amount: line.amount,
                currency_id: this.pos.currency.id,
                order_id: order.uid,
                order_name: order.name,
            };

            const result = await this.env.services.rpc({
                model: 'pos.payment',
                method: 'generate_qr_payment',
                args: [[line.id]],
            });

            return result;

        } catch (error) {
            console.error("Error al generar QR:", error);
            return false;
        }
    }

    /**
     * Muestra el código QR en pantalla
     */
    _displayQRCode(qrData) {
        const qrContainer = document.querySelector('.payment-qr-container');

        if (qrContainer) {
            qrContainer.innerHTML = `
                <div class="qr-payment-display">
                    <h3>${_t("Escanea el código QR para pagar")}</h3>
                    <img src="data:image/png;base64,${qrData.qr_image}"
                         alt="QR Code"
                         class="qr-code-image"/>
                    <p class="qr-amount">Monto: ${this.pos.format_currency(qrData.amount)}</p>
                    <p class="qr-reference">Ref: ${qrData.reference}</p>
                    <div class="qr-status">
                        <span class="spinner"></span>
                        <span>${_t("Esperando confirmación de pago...")}</span>
                    </div>
                </div>
            `;
        }
    }

    /**
     * Inicia el polling para verificar el estado del pago
     */
    _startPaymentPolling(reference) {
        this.pollingAttempts = 0;

        this.pollingInterval = setInterval(async () => {
            this.pollingAttempts++;

            try {
                const result = await this.env.services.rpc({
                    route: '/payment_qr/check_payment',
                    params: { reference: reference },
                });

                if (result.approved) {
                    this._handlePaymentApproved(result);
                } else if (result.payment_status === 'rejected') {
                    this._handlePaymentRejected();
                } else if (this.pollingAttempts >= this.maxPollingAttempts) {
                    this._handlePaymentTimeout();
                }

            } catch (error) {
                console.error("Error al verificar estado del pago:", error);
                if (this.pollingAttempts >= this.maxPollingAttempts) {
                    this._handlePaymentTimeout();
                }
            }

        }, 5000); // Verificar cada 5 segundos
    }

    /**
     * Detiene el polling
     */
    _stopPaymentPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    /**
     * Maneja un pago aprobado
     */
    _handlePaymentApproved(result) {
        this._stopPaymentPolling();
        this._showSuccessMessage(_t("Pago confirmado"));

        // Marcar el pago como exitoso
        const line = this.pos.get_order().selected_paymentline;
        if (line) {
            line.set_payment_status('done');
            line.transaction_id = result.transaction_id;
        }

        // Si está configurado, imprimir el recibo automáticamente
        if (line.payment_method.qr_auto_print) {
            this._autoPrintReceipt();
        }
    }

    /**
     * Maneja un pago rechazado
     */
    _handlePaymentRejected() {
        this._stopPaymentPolling();
        this._showErrorMessage(_t("Pago rechazado"));

        const line = this.pos.get_order().selected_paymentline;
        if (line) {
            line.set_payment_status('retry');
        }
    }

    /**
     * Maneja un timeout del pago
     */
    _handlePaymentTimeout() {
        this._stopPaymentPolling();
        this._showErrorMessage(_t("Tiempo de espera agotado. Por favor, intente de nuevo."));

        const line = this.pos.get_order().selected_paymentline;
        if (line) {
            line.set_payment_status('timeout');
        }
    }

    /**
     * Imprime el recibo automáticamente
     */
    async _autoPrintReceipt() {
        try {
            const order = this.pos.get_order();
            if (order && order.is_paid()) {
                await this.pos.push_and_invoice_order(order);
                // El recibo se imprimirá automáticamente si está configurado en el POS
            }
        } catch (error) {
            console.error("Error al imprimir recibo:", error);
        }
    }

    /**
     * Muestra un mensaje de error
     */
    _showErrorMessage(message) {
        this.env.services.notification.add(message, {
            type: 'danger',
        });
        return false;
    }

    /**
     * Muestra un mensaje de éxito
     */
    _showSuccessMessage(message) {
        this.env.services.notification.add(message, {
            type: 'success',
        });
    }

    /**
     * Cancela el pago
     */
    send_payment_cancel() {
        super.send_payment_cancel();
        this._stopPaymentPolling();

        // Limpiar la visualización del QR
        const qrContainer = document.querySelector('.payment-qr-container');
        if (qrContainer) {
            qrContainer.innerHTML = '';
        }
    }
}

// Registrar el payment interface
registry.category("payment_methods").add("payment_qr", PaymentQR);
