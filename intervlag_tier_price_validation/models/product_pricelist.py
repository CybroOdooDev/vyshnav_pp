# -*- coding: utf-8 -*-
import json

from odoo import models, api


class PricelistItem(models.Model):
    """Inherited product.pricelist class to override required functions"""
    _inherit = "product.pricelist"

    def _get_applicable_rules_domain(self, products, date, **kwargs):
        """Overriden function to modify domain to get applicable rules"""
        if products._name == 'product.template':
            templates_domain = ('product_tmpl_id', 'in', products.ids)
            products_domain = ('product_id.product_tmpl_id', 'in', products.ids)
            return [
                ('pricelist_id', '=', self.id),
                '|', ('categ_id', '=', False),
                ('categ_id', 'parent_of', products.categ_id.ids),
                '|', ('product_tmpl_id', '=', False), templates_domain,
                '|', ('product_id', '=', False), products_domain,
                '|', ('date_start', '=', False), ('date_start', '<=', date),
                '|', ('date_end', '=', False), ('date_end', '>=', date),
            ]
        else:
            product_attribute_values = self.env.context.get('attribute_ids')

            if product_attribute_values:
                attribute_values = product_attribute_values.product_attribute_value_id
                attribute_domain = (
                'attribute_value_ids', 'in', attribute_values.ids)
                templates_domain = (
                    'product_tmpl_id', 'in', products.product_tmpl_id.ids)
                products_domain = ('product_id', 'in', products.ids)
                return [
                    ('pricelist_id', '=', self.id), attribute_domain,
                    '|', ('categ_id', '=', False),
                    ('categ_id', 'parent_of', products.categ_id.ids),
                    '|', ('product_tmpl_id', '=', False), templates_domain,
                    '|', ('product_id', '=', False), products_domain,
                    '|', ('date_start', '=', False), ('date_start', '<=', date),
                    '|', ('date_end', '=', False), ('date_end', '>=', date),
                ]
            else:
                templates_domain = (
                    'product_tmpl_id', 'in', products.product_tmpl_id.ids)
                products_domain = ('product_id', 'in', products.ids)
                return [
                    ('pricelist_id', '=', self.id),
                    '|', ('categ_id', '=', False),
                    ('categ_id', 'parent_of', products.categ_id.ids),
                    '|', ('product_tmpl_id', '=', False), templates_domain,
                    '|', ('product_id', '=', False), products_domain,
                    '|', ('date_start', '=', False), ('date_start', '<=', date),
                    '|', ('date_end', '=', False), ('date_end', '>=', date),
                ]
