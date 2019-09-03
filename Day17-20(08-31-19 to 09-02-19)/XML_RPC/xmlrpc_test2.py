import csv
#import re
#import xlrd
import xmlrpclib
#import time


username = 'admin' #username
pwd = 'admin' #password
dbname = 'opernerp_test' #database
host = 'localhost'
sock_common = xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/object')
print(sock)
filename = '.csv' #your filename Ex. missing_code.csv
def table_writer(filename,header):
    wr = csv.DictWriter(file(filename, "w"),fieldnames=header)
    wr.writerow(dict(zip(header,header)))
    return wr

wr = table_writer('miss%s'%filename, ['date','description']) 
chk_inform=sock.execute(dbname, uid, pwd, 'res.currency','search', [('name','=','Test2')])
if not chk_inform:
    inform = {
        #'title':'mr.',
        'name':'Test2',
        'code':'123',
        'rounding':'1.2',
        'accuracy':'12',
        }
    inform_id=sock.execute(dbname, uid, pwd, 'res.currency','create',inform)
    print(inform_id)
inform_id=sock.execute(dbname, uid, pwd, 'res.currency', 'search',[('name','=','Test2')])
print(inform_id)
inf_id=sock.execute(dbname, uid, pwd, 'res.currency.rate', 'search',[('rate','in',inform_id)])
print(inf_id)
acc_ids=[]
for x in sock.execute(dbname, uid, pwd, 'res.currency.rate', 'read', inf_id):
    acc_ids.append(x['account_id'][0])
date=[]
