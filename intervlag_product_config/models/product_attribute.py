# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    highlight_on_report = fields.Boolean("Highlight on report", default=False,
                                         help="Highlight this attribute on MO")
    is_required = fields.Boolean("Is Required", default=False)

    @api.onchange('value_ids')
    def onchange_value_ids(self):
        this = self.value_ids
        for item in this:
            if item.is_custom and item.is_custom_size:
                raise ValidationError("Both 'Is custom' and 'Is custom size' "
                                      "cannot be used simultaneously.")


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    is_custom_size = fields.Boolean('Is custom size',
                                    help="Allow users to input custom size "
                                         "for size attribute value")
    product_id = fields.Many2one("product.product",
                                 string="Related Product")

    partner_ids = fields.Many2many('res.partner',
                                   string="Related Partner")


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    is_custom_size = fields.Boolean('Is custom value',
                                    related="product_attribute_value_id.is_custom_size")

    partner_ids = fields.Many2many('res.partner',
                                   related="product_attribute_value_id.partner_ids",
                                   string="Related Partner")


class ProductAttributeCustomValue(models.Model):
    _inherit = "product.attribute.custom.value"

    length_custom = fields.Float(string="Length")
    width_custom = fields.Float(string="Width")
    partner_id = fields.Many2one('res.partner',
                                 string="Related Partner")
