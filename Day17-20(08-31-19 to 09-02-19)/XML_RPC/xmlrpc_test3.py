import xmlrpclib

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'opernerp_test'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:4069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:4069/xmlrpc/object')
print 'sock = ',sock
partner = {
   'name': 'Fabien Pinckaers',
}
print'partner',partner
partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner)
print 'partner_id',partner_id
address = {
   'partner_id': partner_id,
}
print 'add',address
address_id = sock.execute(dbname, uid, pwd, 'res.partner.address', 'create', address)
