from openerp.osv import fields, osv

class report_preview(osv.osv_memory):
    _name = "report.preview"
    _description = "Report Template Preview"

    _columns={'report_preview':fields.text('Report Preview',)}