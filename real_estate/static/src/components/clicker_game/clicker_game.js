/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

class ClickerGame extends Component {
    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
    }

    reset() {
        this.state.count = 0;
    }

    static template = "real_estate.ClickerGame";
}

registry.category("actions").add("real_estate.real_estate_clicker_page", ClickerGame);
