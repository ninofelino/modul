import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(odoo.db.list())
odoo.login('ninofelino', 'ninofelino12@gmail.com', 'nuansabaru')