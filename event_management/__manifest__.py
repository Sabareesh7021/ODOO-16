{
    'name': 'Event management',
    'category': 'Sales/CRM',
    'version': '16.0.3.0.1',
    'installable': True,
    'application': True,
    'depends':
        ['base', 'mail', 'uom', 'account_payment'],
    'data': [
        'security/ir.model.access.csv',
        'view/event_management_type.xml',
        'view/event_management_booking.xml',
        'view/event_management_service.xml',
        'view/event_management_catering.xml',
        'data/data.xml',
        'view/catering_menu.xml',
        'wizards/wizard_reporting.xml',
        'wizards/reporting_event_booking.xml',

        ],
    'assets': {
        'web.assets_backend': [
            '/event_management/static/src/js/action_manager.js'
                ]
        }
}
