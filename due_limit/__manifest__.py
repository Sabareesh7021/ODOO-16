{
    'name': 'Due Limit',
    'version': '16.0.5.0.0',
    'depends': ['contacts', 'point_of_sale'
                ],
    'data': [
        'views/contact.xml',
        ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
           'due_limit/script/src/js/limit.js'
        ]
        },
}



