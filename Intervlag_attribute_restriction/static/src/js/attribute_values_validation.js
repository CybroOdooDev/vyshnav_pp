odoo.define(
  "Intervlag_attribute_restriction.product_config",
  function (require) {
    "use strict";
    var ajax = require("web.ajax");

    const {
      OptionalProductsModal,
    } = require("@sale_product_configurator/js/product_configurator_modal");
    OptionalProductsModal.include({
      onChangeVariant: function (ev) {
        var $parent = $(ev.target).closest(".js_product");
        if (!$parent.data("uniqueId")) {
          $parent.data("uniqueId", _.uniqueId());
        }
        this._throttledGetCombinationInfo($parent.data("uniqueId"))(ev);

        var self = this;
        this.$el.find(".attribute_hidden").removeClass("attribute_hidden");
        var product_template_attribute_id = ev.target.dataset.value_id;
        var product_tmpl_id = self.rootProduct["product_template_id"];
        ajax
          .rpc("/product_config/attribute_value_constrains", {
            product_template_attribute_id: product_template_attribute_id,
            product_tmpl_id: product_tmpl_id,
          })
          .then(function (data) {
            if (data) {
              for (var i = 0; i < data["excluded_values"].length; i++) {
                var value_id = data["excluded_values"][i];
                var values_data = self.$el.find(
                  "[data-value_id = " + value_id + "]"
                )[0];
                if (values_data) {
                  $(values_data.parentElement).addClass("attribute_hidden");
                }
              }
            }
          });
      },
    });
  }
);
