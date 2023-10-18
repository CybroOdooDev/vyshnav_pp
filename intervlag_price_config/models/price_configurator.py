# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PriceConfigurator(models.Model):
    _name = "price.configurator"
    _description = 'Price Configurator'

    name = fields.Char(string='Name', compute="_compute_name", store=True,
                       default="NEW")
    print_type_id = fields.Many2one('product.attribute.value',
                                    string="Printing",
                                    domain='[("attribute_type", "=", "print_attribute"),("attribute_id.create_variant","=","no_variant")]', required=True
                                    )
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.company.currency_id)
    product_material_id = fields.Many2one('product.attribute.value',
                                          "Material",
                                          domain='[("attribute_type","=", "material_attribute"),("attribute_id.create_variant","=","no_variant")]',
                                          required=True)
    product_size_id = fields.Many2one('product.attribute.value',
                                      "Size",
                                      domain='[("attribute_type", "=","size_attribute"),("attribute_id.create_variant","=","no_variant")]',
                                      required=True)
    customer_tag_ids = fields.Many2many('res.partner.category',
                                        string="Customer Tag", required=True)
    customer_class_id = fields.Many2one('loyalty.program',
                                        string="Program type",
                                        domain="[('program_type','=',"
                                               "'gift_meter')]", required=True)
    price_matrix_ids = fields.One2many('price.matrix',
                                       'price_configurator_id',
                                       string="Price Matrix", copy=True)

    @api.depends('print_type_id', 'product_material_id', 'product_size_id')
    def _compute_name(self):
        for rec in self:
            rec.name = str(rec.print_type_id.name) + ':' + str(
                rec.product_material_id.name) + '-' + str(
                rec.product_size_id.name)


class PriceMatrix(models.Model):
    _name = "price.matrix"
    _description = "Price Matrix"

    min_qty = fields.Float(string="Minimum Quantity", required=True)
    max_qty = fields.Float(string="Maximum Quantity", required=True)
    cost_price = fields.Float(string="Cost Price")
    sale_price = fields.Float(string="Sale Price")
    delivery_attribute_id = fields.Many2one("product.attribute.value",
                                            'Delivery',
                                            domain='[("attribute_type", "=","delivery_attribute"),'
                                                   '("attribute_id.create_variant","=","no_variant")]',
                                            required=True)
    price_configurator_id = fields.Many2one("price.configurator",
                                            "Price Configurator")

    @api.constrains('min_qty', 'max_qty')
    def _check_values(self):
        for rec in self:
            if rec.min_qty == 0.0 or rec.max_qty == 0.0:
                raise ValidationError(_('Values should not be zero.'))

    @api.onchange('max_qty')
    def _onchange_max_qty(self):
        if self.min_qty:
            if self.min_qty >= self.max_qty:
                raise ValidationError(_('Minimum quantity must be less than '
                                        'Maximum quantity.'))
