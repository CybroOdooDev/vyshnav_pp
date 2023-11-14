# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RestrictionRule(models.Model):
    """Class for setting restriction rules for attribute values"""
    _name = "restriction.rule"
    _description = 'Restriction Rules'

    attribute_id = fields.Many2one('product.attribute',
                                   string="Attribute", required=True)
    values_ids = fields.Many2many('product.attribute.value',
                                  string='Values',
                                  relation='product_attribute_value_restriction_rule_rel',
                                  domain="[('attribute_id', '=', attribute_id)]",
                                  required=True)
    restriction_configurator_id = fields.Many2one('restriction.configurator',
                                                  string="Restriction "
                                                         "Configurator")

    @api.onchange('attribute_id')
    def attribute_id_onchange(self):
        return {'domain': {'attribute_id': [('id', 'not in',
                                             self.restriction_configurator_id.restriction_rule_ids.
                                             attribute_id.
                                             ids)]}}