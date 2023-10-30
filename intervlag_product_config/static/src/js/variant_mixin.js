odoo.define("intervlag_product_config.custom_variant_mixin.js", function (require) {
    "use strict";
    const VariantMixin = require('sale.VariantMixin');
    Object.assign(VariantMixin, {

        getNoVariantAttributeValues: function ($container) {

        var noVariantAttributeValues = [];
        var variantsValuesSelectors = [
            'input.no_variant.js_variant_change:checked',
            'select.no_variant.js_variant_change'
        ];

        $container.find(variantsValuesSelectors.join(',')).each(function () {
            var $variantValueInput = $(this);
            var singleNoCustom = $variantValueInput.data('is_single') && !$variantValueInput.data('is_custom');
            var values = $variantValueInput.val();
            if (!$.isArray(values)) {
                values = [values]; // Convert to array to handle single values
            }

            for (var i = 0; i < values.length; i++) {
                var value = values[i];
                var $option = $variantValueInput.is('select') ? $variantValueInput.find('option[value="' + value + '"]') : $variantValueInput;

                var attribute_value_name = $option.data('value_name');
                var attribute_name = $option.data('attribute_name');
                var is_custom = $option.data('is_custom');

                // Handle potential undefined values
                attribute_value_name = attribute_value_name !== undefined ? attribute_value_name : null;
                attribute_name = attribute_name !== undefined ? attribute_name : null;
                is_custom = is_custom !== undefined ? is_custom : null;

                if ($option.length !== 0 && !singleNoCustom) {
                    noVariantAttributeValues.push({
                        'custom_product_template_attribute_value_id': $option.data('value_id'), // Retrieve inside the loop
                        'attribute_value_name': attribute_value_name,
                        'value': value,
                        'attribute_name': attribute_name,
                        'is_custom': is_custom
                    });
                }
            }

        });
        return noVariantAttributeValues;
    },

    })

});