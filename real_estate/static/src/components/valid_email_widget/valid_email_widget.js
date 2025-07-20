/** @odoo-module **/

import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { EmailField, emailField } from "@web/views/fields/email/email_field";

class ValidEmailField extends EmailField {
    static template = "real_estate.ValidemailWidget";

    setup() {
        super.setup();
        const email = this.props.record.data[this.props.name] || "";
        this.state = useState({
            isValid: this._validateEmail(email),
        });
        console.log("eee")
    }

    _validateEmail(value) {
        if (!value || value.trim() === "") {
            return true; // Consider empty as valid to avoid showing error initially
        }
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(value.trim());
    }

    // Handle input events for real-time validation
    onInput(ev) {
        const value = ev.target.value;
        this.state.isValid = this._validateEmail(value);
    }
}

export const validemailField = {
    ...emailField,
    component: ValidEmailField,
};

registry.category("fields").add("valid_email", validemailField);
registry.category("fields").add("form.valid_email", validemailField);
