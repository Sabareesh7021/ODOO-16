{
    'name': 'coc',
    'category': 'Sales/CRM',
    'version': '16.0.3.0.1',
    'installable': True,
    'application': True,
    'depends':
        ['sale'],
    'data': [
        'views/coc.xml'
           ],
    'assets': {
        'web.assets_backend': [
        '/coc/static/src/css/coc.css'
        ]
           }
}
