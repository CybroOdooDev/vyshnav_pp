# -*- coding: utf-8 -*-
{
    'name': "InterVlag Attribute Restriction",
    'version': "16.0.1.0.0",
    'summary': """InterVlag attribute restriction base""",
    'description': """This module is related to the InterVlag attribute 
     restrictions""",
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['sale','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/restriction_configurator_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/Intervlag_attribute_restriction/static/src/js/**/*',
            '/Intervlag_attribute_restriction/static/src/css/**/*',
        ],
      },
    'license': "AGPL-3",
    'images': [],
    'installable': True,
    'application': True,
}
