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
from operator import itemgetter

class account_invoice(osv.osv):

    _name = "account.invoice"
    _inherit = "account.invoice"
    
    def _get_next_payment(self, cr, uid, ids, field_names, arg, context=None):

        vals={}
        for invoice in self.browse(cr, uid, ids):            
            
            date_due = invoice.date_due
            vals[invoice.id] = date_due
            next_payment = invoice.residual

            if invoice.move_id:                

                lines = sorted(invoice.move_id.line_id, key=itemgetter('date_maturity'), reverse=True)

                numLines = 0
                for line in lines:                    
                    if line.date_maturity and not line.reconcile:
                        numLines += 1
                        if numLines == 1 and date_due != line.date_maturity:
                            date_due = line.date_maturity
                            vals[invoice.id] = date_due

                        if vals[invoice.id] >= line.date_maturity:
                            vals[invoice.id] = line.date_maturity
                            
                            if invoice.type == "out_invoice" or invoice.type == "in_refund":
                                next_payment = line.debit
                            else:
                                if invoice.type == "in_invoice" or invoice.type == "out_refund":
                                    next_payment = line.credit
            value = {
                's_next_date_due': vals[invoice.id], 
                'next_payment': next_payment,
                'date_due': date_due
            }
            self.write(cr, uid, [invoice.id], value, context=context)
        return  vals

    _columns = {        
        'next_date_due' : fields.function(_get_next_payment, string='Next Due Date', type='date'),
        's_next_date_due': fields.date(string='Next Due Date', readonly=True), # Necesaria para poder agrupar en el buscador (en campos function no se puede)
        'next_payment' : fields.float(string='Next Payment', readonly=True),
        'move_unrec_line_ids': fields.related('move_id', 'line_id', type="one2many", relation="account.move.line", string="Lines", store=False, readonly=True)
    }  

    def on_create_write(self, cr, uid, id, context=None):
        if not id:
            return []

        pool = self.pool.get('account.move.line')
        ml = pool.browse(cr, uid, id, context=context)
        return map(lambda x: x.id, ml.move_id.line_id)

    
    