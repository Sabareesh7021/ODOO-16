{
    'name': 'Snippet elearning',
    'version': '16.0.5.0.0',
    'depends': ['website', 'website_slides'
                ],
    'data': [
        'views/view.xml',
        ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/snippet_elearning/static/src/xml/carousal.xml',
            '/snippet_elearning/static/src/js/dynamic.js',
            '/snippet_elearning/static/src/css/dynamic.css',

        ]
        },
}



