# -*- coding: utf-8 -*-
{
    'name': 'Intervlag Sale Order Helpdesk',
    'version': '16.0.0.1.0',
    'category': 'Services',
    'summary': 'Adds features to Generate helpdesk tickets from sale order '
               'also to create sale order from helpdesk ticket ',
    'description': 'Some cases we need to generate helpdesk tickets from sale '
                   'orders.By using this module we can generate helpdesk ticket'
                   'from sale order also we can create sale orders from '
                   'generated tickets',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['helpdesk', 'sale', 'helpdesk_sale', 'helpdesk_sale_timesheet',
                'helpdesk_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/complaint_category_views.xml',
        'views/sale_order_views.xml',
        'views/complaint_department_views.xml',
        'views/helpdesk_ticket_report_analysis_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_team_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'intervlag_sale_order_helpdesk/static/src/js/helpdesk_pivot.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
}
