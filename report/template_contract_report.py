import time
from openerp.report import report_sxw
class contract_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(contract_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'today':time.strftime("%Y%m%d"),
                                  'cr':cr,
                                  'uid': uid,
                                  })
    
report_sxw.report_sxw('report.contract_report_mod','contract.template.wizard','addons/template_contract/report/template_contract_report.mako',
parser = contract_report)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
