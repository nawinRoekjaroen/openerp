import csv
import xmlrpclib
import datetime


username='admin'
pwd='admin'
dbname='opernerp_test'
host='localhost'
sock_common=xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/common')
uid=sock_common.login(dbname,username,pwd)
sock=xmlrpclib.ServerProxy('http://'+host+':4069/xmlrpc/object')

#name_id=sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
#print(name_id)
#code_id=sock.execute(dbname,uid,pwd,'res.currency','search',[('code','=','Bs')])
#print(code_id)
date = '07/11/2019'
filename = 'code.csv'
def table_writer(filename,header):
    wr = csv.DictWriter(file(filename, "w"),fieldnames=header)
    wr.writerow(dict(zip(header,header)))
    return wr

wr = table_writer('missing_%s'%filename, ['code','description']) 
#print('table=',table_writer)
chk_test_id=sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','Test13')])
print('chk=',chk_test_id)
if not chk_test_id:
    test_val={'name':'Test13',
        'accuracy':'29',
        }
    print 'test_val = ',test_val
    currency_id=sock.execute(dbname,uid,pwd,'res.currency','create',test_val)
    #print('move_id=',move_id)
move_id=sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','Test13')])
print'rate=',move_id[0]
#line_id=sock.execute(dbname,uid,pwd,'res.currency.rate','search',[('rate','in',move_id)])
#print'line_id =',line_id
acc_ids=[]
#for x in sock.execute(dbname,uid,pwd,'res.currency.rate','read',line_id):
#    acc_ids.append(x['account_id'][0])
rate=[]
for rate_id in sock.execute(dbname,uid,pwd,'account.account','read',acc_ids):
    rate.append(rate_id['rate'])
chk_code=[]
for line in csv.DictReader(open('rate.csv')):
    account_id=sock.execute(dbname,uid,pwd,'res.currency.rate','search',[('rate','=',line['rate'])])
    print'account_id=',account_id
    check_mode=line['rate'][0]
    print'check_mode=',check_mode
    chk_code=line['rate']
    print'chk_code',chk_code
    if chk_code not in rate:
        if not account_id:
            print'Not have rate---->'+line['rate']+'------>Write to missing_code.csv'
            wr.writerow({'code':line['rate'],'description':'Not Fount Rate'})
    if len(account_id) >= 1:
        if check_mode == '1':
            rate = line['rate']
            print rate
            if rate >= 0:
                print 'rate+++++++ =',rate  
            else:
                print 'rate------- =',rate
            move_line={'currency_id':move_id,
                       #'name' : line['date'],
                       'rate' : line['rate'],
                       } 
            print 'move_line',move_line
            res = sock.execute(dbname,uid,pwd,'res.current.rate','create',move_line)
            print 'res',res
            if res:
            
                if res:
                    
                    print "created %s"%line['rate']
            if check_mode == '2':
                date = datetime(line['date'])
                if date >= 0:
                    print '----------- = ',date
                else:
                    print '----------- = ',date
                move_line_val = { 'rate' :move_id[0], 
                                 'name' : line['date']
                                #, 'account_id' : account_id[0] if account_id else False
                                #, 'debit' : line_uncredit
                                #, 'account_id' : account_id[0]
                                #, 'credit' : rate
                               # , 'company_id' : company_id[0] if company_id else False
                                }
                res = sock.execute(dbname, uid, pwd, 'res.currency.rate', 'create', move_line_val)
                if res:
                    
                    print "created %s"%line['date']
            #if check_mode == '3':
              #  line_uncredit = 0
               # amount = float(line['amount'])
               # if amount >= 0:
               #     print '-----------Check positive = ',amount
               # else:
                #    print '-----------Check Nagative = ',amount
                 #   line_uncredit = amount * -1
                  #  amount = 0
               # move_line_val = { 'move_id' : move_id[0]
                #                , 'name' : line['name']
                 #               , 'account_id' : account_id[0] if account_id else False
                  #              , 'debit' : line_uncredit
                                #, 'account_id' : account_id[0]
                   #             , 'credit' : amount
                    #            , 'company_id' : company_id[0] if company_id else False
                     #           }
              #  res = sock.execute(dbname, uid, pwd, 'res.currency.rate', 'create', move_line_val)
               # if res:
                #    print "created %s"%line['name']
    else:
        print '--------->Same rate = ',line['rate'] 
print "FINISHED"

    


