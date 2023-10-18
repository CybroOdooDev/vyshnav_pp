from odoo import http, fields
from odoo.http import request


class AttributeValueConstrains(http.Controller):
    """controller to add and retrieve data for attribute values"""

    @http.route('/product_config/attribute_value_constrains', type='json',
                auth='user')
    def attribute_value_rules(self, **kwargs):
        selected_varient = kwargs.get('product_template_attribute_id')
        print(selected_varient)
        product_tmpl_id = kwargs.get('product_tmpl_id')
        product = request.env['product.template'].browse(int(product_tmpl_id))
        attribute_values_in_rule = (product.product_attribute_rule_ids.
                                    values_ids.ids)
        if selected_varient:
            product_attribute_value = request.env[('product.template.attribute'
                                                   '.value')].browse(int(
                selected_varient)).product_attribute_value_id
            if product_attribute_value.id in attribute_values_in_rule:
                excluded_product_attribute_values = (product.
                                                     product_attribute_rule_ids.
                                                     restriction_config_id.
                                                     restriction_rule_ids.
                                                     values_ids)
                excluded_product_tmpl_attribute_values = request.env[
                    'product.template.attribute.value'].search([(
                    'product_attribute_value_id',
                    'in',
                    excluded_product_attribute_values.ids)])
                return {'excluded_values':
                            excluded_product_tmpl_attribute_values.ids}
