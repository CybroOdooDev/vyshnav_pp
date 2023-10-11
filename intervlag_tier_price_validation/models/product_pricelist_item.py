# -*- coding: utf-8 -*-
import json

from odoo import fields, models, tools, api


class PricelistItem(models.Model):
    """Inherited product.pricelist.item class to add attributes and its
    values in pricelist"""
    _inherit = "product.pricelist.item"

    product_attribute_id = fields.Many2one('product.attribute',
                                           string="Product attributes")
    attribute_value_ids = fields.Many2many('product.attribute.value',
                                           relation='product_attribute_value_product_pricelist_item_rel',
                                           string="Values",
                                           domain="[('attribute_id', '=', "
                                                  "product_attribute_id)]")

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        """Function to set domain for product attribute field"""
        return {'domain': {'product_attribute_id': [('id', 'in',
                                                       self.
                                                       product_tmpl_id.
                                                       attribute_line_ids.attribute_id.ids)]}}

    def _is_applicable_for(self, product, qty_in_product_uom):
        """Check whether the current rule is valid for the given product & qty.
        Note: self.ensure_one()
        :param product: product record (product.product/product.template)
        :param float qty_in_product_uom: quantity, expressed in product UoM
        :returns: Whether rules is valid or not
        :rtype: bool
        """
        order_id = self.env.context.get('order_id')
        quantity = 0
        if order_id:
            suitable_lines = self.env['sale.order.line'].search(
                [('order_id', '=', order_id.id), (
                    'product_no_variant_attribute_value_ids.product_attribute_value_id',
                    'in',
                    self.attribute_value_ids.ids)])
            for rec in suitable_lines:
                quantity += rec.product_uom_qty
        self.ensure_one()
        product.ensure_one()
        res = True
        is_product_template = product._name == 'product.template'
        if self.min_quantity and quantity < self.min_quantity:
            res = False

        elif self.applied_on == "2_product_category":
            if (
                    product.categ_id != self.categ_id
                    and not product.categ_id.parent_path.startswith(
                self.categ_id.parent_path)
            ):
                res = False
        else:
            # Applied on a specific product template/variant
            if is_product_template:
                if (self.applied_on == "1_product" and product.id != self.
                        product_tmpl_id.id):
                    res = False
                elif self.applied_on == "0_product_varsetiant" and not (
                        product.product_variant_count == 1
                        and product.product_variant_id.id == self.product_id.id
                ):
                    # product self acceptable on template if has only one variant
                    res = False
                else:
                    if self.applied_on == "1_product" and product.product_tmpl_id.id != self.product_tmpl_id.id:
                        res = False
                    elif self.applied_on == "0_product_variant" and product.id != self.product_id.id:
                        res = False
            return res
        return res
