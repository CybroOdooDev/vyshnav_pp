# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    """Inherited sale.order.line class to update functions related to
    pricleist"""
    _inherit = "sale.order.line"

    pricelist_item_id = fields.Many2one(
        comodel_name='product.pricelist.item',
        compute='_compute_pricelist_item_id', store=True)

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        """Overriden function to set pricelist rule based on quantity in sale
        order"""
        for line in self:
            if (not line.product_id or line.display_type or not line.
                    order_id.pricelist_id):
                line.pricelist_item_id = False
            elif not line.product_no_variant_attribute_value_ids:
                line.pricelist_item_id = (
                    line.order_id.pricelist_id._get_product_rule(
                        line.product_id,
                        line.product_uom_qty or 1.0,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                    ))
            else:
                line.pricelist_item_id = (
                    line.order_id.pricelist_id._origin.with_context(
                        order_id=line.order_id._origin,
                        attribute_ids=line.product_no_variant_attribute_value_ids._origin)._get_product_rule(
                        line.product_id,
                        line.product_uom_qty or 1.0,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                    ))

    def _get_pricelist_price(self):
        """Compute the price given by the pricelist for the given line
        information.
        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()
        self.product_id.ensure_one()
        pricelist_rule = self.pricelist_item_id
        order_date = self.order_id.date_order or fields.Date.today()
        product = self.product_id.with_context(
            **self._get_product_price_context())
        qty = self.product_uom_qty or 1.0
        uom = self.product_uom or self.product_id.uom_id
        attribute = self.product_attributes
        price_list_attribute = pricelist_rule.product_attribute_id.name
        if price_list_attribute:
            if price_list_attribute in attribute.keys():
                attribute_list = []
                for rec in pricelist_rule.attribute_value_ids:
                    attribute_dict = {price_list_attribute: rec.name}
                    attribute_list.append(attribute_dict)
                is_subset = any(
                    attribute.items() >= d.items() for d in attribute_list)
                if is_subset:
                    price = pricelist_rule._compute_price(
                        product, qty, uom, order_date,
                        currency=self.currency_id)
                    return price
                else:
                    price = product.list_price
                    return price
        else:
            price = pricelist_rule._compute_price(
                product, qty, uom, order_date, currency=self.currency_id)
            return price
