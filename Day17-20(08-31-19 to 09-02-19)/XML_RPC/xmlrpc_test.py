import csv
import xmlrpclib
import datetime 


username='admin'
print(username)
pwd='admin'
print(pwd)
dbname='opernerp_test'
print(dbname)
host='localhost'
print(host)
sock_common=xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/common')
print(sock_common)
uid=sock_common.login(dbname,username,pwd)
print(uid)
sock=xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/object')
print(sock)
name_id = sock.execute(dbname,uid,pwd,'hr.employee','search',[('name','=','qqqqwwww')])
print(name_id)
#country_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('country','=','Belgium')]) 
#print(country_id)
#birthday = sock.execute(dbname, uid, pwd, 'hr.employee', 'search', [('birthday','=','08/12/2019')])
#print(birthday)
#ids=sock.execute(dbname,uid,pwd,'hr.employee', 'read',name,['name'])
#print(ids)
#count=sock.execute(dbname,uid,pwd,'res.partner','read',country_id,['country'])
#print(count)
#results=sock.execute(dbname,uid,pwd,'hr.employee', 'write',name,{'name':'tes123'})
#print(results)
date='09/30/2019'
print(date)

filename = 'code.csv' #your filename Ex. missing_code.csv
def table_writer(filename,header):
    wr = csv.DictWriter(file(filename, "w"),fieldnames=header)
    wr.writerow(dict(zip(header,header)))
    return wr

wr = table_writer('missing_%s'%filename, ['code','description']) #create column in csv file

chk_move_id = sock.execute(dbname, uid, pwd, 'purchase.order', 'search', [('name','=','test123')])

if not chk_move_id:
    move_vall={'name':'test123',
        'date':date,
        'name_id':name_id[0] if name_id else False,
        #'country_id':country_id[0],
        #'birthday':birthday[0]
        }
    print(move_vall)
 
move_id = sock.execute(dbname, uid, pwd, 'purchase.order', 'create', move_vall)
print(move_id)
count = sock.execute(dbname,uid,pwd,'purchase.order','search',[('name','=','test123')])
print(count)
#results=sock.execute(dbname,uid,pwd,'hr.employee','unlink',name)
#iprint(results)

