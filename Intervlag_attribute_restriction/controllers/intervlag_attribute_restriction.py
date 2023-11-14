# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request


class AttributeValueConstrains(http.Controller):
    """controller to add and retrieve data for attribute values"""

    @http.route('/product_config/attribute_value_constraints', type='json',
                auth='user')
    def attribute_value_rules(self, **kwargs):
        """function to get attribute values that needs to exclude in product
        configurator"""
        selected_varient = kwargs.get('product_template_attribute_id')
        product_tmpl_id = kwargs.get('product_tmpl_id')
        product = request.env['product.template'].browse(int(product_tmpl_id))
        if selected_varient:
            product_attribute_value_ids = []
            for varient_value in selected_varient:
                product_attribute_value = request.env[
                    'product.template.attribute.value'].browse(
                    int(varient_value))
                if product_attribute_value:
                    product_attribute_value_ids.append(
                        product_attribute_value.product_attribute_value_id)
            excluded_values_li = []
            for rec in product_attribute_value_ids:
                print('satisfied', rec.name)
                product_rule = product.product_attribute_rule_ids.search(
                    [('values_ids', 'in', rec.id),
                     ('product_template_id', '=', product.id)])
                for rule in product_rule:
                    excluded_values_li.extend(
                        rule.restriction_config_id.restriction_rule_ids.values_ids.ids)
                print(excluded_values_li)
            excluded_product_tmpl_attribute_values = request.env[
                'product.template.attribute.value'].search([(
                'product_attribute_value_id',
                'in',
                excluded_values_li)])
            return {'excluded_values': excluded_product_tmpl_attribute_values.ids}
            # if rec.id in attribute_values_in_rule:
            #     excluded_product_attribute_values = (product.
            #                                          product_attribute_rule_ids.
            #                                          restriction_config_id.
            #                                          restriction_rule_ids.
            #                                          values_ids)
            #     excluded_product_tmpl_attribute_values = request.env[
            #         'product.template.attribute.value'].search([(
            #         'product_attribute_value_id',
            #         'in',
            #         excluded_product_attribute_values.ids)])
            #     print(excluded_product_attribute_values.ids, 'this')

            #                 excluded_product_tmpl_attribute_values.ids}
            #     return {'excluded_values':
            #                 excluded_product_tmpl_attribute_values.ids}

            # if product_attribute_value_ids in attribute_values_in_rule:
