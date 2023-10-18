# -*- coding: utf-8 -*-
from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            if line.product_template_id.has_configurable_attributes:
                customer_tag_ids = line.order_id.partner_id.category_id
                customer_class_id = line.order_id.partner_id.gift_category_id
                size = line.product_no_variant_attribute_value_ids.filtered(
                    lambda
                        pc: pc.attribute_id.attribute_type == 'size_attribute' and pc.id in
                            line.product_no_variant_attribute_value_ids.ids
                ).product_attribute_value_id
                material = line.product_no_variant_attribute_value_ids.filtered(
                    lambda
                        pc: pc.attribute_id.attribute_type == 'material_attribute' and pc.id
                            in line.product_no_variant_attribute_value_ids.ids
                ).product_attribute_value_id

                delivery = line.product_no_variant_attribute_value_ids.filtered(
                    lambda
                        pc: pc.attribute_id.attribute_type == 'delivery_attribute' and pc.id in
                            line.product_no_variant_attribute_value_ids.ids
                ).product_attribute_value_id

                print_type = (
                    line.product_no_variant_attribute_value_ids.filtered(
                        lambda pc: pc.attribute_id.attribute_type == 'print_attribute'
                                   and pc.id in
                                   line.product_no_variant_attribute_value_ids.ids
                    ).product_attribute_value_id)
                domain = [(
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
                     customer_class_id.id)]
                quantity = 0
                order_lines = line.order_id.order_line
                similar_order_lines = order_lines.filtered(
                    lambda
                        x: x.product_no_variant_attribute_value_ids.ids == line.
                    product_no_variant_attribute_value_ids.ids)
                for qty in similar_order_lines:
                    quantity += qty.product_uom_qty
                domain.append(('min_qty', '<=', quantity))
                domain.append(('max_qty', '>=', quantity))
                price_configurator_price = line.env['price.matrix'].search(
                    domain)
                if price_configurator_price:
                    line.price_unit = price_configurator_price.sale_price
                else:
                    if line.qty_invoiced > 0:
                        continue
                    if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                        line.price_unit = 0.0
                    else:
                        price = line.with_company(
                            line.company_id)._get_display_price()
                        line.price_unit = line.product_id._get_tax_included_unit_price(
                            line.company_id,
                            line.order_id.currency_id,
                            line.order_id.date_order,
                            'sale',
                            fiscal_position=line.order_id.fiscal_position_id,
                            product_price_unit=price,
                            product_currency=line.currency_id
                        )
            else:
                if line.qty_invoiced > 0:
                    continue
                if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                    line.price_unit = 0.0
                else:
                    price = line.with_company(
                        line.company_id)._get_display_price()
                    line.price_unit = line.product_id._get_tax_included_unit_price(
                        line.company_id,
                        line.order_id.currency_id,
                        line.order_id.date_order,
                        'sale',
                        fiscal_position=line.order_id.fiscal_position_id,
                        product_price_unit=price,
                        product_currency=line.currency_id
                    )

    @api.model_create_multi
    def create(self, vals_list):
        order_line = super(SaleOrderLine, self).create(vals_list)
        order_line._compute_price_unit()
        return order_line


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_updated = fields.Boolean(string="is updated", default=False)

    def action_update_price_config_price(self):
        self.is_updated = True
        self.order_line._compute_price_unit()

    @api.onchange('order_line', 'partner_id')
    def _onchange_order_line(self):
        self.is_updated = False