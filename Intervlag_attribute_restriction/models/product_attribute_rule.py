# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductAttributeRule(models.Model):
    """Class to add restriction rules in product"""
    _name = "product.attribute.rule"
    _description = 'Product Attribute Rule'

    product_template_id = fields.Many2one('product.template', string="Product")
    attribute_id = fields.Many2one('product.attribute',
                                   string="Attribute",
                                   required=True)
    values_ids = fields.Many2many('product.attribute.value',
                                  string='Values',
                                  relation='product_attribute_value_product_attribute_rule_rel',
                                  domain="[('attribute_id', '=', attribute_id)]",
                                  required=True)
    restriction_config_id = fields.Many2one('restriction.configurator',
                                            string='Rule')

    @api.onchange('attribute_id')
    def attribute_id_onchange(self):
        return {'domain': {'attribute_id': [('id', 'in',
                                             self.
                                             product_template_id.
                                             attribute_line_ids.
                                             attribute_id.
                                             ids)]}}
