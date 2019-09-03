from report.interface import report_rml
from report.interface import toxml
import datetime

class report_custom(report_rml):

    def get_month_name(self, cr, uid, month):
        _months = {1:_("January"), 2:_("February"), 3:_("March"), 4:_("April"), 5:_("May"), 6:_("June"), 7:_("July"), 8:_("August"), 9:_("September"), 10:_("October"), 11:_("November"), 12:_("December")}
        return _months[month]

    def get_weekday_name(self, cr, uid, weekday):
        _weekdays = {1:_('Mon'), 2:_('Tue'), 3:_('Wed'), 4:_('Thu'), 5:_('Fri'), 6:_('Sat'), 7:_('Sun')}
        return _weekdays[weekday]

    def create_xml(self, cr, uid, ids, data, context):

        # Computing the dates (start of month: som, and end of month: eom)
        som = datetime.date(data['form']['year'], data['form']['month'], 1)
        eom = som + datetime.timedelta(lengthmonth(som.year, som.month))
        date_xml = ['<date month="%s" year="%d" />' % (self.get_month_name(cr, uid, som.month), som.year), '<days>']
        date_xml += ['<day number="%d" name="%s" weekday="%d" />' % (x, self.get_weekday_name(cr, uid, som.replace(day=x).weekday()+1), som.replace(day=x).weekday()+1) for x in range(1, lengthmonth(som.year, som.month)+1)]
        date_xml.append('</days>')
        date_xml.append('<cols>2.5cm%s,2cm</cols>\n' % (',0.7cm' * lengthmonth(som.year, som.month)))

        emp_xml=''
        for id in data['form']['user_ids'][0][2]:
            emp_xml += emp_create_xml(cr, id, som, eom)

        # Computing the xml
        #Without this, report don't show non-ascii characters (TO CHECK)
        date_xml = '\n'.join(date_xml)

        xml='''<?xml version="1.0" encoding="UTF-8" ?>
        <report>
        </report>
        ''' 

report_custom('report.test.analytical.users', 'test.module', '', 'addons/ac_test/report/test.xsl')

