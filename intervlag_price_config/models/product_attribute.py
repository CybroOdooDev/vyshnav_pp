# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    # is_material_attribute = fields.Boolean("Is Material Attribute",
    #                                        dafault=False)
    # is_print_type = fields.Boolean("Is Print Type Attribute",
    #                                dafault=False)

