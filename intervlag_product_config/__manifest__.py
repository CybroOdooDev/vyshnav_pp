# -*- coding: utf-8 -*-

{
    'name': "InterVlag Product Configurator",
    'version': "16.0.1.0.0",
    'summary': """InterVlag product configurator base""",
    'description': """This module is related to the InterVlag product 
                    configurator""",
    'category': 'Website',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['sale', 'product', 'intervlag_sale', 'website_sale',
                'sale_product_configurator'],
    'data': [
        'views/sale_order_views.xml',
        'views/product_attribute_views.xml',
        'views/templates.xml',
        'views/product_templates.xml',
        'views/product_configurator.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'intervlag_product_config/static/src/js/product_configurator.js',
            'intervlag_product_config/static/src/js/variant_mixin.js',
            'intervlag_product_config/static/src/js/configure_custom.js'
        ],
    },
    'license': "AGPL-3",
    'images': [],
    'installable': True,
    'application': True,
}

