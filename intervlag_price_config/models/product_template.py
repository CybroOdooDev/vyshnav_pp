# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    print_type = fields.Selection([('digital', 'Digital Print per m2'),
                                   ('digital_beach',
                                    'Digital Print per quantity'),
                                   ('screen', 'Screen Print')],
                                  string="Printing")
