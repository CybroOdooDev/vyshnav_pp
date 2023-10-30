/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SaleOrderLineProductField } from '@sale/js/sale_product_field';
import { OptionalProductsModal } from "@sale_product_configurator/js/product_configurator_modal";
import {
    selectOrCreateProduct,
    getSelectedVariantValues,
    getNoVariantAttributeValues,
} from "sale.VariantMixin";


patch(SaleOrderLineProductField.prototype, 'intervlag_product_config', {

    setup() {
        this._super(...arguments);
        this.rpc = useService("rpc");
        this.ui = useService("ui");
        this.orm = useService("orm");
    },

    async _convertConfiguratorDataToUpdateData(mainProduct) {

        const nameGet = await this.orm.nameGet(
            'product.product',
            [mainProduct.product_id],
            { context: this.context }
        );
        let result = {
            product_id: nameGet[0],
            product_uom_qty: mainProduct.quantity,
            design_code_custom_flag: mainProduct.design_code_custom_save,
        };
        var customAttributeValues = mainProduct.product_custom_attribute_values;
        var customValuesCommands = [{ operation: "DELETE_ALL" }];
        if (customAttributeValues && customAttributeValues.length !== 0) {
            _.each(customAttributeValues, function (customValue) {
                customValuesCommands.push({
                    operation: "CREATE",
                    context: [
                        {
                            default_custom_product_template_attribute_value_id:
                                customValue.custom_product_template_attribute_value_id,
                            default_custom_value: customValue.custom_value,
                        },
                    ],
                });
            });
        }

        result.product_custom_attribute_value_ids = {
            operation: "MULTI",
            commands: customValuesCommands,
        };

        var noVariantAttributeValues = mainProduct.no_variant_attribute_values;
        var noVariantCommands = [{ operation: "DELETE_ALL" }];
        if (noVariantAttributeValues && noVariantAttributeValues.length !== 0) {
            var resIds = _.map(noVariantAttributeValues, function (noVariantValue) {
                return { id: parseInt(noVariantValue.value) };
            });

            noVariantCommands.push({
                operation: "ADD_M2M",
                ids: resIds,
            });
        }

        result.product_no_variant_attribute_value_ids = {
            operation: "MULTI",
            commands: noVariantCommands,
        };
        return result;
    },

    /**
     * Will map the optional producs data to sale.order.line
     * creation contexts.
     *
     * @param {Array} optionalProductsData The optional products data given by the configurator
     *
     * @private
     */
    _convertConfiguratorDataToLinesCreationContext: function (optionalProductsData) {
        return optionalProductsData.map(productData => {
            return {
                default_product_id: productData.product_id,
                default_product_template_id: productData.product_template_id,
                default_product_uom_qty: productData.quantity,
                default_design_code_custom_flag:productData.design_code_custom_save,
                default_product_no_variant_attribute_value_ids: productData.no_variant_attribute_values.map(
                    noVariantAttributeData => {
                        return [4, parseInt(noVariantAttributeData.value)];
                    }
                ),
                default_product_custom_attribute_value_ids: productData.product_custom_attribute_values.map(
                    customAttributeData => {
                        return [
                            0,
                            0,
                            {
                                custom_product_template_attribute_value_id:
                                    customAttributeData.custom_product_template_attribute_value_id,
                                custom_value: customAttributeData.custom_value,
                            },
                        ];
                    }
                )
            };
        });
    },
});
