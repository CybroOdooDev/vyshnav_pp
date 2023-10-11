# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PriceConfigurator(models.Model):
    _name = "price.configurator"
    _description = 'Price Configurator'

    name = fields.Char(string='Name', compute="_compute_name", store=True,
                       default="NEW")
    print_type_id = fields.Many2one('product.attribute.value',
                                    string="Printing",
                                    domain='[("attribute_id'
                                           '.is_print_type", "=", True)]',
                                    )
    print = fields.Selection(related="print_type_id.print_type",string="Print")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.company.currency_id)
    product_material_id = fields.Many2one('product.attribute.value',
                                          "Material",
                                          domain='[("attribute_id'
                                                 '.is_material_attribute", '
                                                 '"=", True)]')
    product_size_id = fields.Many2one('product.attribute.value',
                                      "Size",
                                      domain='[("attribute_id'
                                             '.is_size_attribute", "=", True)]')
    customer_tag_ids = fields.Many2many('res.partner.category',
                                        string="Customer Tag")
    customer_class_id = fields.Many2one('loyalty.program',
                                        string="Program type",
                                        domain="[('program_type','=','gift_meter')]")
    price_matrix_ids = fields.One2many('price.matrix',
                                       'price_configurator_id',
                                       string="Price Matrix")

    @api.depends('print_type_id', 'product_material_id', 'product_size_id')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.print_type_id.name + ':' + str(
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
                                            domain='[("attribute_id'
                                                   '.is_delivery_attribute", "=", True)]')
    price_configurator_id = fields.Many2one("price.configurator",
                                            "Price Configurator")
