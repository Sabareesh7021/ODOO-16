{
    'name': 'Product Owner',
    'version': '16.0.5.0.0',
    'depends': ['product', 'point_of_sale'
                ],
    'data': [
        'views/product.xml',
        ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'product_owner/static/src/js/action_manager.js',
            'product_owner/static/src/xml/pos_session.xml',
            'product_owner/static/src/xml/order_line_pos.xml',

        ]
        },
}



