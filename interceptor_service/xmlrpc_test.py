import xmlrpc.client
url = "http://localhost:8069"
db = "phitenodoo14"
username = "admin"
password = "ca83214a5ffa64e659702b8ffc7dfc855e3a03a1"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
so = models.execute_kw(db, uid, password, 'sale.order', 'create', [{"name":"ASD-852/FDR/01/15","partner_id":11}])

import pdb;pdb.set_trace()
