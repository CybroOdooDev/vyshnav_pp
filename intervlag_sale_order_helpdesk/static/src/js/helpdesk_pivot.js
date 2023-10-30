/** @odoo-module **/
import { PivotModel } from "@web/views/pivot/pivot_model";
import { patch } from "@web/core/utils/patch";

patch(PivotModel.prototype, "HelpdeskPivot.percentage", {
//Patched component to customize pivot view
    setup() {
        this._super.apply(this, arguments);
    },
       _getCellValue(groupId, measure, originIndexes, config) {
       //Function to calculate percentage based on pivot view measurements
        var key = JSON.stringify(groupId);
        if (!config.data.measurements[key]) {
            return;
        }
        var values
        if (measure=="valid_ticket_percentage"){
          values=originIndexes.map((originIndex) => {
          var total_tickets=config.data.measurements[key][originIndex]['__count'];
          var percentage=config.data.measurements[key][originIndex]['valid_ticket_percentage'];
          var val= (percentage / total_tickets)
          return val;
           });
        }
         else if (measure=="average_cost"){
          values = originIndexes.map((originIndex) => {
          var total_tickets=config.data.measurements[key][originIndex]['__count'];
          var cost_of_restore=config.data.measurements[key][originIndex]['cost_of_restore'];
          var avg = (cost_of_restore / total_tickets)
          return avg;
           });
        }
        else{
        values = originIndexes.map((originIndex) => {
            return config.data.measurements[key][originIndex][measure];
        });
        }
         if (originIndexes.length > 1) {
            return computeVariation(values[1], values[0]);
        } else {
            return values[0];
        }
     }

});
