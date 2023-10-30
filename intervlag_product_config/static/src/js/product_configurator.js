odoo.define('intervlag_product_config.product_configurator', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    const {OptionalProductsModal} = require('@sale_product_configurator/js/product_configurator_modal');
    OptionalProductsModal.include({
        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            this.$el.find('select').select2({
                closeOnSelect: false
            })
            this.$el.find('ul').css("border", "none");
            this.$el.find('input[name="add_qty"]').val(this.rootProduct.quantity);
            // set a unique id to each row for options hierarchy
            var $products = this.$el.find('tr.js_product');
            _.each($products, function (el) {
                var $el = $(el);
                var uniqueId = self._getUniqueId(el);

                var productId = parseInt($el.find('input.product_id').val(), 10);
                if (productId === self.rootProduct.product_id) {
                    self.rootProduct.unique_id = uniqueId;
                } else {
                    el.dataset.parentUniqueId = self.rootProduct.unique_id;
                }
            });

            return def.then(function () {
                // This has to be triggered to compute the "out of stock" feature
                self._opened.then(function () {
                    self.triggerVariantChange(self.$el);
                });
            });
        },

        init: function (parent, params) {
            var self = this;

            var options = _.extend({
                size: 'large',
                buttons: [{
                    text: params.okButtonText,
                    click: this._onConfirmButtonClick,
                    // the o_sale_product_configurator_edit class is used for tours.
                    classes: 'btn-info o_sale_product_configurator_edit'
                }, {
                    text: params.cancelButtonText,
                    click: this._onCancelButtonClick
                },
                ],
                technical: !params.isWebsite,
            }, params || {});
            this._super(parent, options);

            this.context = params.context;
            this.rootProduct = params.rootProduct;
            this.container = parent;
            this.pricelistId = params.pricelistId;
            this.previousModalHeight = params.previousModalHeight;
            this.mode = params.mode;
            this.dialogClass = 'oe_advanced_configurator_modal';
            this._productImageField = 'image_128';

            this._opened.then(function () {
                if (self.previousModalHeight) {
                    self.$el.closest('.modal-content').css('min-height', self.previousModalHeight + 'px');
                }
            });

        },


        getAndCreateSelectedProducts: async function () {
            var self = this;
            let products = [];
            let designCount;
            let variant;
            let quant;
            let length;
            let width;
            for (const product of self.$modal.find('.js_product.in_cart')) {
                var $item = $(product);
                var quantity = parseFloat($item.find('input[name="add_qty"]').val().replace(',', '.') || 1);
                var parentUniqueId = product.dataset.parentUniqueId;
                var uniqueId = product.dataset.uniqueId;
                const productID = parseInt($item.find('input.product_id').val(), 10);
                const productTemplateID = parseInt($item.find('input.product_template_id').val(), 10);
                var productCustomVariantValues = $item.find('.custom-attribute-info').data("attribute-value") || self.getCustomVariantValues($item);
                var noVariantAttributeValues = $item.find('.no-attribute-info').data("attribute-value") || self.getNoVariantAttributeValues($item);
                var attributeCountMap = {}; // To count attribute repetitions
                length = self.$modal.find('.variant_custom_value_length').val() || false;
                width = self.$modal.find('.variant_custom_value_width').val() || false;
                if(length && width){
                    self.$modal.find('.variant_custom_value').val(`Custom Size : ${length} x ${width}`);
                }
                productCustomVariantValues = $item.find('.custom-attribute-info').data("attribute-value") || self.getCustomVariantValues($item);
                noVariantAttributeValues = $item.find('.no-attribute-info').data("attribute-value") || self.getNoVariantAttributeValues($item);
                designCount = self.$modal.find('.custom-no-of-design').val() || 1;
                quant = self.$modal.find('.js_quantity').val() || 1;
                // Iterate through noVariantAttributeValues to count repetitions
                for (const attributeValue of noVariantAttributeValues) {
                    var attributeKey = attributeValue.attribute_name;

                    // Check if the attribute name is already in the map
                    if (attributeCountMap[attributeKey]) {
                        attributeCountMap[attributeKey]++;
                    } else {
                        attributeCountMap[attributeKey] = 1;
                    }
                }

                // Now, attributeCountMap contains the count of each attribute name

                // Iterate through noVariantAttributeValues again to create products
                var fullAttribute = []

                var combineVariants = false;

                for (const attributeValue of noVariantAttributeValues) {
                    var attributeKey = attributeValue.attribute_name;

                    // Check if the attribute occurs only once (not repeating)
                    if (attributeCountMap[attributeKey] === 1) {
                        fullAttribute.push(attributeValue)
                        combineVariants = true;

                    }
                }

                   if (combineVariants) {
                    let qty = (designCount > 1) ? 0 : 1;
                    function getRandomInt(max) {
                        return Math.floor(Math.random() * max);
                    }
                    var design_code_custom_save ={}
                    if ($('.variant_custom_value_checkbox').val() === "True"){
                    design_code_custom_save = {'Design_code':getRandomInt(10000),
                                   'is_to_save': $('.variant_custom_value_checkbox').val()}
                    }
                    else{
                      design_code_custom_save = {'Design_code':getRandomInt(10000)}
                    }
            for (designCount; designCount>0; designCount--) {
                var newProduct = {
                        'design_code_custom_save':design_code_custom_save,
                        'product_id': productID,
                        'product_template_id': productTemplateID,
                        'quantity': quantity,
                        'parent_unique_id': parentUniqueId,
                        'unique_id': uniqueId,
                        'product_custom_attribute_values': productCustomVariantValues,
                        'no_variant_attribute_values': fullAttribute, // Use the current attribute value in the array
                    };
                    products.push(newProduct);
            }

                }

            }

            for (const attributeValue of noVariantAttributeValues) {
                var attributeKey = attributeValue.attribute_name;
                if (attributeCountMap[attributeKey] > 1) {
                var newProd = {
                        'product_id': parseInt(attributeValue.custom_product_template_attribute_value_id),
                        'product_template_id': parseInt(attributeValue.is_custom),
                        'quantity': quantity,
                        'parent_unique_id': parentUniqueId,
                        'unique_id': uniqueId,
                        'product_custom_attribute_values': [],
                        'no_variant_attribute_values': [], // Use the current attribute value in the array
                    };
                    products.push(newProd);
            }

            }
            return products;
        },

    });
});