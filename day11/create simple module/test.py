from osv import fields, osv
from tools import config
import math
from tools.translate import _
class TestModule(osv.osv):
    _name = "test.module"

    _columns = {
        'title':fields.selection([('mr','MR.'),('miss','MISS'),('mrs','MRS.')],'Title'),
        'name':fields.char("First Name",size=128, required=True),
        'laname':fields.char("Last Name",size=10,),
        'age':fields.integer('AGE', size=3),
        'sex':fields.selection([('',''),('male','Male'),('female','Female')],'Gender'),
        'birthday':fields.date('Date Of Birth', ),
        'country_id':fields.many2one('res.country','Nationality'),
        'religion_id':fields.selection([('buddhism','Buddhism'),('cristianity','Cristianity'),('islam','Islam')], 'Religion'), 
        'marital':fields.selection([('maried','Maried'),('unmaried','Unmaried'),('divorced','Divorced')],'Marital'),
        'address_home_id':fields.many2one('res.partner.address','Home Address'),
        'work_location':fields.char('Work Location',size=32),
        'work_phone':fields.char('Work Phone',size=12),
        'phone':fields.char('Phone',size=12,),
        'email':fields.char('Email',size=32),
        'note':fields.text('Note',size=50),
        'gid':fields.integer('GID',size=6),
        'date_id':fields.datetime('Date Start'),
        'test_id':fields.one2many('edu.psn','id_test','TimeTime'),
     }

    def _check_recursion(self, cr, uid, ids):
        level = 100
        while len(ids):
            cr.execute('SELECT DISTINCT country_id FROM TestModule '\
                       'WHERE id IN %s', (tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True
TestModule()

class Edu_psn(osv.osv):
    _name = "edu.psn"
 
    _columns = {
    'id_test':fields.many2one('test.module','Time'),
    'graduated':fields.date('Graduated'),
    'test':fields.integer('TTest',size=23),
    'degree':fields.selection([('senior','Senior High School'),('voc','Vocational Certificate'),('dip','Diploma'),('bach','Bachelor Degree')], 'Degree'),

    }
Edu_psn()
