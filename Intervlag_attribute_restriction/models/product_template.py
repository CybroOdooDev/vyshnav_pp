# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """Inherited class to add restriction rules for attribute values in
    product"""
    _inherit = 'product.template'

    product_attribute_rule_ids = fields.One2many('product.attribute.rule',
                                                 'product_template_id'
                                                 , string="Restriction")



