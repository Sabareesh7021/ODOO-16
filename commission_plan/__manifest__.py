{
    'name': 'Commission Plan',
    'category': 'Sales/CRM',
    'version': '16.0.5.0.0',
    'depends': [
        'product',
        'sales_team',
        'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/commission_plan.xml',
        'views/commission_sales.xml'
    ],
    'installable': True,
    'application': True,
}
