# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'Contract Templates',
    'version' : '1.1',
    'author' : 'Shivam Goyal',
    'category' : 'templates',
    'description' : """
Contract Templates
==================
   """,
    'website': '',
    'images' : [], #'/images/image_name.png'
    'depends' : ['base','account_analytic_analysis','report_webkit','hr','base_vat'],#account_analytic_analysis
    'data': ['paper_format.xml','template_contract_report.xml','template_contract.xml','template_settings.xml',
             'report/template_contract_custom.xml','security/ir.model.access.csv',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
