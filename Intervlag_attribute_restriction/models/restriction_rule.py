from odoo import models, fields


class RestrictionRule(models.Model):
    _name = "restriction.rule"
    _description = 'Restriction Rules'

    attribute_id = fields.Many2one('product.attribute',
                                   string="Attribute",required= True)
    condition = fields.Selection([('in', 'Include'),
                                  ('not in',
                                   'Exclude')],
                                 string="Condition",required= True)
    values_ids = fields.Many2many('product.attribute.value',
                                  string='Values',
                                  relation='product_attribute_value_restriction_rule_rel',
                                  domain="[('attribute_id', '=', attribute_id)]",required= True)
    restriction_configurator_id = fields.Many2one('restriction.configurator',
                                                  string="Restriction "
                                                         "Configurator")
