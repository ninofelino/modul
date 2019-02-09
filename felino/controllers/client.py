#npm install odoo-xmlrpc
import odoorpc

host="nbi.falinwa.com"
odoo = odoorpc.ODOO(host, port=8069)
#print(odoo.db.list())
odoo.login('ninofelino', 'fashion2@gmail.com', 'fashion')
user = odoo.env.user
Order = odoo.env['product.product']
order_ids = Order.search([])
print(type(order_ids))
#Order = odoo.cr.execute('select * from felino_dbinv ') 

for order in Order.browse(order_ids):
    print order.name
