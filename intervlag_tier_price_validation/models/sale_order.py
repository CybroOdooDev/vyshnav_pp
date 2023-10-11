# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    """Inherited sale.order class to update functions related to
    pricleist"""
    _inherit = "sale.order"

    def action_update_prices(self):
        """overriden function to call '_compute_pricelist_item_id()' function"""
        self.order_line._compute_pricelist_item_id()
        super().action_update_prices()

