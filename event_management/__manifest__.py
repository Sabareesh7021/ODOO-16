{
    'name': 'Event management',
    'category': 'Sales/CRM',
    'version':'16.0.3.0.1',
    'depends':
        ['base','mail', 'uom'],
    'data':[
        'security/ir.model.access.csv',
        'view/event_management_type.xml',
        'view/event_management_booking.xml',
        'view/event_management_service.xml',
        'view/event_management_catering.xml',
        'data/data.xml',
        'view/catering_menu.xml'

        ],
    'installable' : True,
    'application' : True,


}