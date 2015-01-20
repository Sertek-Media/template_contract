# coding=utf-8
from num2words import num2words
from openerp.tools import amount_to_text_en
from openerp.osv import osv , orm , fields
from openerp.addons.email_template import html2text
from openerp.tools.translate import _
from datetime import date

class template_contract(osv.osv):
    _inherit='account.analytic.account'
    _description='custom templates'
    
    def _get_date(self,cr, uid, ids, name, arg, context=None):
        if context is None:context = {}
        res={}
        for id in ids:
            res[id]=date.today()
        return res
    
    _columns={#'timesheet_invoice_ratio':
              'current_date':fields.function(_get_date,type='date'),
              'template_add':fields.one2many('contract.template.settings','template_id','Edit Report',readonly=False),
              'advance_percent':fields.float('Advance Percent (%)', help="Fill the advance payment percent"),
              'report_template':fields.many2one('contract.template.settings',string='Report Template',
                                            help="Select and save then see editable report page below to see the editable report",
                                            ),
              'report_text':fields.text('Report'),#for the editable report field
              'manager_details':fields.many2one('hr.employee'),# for the details of the manager(phone,email,etc)
              'sale_orders':fields.char('sale order list'),#sale order list
              'advance_amount_words':fields.char('advance number to text'),
              'fixed_words':fields.char('fixed words'),
              'time_words':fields.char('time words'),
              'vat_words':fields.char('vat words'),
              'full_amount_words':fields.char('full amount words'),
              }
    
    
    def create(self,cr,uid,vals,context):
        
        if vals.has_key('manager_id') and vals['manager_id']!=False:
            id_manager=vals['manager_id']
            #print('00000000000000000000000000000000000000000000000 id_manager',id_manager)
            user_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',id_manager)])
            ##print('00000000000000000000000000000000000000000000000 user',user_id)
            if len(user_id)!=0:
                vals['manager_details']=user_id[0]
            else:
                raise osv.except_osv(('ERROR !'), ('No such employee in Human resources. Please rectify it.'))
        
        return super(template_contract,self).create(cr,uid,vals,context)
    
    
    #def 
    
    
    def write(self,cr,uid,ids,vals,context):
        try:
            print('00000000000000000000000000000000000000 cr, uid , ids ,  write vals',cr,uid,ids,vals)
            #print('********************* ids',type(ids).__name__)
            if type(ids).__name__ == 'list':id_int = ids[0]
            #print('********************* ids',type(id_int).__name__)
            self_obj=self.browse(cr,uid,id_int,context)
            print "88888888888888888888888888888888888888888",self_obj,self_obj.partner_id
            sale_obj=self.pool.get('sale.order')
            salelist_ids=sale_obj.search(cr,uid,[('project_id','=',ids[0]),('state', '=', 'manual')])
            if salelist_ids:
                currency=sale_obj.browse(cr,uid,salelist_ids[0]).pricelist_id.currency_id.name
            else:
                currency="!!"
                print('00000000000000000000000000000 sale ids[0] currency id',currency)
            vat=0
            salelist=[]
            for i in salelist_ids:
                list=sale_obj.read(cr,uid,i,fields=['name'])['name']
                salelist.append(list)
                vat+=sale_obj.browse(cr,uid,i).amount_tax
            #print('0000000000000000000000000000 name',salelist)
            salelist_string=', '.join(salelist)
            vals['sale_orders']=salelist_string
            if self_obj.partner_id:
                customer_lang=(self.pool.get("res.partner").read(cr,uid,self_obj.partner_id.id,fields=['lang']))['lang']
                print('======================customer lang',customer_lang)
                lang1 ='lt' if (customer_lang=='lt_LT') else 'en_US' 
                print('lang',lang1)
                centu='Centų'
                cent=centu.decode('utf-8') if (lang1=='lt') else 'Cents'
                print('centu',cent)
            else:
                lang1 ='en_US'
                
            if self_obj.fix_price_invoices and self_obj.fix_price_to_invoice!=0:
                fixed_amount=self_obj.fix_price_to_invoice
                z='%.2f'% fixed_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['fixed_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['fixed_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                vat_amount=vat
                z='%.2f'% vat_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['vat_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['vat_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                '''mind the 1.21 below and 0.21 above'''
                full_amount=self_obj.fix_price_to_invoice+vat_amount
                z='%.2f'% full_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['full_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['full_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                advance_amount=(self_obj.advance_percent*full_amount)/100
                z='%.2f'% advance_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['advance_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['advance_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
            if self_obj.invoice_on_timesheets and self_obj.ca_to_invoice!=0:
                
                time_amount=self_obj.ca_to_invoice
                z='%.2f'% time_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['time_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['time_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                vat_amount=0
                z='%.2f'% vat_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['vat_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['vat_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                '''mind the 1.21 below and 0.21 above'''
                full_amount=self_obj.ca_to_invoice+vat_amount
                z='%.2f'% full_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['full_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['full_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
                advance_amount=(self_obj.advance_percent*full_amount)/100
                z='%.2f'% advance_amount
                a=str(z).split('.')
                print(a)
                if a[1]=='00':vals['advance_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' )')
                else: vals['advance_amount_words']=(str(z)+' '+currency+' ( '+num2words(abs(int(a[0])),lang=lang1)+' '+currency+' '+a[1]+' '+cent+' )')
                
            
            '''get all sales orders related to this contract ,  only executes when some field other than fix_price_to_invoice 
            or ca_to_invoice is edited'''
            
            #print('8888888888888888888888888888******************',self_obj.manager_id.id)
            #print('8888888888888888888888888888******************',self_obj.manager_details)
            ''' for manager(user) details in hr.employee''' 
            if vals.has_key('manager_id') and vals['manager_id']!=False:
                id_manager=vals['manager_id']
                #print('00000000000000000000000000000000000000000000000 id_manager',id_manager)
                user_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',id_manager)])
                #print('00000000000000000000000000000000000000000000000 user',user_id)
                if len(user_id)!=0:
                    vals['manager_details']=user_id[0]
                else:
                    raise osv.except_osv(('ERROR !'), ('No such employee in Human resources. Please rectify it.'))
            
            if not vals.has_key('manager_id') and self_obj.manager_id.id!=False and self_obj.manager_id!=False:
                id_manager=self_obj.manager_id.id
                #print('00000000000000000000000000000000000000000000000 id_manager',id_manager)
                user_id=self.pool.get('hr.employee').search(cr,uid,[('user_id','=',id_manager)])
                #print('00000000000000000000000000000000000000000000000 user',user_id)
                if len(user_id)!=0:
                    vals['manager_details']=user_id[0]
                else:
                    raise osv.except_osv(('ERROR !'), ('No such employee in Human resources. Please rectify it.'))
            
            
            ''' the next piece of code updates the editable field report , if the template is changed or even if any other value is changed'''
            #print('ok 1')
            #if self_obj.report_template.name != False:
            #    id_template=
        except:
            print ("   ************************Error Encountered !!!!  ***********************")
            raise
        
        
        return super(template_contract,self).write(cr,uid,ids,vals,context)
    
    
   
class template_settings(osv.osv):
    _name='contract.template.settings'
    _columns={'base_template':fields.boolean(string = 'is Base Template',help="Tick if you want this template to be a base template"),
              'template_id':fields.many2one('account.analytic.account',string='Template'),
              'name':fields.char('Contract Report',size=50,required=True),
              'report_html':fields.text('Report html'),
              'child_of_template':fields.many2one('contract.template.settings','Base Template')
              }   
    
    _defaults={
               'base_template':False
               } 

    def write (self,cr,uid,id,vals,context):
        if vals.has_key('child_of_template'):
            #print ("The base template has been changed",vals)
            html_description = self.browse(cr,uid,vals.get('child_of_template',False),context).report_html
            vals['report_html'] = html_description
        return super(template_settings,self).write(cr,uid,id,vals,context)
            
    def create(self,cr,uid,vals,context=None):
        if not vals.get('base_template',False):
            html_description = self.browse(cr,uid,vals.get('child_of_template',False),context).report_html
            vals['report_html'] = html_description
            id = super (template_settings,self).create(cr,uid,vals,context)
            return id
        else:
            return super(template_settings,self).create(cr,uid,vals,context)
        
    def onchange_child(self,cr,uid,id,base_template,context=None):
        value = {}
        if base_template == True:
            value = {'child_of_template':False}
        return {'value':value}
    
class contract_template_wizard(osv.osv_memory):
    _name = "contract.template.wizard"
    _descrition = "Preview COntract Template"
    _columns = {
                'report_html':fields.text('Report')
                }
    def print_contract(self,cr,uid,id,context):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'contract_report_mod',
        }
    def print_contract2(self,cr,uid,id,context):
        datas = {'ids': id}
        datas['model'] = 'contract.template.wizard'
        datas['form'] = self.read(cr, uid, id,context)[0]
        if context == None: context = {}
        return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'template_contract.report_qweb_contract_repeat',
                    'datas': datas,
                    'context':context
                }
        
        
        
