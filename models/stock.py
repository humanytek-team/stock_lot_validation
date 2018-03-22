# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
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
###############################################################################

from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMoveLots(models.Model):
    _inherit = 'stock.move.lots'

    @api.onchange('lot_id', 'quantity_done')
    def onchange_lot(self):
        res = {}
        if self.env.context.get('raw_material'):
            StockQuant = self.env['stock.quant']
            quants = StockQuant.search([
                    ('product_id.id', '=', self.product_id.id),
                    ('lot_id.id', '=', self.lot_id.id),
                    ('location_id.id', '=', self.env.context.get('location_id'))
                    ])
            qty_total = 0
            for quant in quants:
                qty_total += quant.qty
            if self.quantity_done > qty_total:
                self.quantity_done = 0
                message = "No tiene stock de este lote"
                res['warning'] = {'title': _('Warning'), 'message': message}
        return res


class StockPackOperationLot(models.Model):
    _inherit = 'stock.pack.operation.lot'

    @api.onchange('lot_id', 'qty')
    def onchange_lot(self):
        res = {}
        if self.lot_id and self.qty > 0:
            if self.env.context.get('field_parent') and self.env.context.get('field_parent') == 'operation_id':
                StockQuant = self.env['stock.quant']
                quants = StockQuant.search([
                        ('product_id.id', '=',
                            self.env.context.get('default_product_id')),
                        ('lot_id.id', '=', self.lot_id.id),
                        ('location_id.id', '=', self.env.context.get('location_id'))
                        ])
                qty_total = 0
                for quant in quants:
                    qty_total += quant.qty
                if self.qty > qty_total:
                    self.qty = 0
                    message = "No tiene stock de este lote"
                    res['warning'] = {'title': _('Warning'), 'message': message}
        return res

