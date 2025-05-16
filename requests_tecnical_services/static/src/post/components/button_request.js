/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { CategorySelector } from "@point_of_sale/app/generic_components/category_selector/category_selector";


class ButtonRequestPopup extends Component {
    static template = "requests_tecnical_services.ButtonRequestPopup";
    static defaultProps = {
        title: 'jola',
        requests: { type: Array, optional: true },
        close: { type: Function, optional: true },
    };
}


patch(CategorySelector, {
    components: {
        ...CategorySelector.components,
        ButtonRequestPopup

    },
    
});

patch(CategorySelector.prototype, {

    setup() {
        this.orm = useService("orm");
        this.popup = useService("popup");
        this.pos = useService("pos"); 
    },

    async getRequest() {
        // 1. Obtener el cliente actual del POS
        const users = this.pos.user.id

        const requests = await this.orm.searchRead(
            "technical.service.request",
            [
                ["assigned_user_id", "=", users],
                ["state", "!=", "done"],  
            ],
            ["name", "equipment", "priority", "date_requested"]
        );
       
        console.log(requests)
        this.popup.add(ButtonRequestPopup, {
            title: `Solicitudes de ${this.pos.user.name}`,
            requests: requests,
        });
    }
});
