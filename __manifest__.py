# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Name Card Request',
    'version' : '1.0.0',
    'category': 'Name Card Request',
    'author': 'Odoo Mates',
    'sequence': -100,
    'description': """Name Card Request""",
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'views/namecard.xml',
        'report/name_card.xml',
        'report/report.xml',
    ],
    'depends': ['mail'],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
