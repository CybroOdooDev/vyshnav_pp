odoo.define('intervlag_product_config.configure', function (require) {
    "use strict";

    var core = require('web.core');
    var VariantMixin = require('sale.VariantMixin');


    VariantMixin.getCustomVariantValues = ($target) =>{

        var variantCustomValues = [];

        $target.find('.variant_custom_value').each(function (){
            var $variantCustomValueInput = $(this);
            var $closestLength = $variantCustomValueInput.siblings('.variant_custom_value_length');
            var $closestWidth = $closestLength.siblings('.variant_custom_value_width');
            var length = $closestLength.val();
            var width = $closestWidth.val();
            if(length && width){
            $variantCustomValueInput.val(`Custom Size : ${length}x${width}`);}
            if ($variantCustomValueInput.length !== 0){
                variantCustomValues.push({
                    'custom_product_template_attribute_value_id': $variantCustomValueInput.data('custom_product_template_attribute_value_id'),
                    'attribute_value_name': $variantCustomValueInput.data('attribute_value_name'),
                    'custom_value': $variantCustomValueInput.val(),
                });
            }
        });

        return variantCustomValues;

    }

    VariantMixin.handleCustomValues = ($target) => {

        var $variantContainer;
        var $customInput = false;

        var rpc = require('web.rpc');
        if ($target.is('input[type=radio]') && $target.is(':checked')) {
            $variantContainer = $target.closest('ul').closest('li');
            $customInput = $target;
        } else if ($target.is('select')) {
            $variantContainer = $target.closest('li');

            $customInput = $target
                .find('option[value="' + $target.val() + '"]');
        }

        if ($variantContainer) {

            var isCustom = $customInput && $customInput.data('is_custom') === 'True';
            var attributeValueName = $customInput.data('value_name');
            var attributeValueId = $customInput.data('value_id');
            rpc.query({
                        route: '/get_is_customsize',
                        params: {'id': attributeValueId,'name':attributeValueName },
                        }).then(function (result)
          {
             if (isCustom || result) {
                if (isCustom){
                            $variantContainer.find('.variant_custom_value').remove();
                            var $input = $('<input>', {
                                type: 'text',
                                'data-custom_product_template_attribute_value_id': attributeValueId,
                                'data-attribute_value_name': attributeValueName,
                                class: 'variant_custom_value form-control mt-2',
                                style: 'max-width: 83%'
                            });
                            $input.attr('placeholder', attributeValueName +" : Custom");
                            $input.addClass('custom_value_radio');
                            $variantContainer.append($input);

                            }
                           else{$variantContainer.find('.variant_custom_value').remove();
                           }
                if (result){
                            $variantContainer.find('.variant_custom_value_length').remove();
                            $variantContainer.find('.variant_custom_value_width').remove();
                            $variantContainer.find('.variant_custom_value').remove();
                            var $input = $('<input>', {
                                type: 'text',
                                'data-custom_product_template_attribute_value_id': attributeValueId,
                                'data-attribute_value_name': attributeValueName,
                                class: 'variant_custom_value form-control mt-2',
                                style: 'display: none;'
                            });
                            $input.attr('placeholder', attributeValueName +" : Custom");
                            $input.addClass('custom_value_radio');
                            $variantContainer.append($input);

                            var $input_length = $('<input>', {
                                    type: 'number',
                                    'data-custom_product_template_attribute_value_id': attributeValueId,
                                    'data-attribute_value_name': attributeValueName,
                                    class: 'variant_custom_value_length form-control mt-4',
                                    style: 'max-width: 83% ; border-radius:4px;'
                                });
                                $input_length.attr('placeholder', attributeValueName +" : Length");
                                $variantContainer.append($input_length);
                                var $input_width = $('<input>', {
                                    type: 'number',
                                    'data-custom_product_template_attribute_value_id': attributeValueId,
                                    'data-attribute_value_name': attributeValueName,
                                    class: 'variant_custom_value_width form-control mt-4',
                                    style: 'max-width: 83% ; border-radius:4px;'
                                });
                                $input_width.attr('placeholder', attributeValueName +" : Width");
                                $variantContainer.append($input_width);
                                $(".variant_custom_value").val($('.variant_custom_value_length').val());
                                    var $label = $('<label>', {
                                    for: 'saveCheckbox',
                                    text: 'Save this?',
                                    class: 'label_for_checkbox mt-2',
                                });
                             var $checkbox = $('<input>', {
                                type: 'checkbox',
                                id: 'saveCheckbox',
                                class: 'variant_custom_value_checkbox mt-2',
                                style: 'display: inline-block; margin-right: 10px;'
                            });
                            $variantContainer.append($checkbox);
                            $variantContainer.append($label);
                            $('.variant_custom_value_checkbox').val("False")
                            $checkbox.on('change', function() {
                                if (this.checked) {
                                      $('.variant_custom_value_checkbox').val("True")
                                }
                                else{
                                    $('.variant_custom_value_checkbox').val("False")
                                }
                            });
                            }
                            else{
                            $variantContainer.find('.variant_custom_value_width').remove();
                            $variantContainer.find('.variant_custom_value_length').remove();
                            $variantContainer.find('.variant_custom_value_checkbox').remove();
                            $variantContainer.find('.label_for_checkbox').remove();
                            }
                    var previousCustomValue = $customInput.attr("previous_custom_value");
                    if (previousCustomValue) {
                        $variantContainer.find('.variant_custom_value').val(previousCustomValue);
                    }
            }
            else {
                $variantContainer.find('.variant_custom_value').remove();
                $variantContainer.find('.variant_custom_value_width').remove();
                $variantContainer.find('.variant_custom_value_length').remove();
                $variantContainer.find('.variant_custom_value_checkbox').remove();
                $variantContainer.find('.label_for_checkbox').remove();
            }
        }

        );
        }

    }

});