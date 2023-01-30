{
    'name': 'Idle Timer',
    'version': '16.0.1.0.0',
    'author': 'Sabareesh S',
    'summary': 'Idle Time',
    'sequence': 10,

    'depends': ['base', 'survey'],
    'data': [
        'views/idle_time.xml',
        'views/timer.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'idle_timer/static/src/js/idle_time.js'
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': True,

}
