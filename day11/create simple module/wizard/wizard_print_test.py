import wizard
import datetime
import netsvc

form='''<?xml version="1.0"?>
<form string="Test Print">
</form>'''

fields = {
    'month': dict(string=u'', type='',  selection=[(x, datetime.date(2000, x, 1).strftime('%B')) for x in range(1, 13)]),
    'year': dict(string=u'', type='',),
    'user_ids': dict(string=u'', type='', relation='',),
}

def _get_value(self, cr, uid, data, context):
    today=datetime.date.today()
    return dict(month=today.month, year=today.year)

class wizard_report(wizard.interface):
    states={
        'init':{
            'actions':[_get_value],
            'result':{'type':'form', 'arch':form, 'fields':fields, 'state':[('end','Cancel','gtk-cancel'),('report','Print','gtk-print')]}
        },
        'report':{
            'actions':[],
            'result':{'type':'print', 'report':'test.analytical.users', 'state':'end'}
        }
    }
wizard_report('test.analytical.users')
