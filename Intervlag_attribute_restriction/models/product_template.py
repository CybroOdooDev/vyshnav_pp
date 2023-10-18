from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_attribute_rule_ids = fields.One2many('product.attribute.rule',
                                                 'product_template_id'
                                                 , string="Restriction")

    def rule_for_product(self):
        attribute_values = self.product_attribute_rule_ids.values_ids
        excluded_values = self.product_attribute_rule_ids.restriction_config_id.restriction_rule_ids.values_ids
        return {
            'attribute_values':attribute_values,
            'excluded_values':excluded_values
                }

