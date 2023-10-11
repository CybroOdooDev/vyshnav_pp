/** @odoo-module **/
import { FormRenderer } from "@web/views/form/form_renderer";
export class priceConfigSaleOrderRender extends FormRenderer {
   setup() {
       super.setup();
   }
   _UpdatePrices(ev){
//    console.warn(this)
     ev.target.style.color = "red";
    }
}