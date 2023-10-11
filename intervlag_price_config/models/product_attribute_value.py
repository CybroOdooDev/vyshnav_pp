from odoo import models, fields


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    print_type = fields.Selection([('digital', 'Digital Print per m2'),
                                   ('digital_beach', 'Digital Print per quantity'),
                                   ('screen', 'Screen Print')],
                                  string="Printing")
