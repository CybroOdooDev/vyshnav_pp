/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { OptionalProductsModal } from "@sale_product_configurator/js/product_configurator_modal";

patch(OptionalProductsModal.prototype, 'MultipleDesign', {
        getAndCreateSelectedProducts: async function () {
        var self = this;
        const products = [];
        let productCustomVariantValues;
        let noVariantAttributeValues;
        let designCount;
        for (const product of self.$modal.find('.js_product.in_cart')) {
            var $item = $(product);
            var parentUniqueId = product.dataset.parentUniqueId;
            var uniqueId = product.dataset.uniqueId;
            productCustomVariantValues = $item.find('.custom-attribute-info').data("attribute-value") || self.getCustomVariantValues($item);
            noVariantAttributeValues = $item.find('.no-attribute-info').data("attribute-value") || self.getNoVariantAttributeValues($item);
            designCount = self.$modal.find('.custom-no-of-design').val() || 1;

            const productID = await self.selectOrCreateProduct(
                $item,
                parseInt($item.find('input.product_id').val(), 10),
                parseInt($item.find('input.product_template_id').val(), 10),
                true
            );
            let qty = (designCount > 1) ? 0 : 1;
            for (designCount; designCount>0; designCount--) {
                products.push({
                    'product_id': productID,
                    'product_template_id': parseInt($item.find('input.product_template_id').val(), 10),
                    'quantity': qty,
                    'parent_unique_id': parentUniqueId,
                    'unique_id': uniqueId,
                    'product_custom_attribute_values': productCustomVariantValues,
                    'no_variant_attribute_values': noVariantAttributeValues,
                });
                }
        }
        return products;
    },
});
