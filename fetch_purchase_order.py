import xmlrpc.client

url_db1 = "http://localhost:8015"
db_1 = 'db15_1_new'
username_db_1 = '1'
password_db_1 = '41511c9b7e359b4f2f4da8638efde1f3fe509a90'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
model_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))


uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})

url_db2 = "http://localhost:8016"
db_2 = 'odoo_16'
username_db_2 = '1'
password_db_2 = '8cb24851d4e2b3dbdaf6556febdb783661a7be52'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
model_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))

uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

db_purchase = model_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]],
                                 {'fields': ['name', 'partner_id', 'company_id', 'user_id', 'amount_total', 'state',
                                             'order_line',
                                             'date_order',
                                             'date_planned']})
order_line = model_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read', [[]],
                                 {'fields': ['product_id', 'product_qty', 'name', 'price_unit', 'taxes_id', 'price_subtotal']})
db_2_order = model_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'search_read', [[]],
                                {'fields': ['name', 'order_line', 'date_order', 'partner_id']})

print(order_line)
db1_date = [i['date_order'] for i in db_2_order]
db1_partner = [i['partner_id'] for i in db_2_order]


for rec in db_purchase:
    if rec['date_order'] not in db1_date and rec['partner_id'] not in db1_partner:
        print(8888888888888)
        vals = []
        for i in order_line:
            if i['id'] in rec['order_line']:
                vals.append((0, 0, {
                    'product_id': i['product_id'][0],
                    'name': i['name'],
                    'product_qty': i['product_qty'],
                    'price_unit': i['price_unit'],
                    'taxes_id': i['taxes_id'],
                    'price_subtotal': i['price_subtotal']
                    }))

        partner_id = model_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [
                {'partner_id': rec['partner_id'][0],
                 'company_id': rec['company_id'][0],
                 'user_id': rec['user_id'][0],
                 'amount_total': rec['amount_total'],
                 'state': rec['state'],
                 'order_line': vals,
                 'date_order': rec['date_order'],
                 'date_planned': rec['date_planned']
                 }
            ])
    else:
        print(1234567890)
        pass
