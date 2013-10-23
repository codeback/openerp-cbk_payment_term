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

import pdb

class account_invoice(osv.osv):

    _name = "account.invoice"
    _inherit = "account.invoice"

    def _get_next_date_due(self, cr, uid, ids, field_names, arg, context=None):

        vals={}
        pdb.set_trace()
        for invoice in self.browse(cr, uid, ids)
            vals[invoice.id] = {}
            vals[invoice.id]['next_date_due'] = invoice.date_due
            for line in invoice.move_lines
                if line.date_maturity and not line.reconcile
                    if vals[invoice.id]['next_date_due'] < line.date_maturity
                        vals[invoice.id]['next_date_due'] = line.date_maturity

        return  vals

    _columns = {        
        'next_date_due' : fields.function(_get_next_date_due, string='Next Due Date', type='date'),
    }  
