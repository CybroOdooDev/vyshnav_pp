# -*- coding: utf-8 -*-
{
    'name': "Intervlag Tier Price Validation",
    'version': "16.0.1.0.0",
    'summary': """InterVlag Tier Price Validation to set price list 
     based on product attributes in sale order""",
    'description': """This module is related to the
     InterVlag Tier Price Validation""",
    'category': 'Sale',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['sale', 'product', 'base', 'uom'],
    'data': [
        'views/product_pricelist_views.xml',
        'views/sale_order_views.xml'
    ],
    'license': "AGPL-3",
    'images': [],
    'installable': True,
    'application': True,
}

