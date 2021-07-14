import xmlrpc.client


def query_get_data(odoo_model, method, fields, search_filter=[]):
    url = "http://localhost:8069"
    db = "phitenodoo14"
    username = "admin"
    password = "ca83214a5ffa64e659702b8ffc7dfc855e3a03a1"
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model_query = models.execute_kw(db, uid, password, odoo_model, method,
                                    search_filter, fields)
    return model_query


def query_create_data(odoo_model, fields):
    url = "http://localhost:8069"
    db = "phitenodoo14"
    username = "admin"
    password = "ca83214a5ffa64e659702b8ffc7dfc855e3a03a1"
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return models.execute_kw(db, uid, password, odoo_model, 'create', [fields])


def query_write_data(id, model, field):
    url = "http://localhost:8069"
    db = "phitenodoo14"
    username = "admin"
    password = "ca83214a5ffa64e659702b8ffc7dfc855e3a03a1"
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
       
    return models.execute_kw(db, uid, password, model, 'write', [[id], field],{})
