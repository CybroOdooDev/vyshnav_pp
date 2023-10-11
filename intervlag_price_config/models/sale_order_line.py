# -*- coding: utf-8 -*-
from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_config_id = fields.Many2one('price.matrix',
                                      string="Price config",
                                      store=True)

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            if line.product_template_id.has_configurable_attributes:
                customer_tag_ids = line.order_id.partner_id.category_id
                customer_class_id = line.order_id.partner_id.gift_category_id
                size = line.product_no_variant_attribute_value_ids.search(
                    [('attribute_id.is_size_attribute', '=', True),
                     ('id', 'in',
                      line.product_no_variant_attribute_value_ids.ids)]).product_attribute_value_id
                material = line.product_no_variant_attribute_value_ids.search(
                    [('attribute_id.is_material_attribute', '=', True),
                     ('id', 'in',
                      line.product_no_variant_attribute_value_ids.ids)]).product_attribute_value_id
                delivery = line.product_no_variant_attribute_value_ids.search(
                    [('attribute_id.is_delivery_attribute', '=', True),
                     ('id', 'in',
                      line.product_no_variant_attribute_value_ids.ids)]).product_attribute_value_id
                print_type = line.product_no_variant_attribute_value_ids.search(
                    [('attribute_id.is_print_type', '=', True),
                     ('id', 'in',
                      line.product_no_variant_attribute_value_ids.ids)]).product_attribute_value_id
                quantity = line.product_uom_qty
                price_configurator_price = line.env['price.matrix'].search(
                    [(
                        'price_configurator_id.print_type_id', '=',
                        print_type.id),
                        ('price_configurator_id.customer_tag_ids', 'in',
                         customer_tag_ids.ids),
                        ('price_configurator_id.product_size_id', 'in',
                         size.ids),
                        ('price_configurator_id.product_material_id', '=',
                         material.id),
                        ('delivery_attribute_id', '=', delivery.id),
                        ('price_configurator_id.customer_class_id', '=',
                         customer_class_id.id)])
                if price_configurator_price:
                    line.write({'price_config_id': price_configurator_price.id})
                    # ;price_config_id = price_configurator_price.id
                    suitable_order_lines = line._origin.order_id.order_line.search(
                        [('price_config_id', '=', price_configurator_price.id),
                         ('order_id', '=', line._origin.order_id.id)])
                    if len(suitable_order_lines) > 1:
                        combined_quantity = 0
                        for rec in suitable_order_lines:
                            combined_quantity += rec.product_uom_qty
                        merge_price_configurator_price = line.env[
                            'price.matrix'].search(
                            [(
                                'price_configurator_id.print_type_id', '=',
                                print_type.id),
                                ('price_configurator_id.customer_tag_ids',
                                 'in',
                                 customer_tag_ids.ids),
                                ('price_configurator_id.product_size_id',
                                 'in',
                                 size.ids),
                                (
                                    'price_configurator_id.product_material_id',
                                    '=',
                                    material.id),
                                ('delivery_attribute_id', '=', delivery.id),
                                ('price_configurator_id.customer_class_id',
                                 '=',
                                 customer_class_id.id),
                                ('min_qty', '<=', combined_quantity),
                                ('max_qty', '>=', combined_quantity)])
                        if merge_price_configurator_price:
                            for value in suitable_order_lines:
                                value.price_unit = merge_price_configurator_price.sale_price
                        else:
                            super()._compute_price_unit()
                    else:
                        if price_configurator_price.min_qty <= quantity and price_configurator_price.max_qty >= quantity:
                            line.price_unit = price_configurator_price.sale_price
                        else:
                            super()._compute_price_unit()
                else:
                    super()._compute_price_unit()
            else:
                super()._compute_price_unit()

    def create(self, vals_list):
        order_line = super(SaleOrderLine, self).create(vals_list)
        order_line._compute_price_unit()
        return order_line


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_updated = fields.Boolean(String="is updated", default=False)

    def action_update_price_config_price(self):
        self.is_updated = True
        self.order_line._compute_price_unit()

    @api.onchange('order_line')
    def _onchange_order_line(self):
        self.is_updated = False
