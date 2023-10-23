# -*- coding: utf-8 -*-
{
    'name': "InterVlag Price Configurator",
    'version': "16.0.1.0.0",
    'summary': """InterVlag price configurator base""",
    'description': """This module is related to the InterVlag price 
                    configurator""",
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['sale', 'contacts', 'intervlag_sale',
                'intervlag_delivery_fedex',
                'intervlag_gift_meter','sale_product_configurator',
                'intervlag_product_config'],
    'data': [
        'data/print_type_data.xml',
        'security/ir.model.access.csv',
        'views/price_configurator_views.xml',
        'views/product_attribute_views.xml',
        'views/product_attribute_value_views.xml',
        'views/product_template_view.xml',
        'views/sale_order_views.xml',
        'views/variant_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/intervlag_price_config/static/src/css/**/*',
            '/intervlag_price_config/static/src/js/**/*',
        ],
    },
    'license': "AGPL-3",
    'images': [],
    'installable': True,
    'application': True,
}
