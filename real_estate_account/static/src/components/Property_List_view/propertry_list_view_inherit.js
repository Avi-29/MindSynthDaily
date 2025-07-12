/** @odoo-module */

import { registry } from "@web/core/registry"
import { listView } from "@web/views/list/list_view"
import { ListController } from "@web/views/list/list_controller"

class PropertyListController extends ListController{
     setup(){
     super.setup()
     console.log("Eeeee")
     }
    viewInvoices() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            name: "Customer Invoices",
            res_model: "account.move",
            views: [[false, "list"], [false, "form"]],
            domain: [["move_type", "=", "out_invoice"]],
        });
    }
}
PropertyListController.template = `real_estate_account.propertyListView`;
export const propertyListView = {
    ...listView,
    Controller: PropertyListController,
}

registry.category("views").add("real_estate_list_view", propertyListView)