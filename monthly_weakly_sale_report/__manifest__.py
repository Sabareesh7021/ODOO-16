{
    'name': 'Sale report M or W',
    'version': '16.0.1.0.0',
    'summary': 'sale reporting ',
    'sequence': 10,


    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'report/report_pdf.xml',
        'report/report_temp.xml',
        'data/schedule_action.xml',
        'views/conf.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': True,

}
