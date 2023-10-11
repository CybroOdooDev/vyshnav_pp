/** @odoo-module **/
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { priceConfigSaleOrderRender } from './price_config_form_renderer.js';

export const SaleOrderPriceConfig = {
    ...formView,
    Renderer: priceConfigSaleOrderRender,
};
registry.category("views").add("sale_order_price_config", SaleOrderPriceConfig);
