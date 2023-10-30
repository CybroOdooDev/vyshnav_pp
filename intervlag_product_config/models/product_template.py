# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_configurable_product = fields.Boolean("Is Configurable Product",
                                             default=False,help="This is used to make the product configurable with custom size.")


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    @api.onchange("attribute_id")
    def onchange_attribute_id(self):
        if self.attribute_id:
            if self.product_tmpl_id.is_configurable_product:
                if self.attribute_id.create_variant != 'no_variant':
                    raise ValidationError(
                        _("Sorry you cannot add '%s' attribute to this product. You "
                          "can only add attribute with 'Variants Creation Mode' "
                          "with 'Never (option)' to a configurable product") % (self.attribute_id.name))