# -*- encoding: utf-8 -*-
##############################################################################
#
#    cbk_crm_information: CRM Information Tab
#    Copyright (c) 2013 Codeback Software S.L. (http://codeback.es)    
#    @author: Miguel García <miguel@codeback.es>
#    @author: Javier Fuentes <javier@codeback.es>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from osv import fields, osv
from datetime import datetime, timedelta  

class account_invoice(osv.osv):

    _name = "account.invoice"
    _inherit = "account.invoice"
    
    def _get_next_payment(self, cr, uid, ids, field_names, arg, context=None):

        vals={}
        for invoice in self.browse(cr, uid, ids):            
            vals[invoice.id] = invoice.date_due
            next_payment = invoice.residual
            if invoice.move_id:
                for line in invoice.move_id.line_id:
                    if line.date_maturity and not line.reconcile:
                        if vals[invoice.id] > line.date_maturity:
                            vals[invoice.id] = line.date_maturity
                            
                            if invoice.type == "out_invoice" or invoice.type == "in_refund":
                                next_payment = line.debit
                            else:
                                if invoice.type == "in_invoice" or invoice.type == "out_refund":
                                    next_payment = line.credit
            value = {
                's_next_date_due': vals[invoice.id], 
                'next_payment': next_payment,
            }
            self.write(cr, uid, [invoice.id], value, context=context)
        return  vals

    _columns = {        
        'next_date_due' : fields.function(_get_next_payment, string='Next Due Date', type='date'),
        's_next_date_due': fields.date(string='Next Due Date', readonly=True), # Necesaria para poder agrupar en el buscador (en campos function no se puede)
        'next_payment' : fields.float(string='Next Payment', readonly=True),
    }  

    
    