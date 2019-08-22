from osv import fields, osv
import datetime

class TestModule(osv.osv):
    _name = 'test.module'
    _inherit = 'res.partner'
    _colunms = {
        'title':fields.selection([('mr','MR.'),('miss','MISS'),('mrs','MRS.')]),
        'gender':fields.boolean('Male'),
        'gender2':fields.boolean('Female'),
        'fname':fields.char('First Name',size=16),
        'lname':fields.char('Last Name',size=16),
        'age':fields.integer('AGE', size=16),
        'dateofbirth':fields.datetime('Date Of Birth'),
     }
    _defaults = {
    }
TestModule()

