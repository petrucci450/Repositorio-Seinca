from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)

        if not self.sale_line_id:
            return vals

        selected_lots = self.sale_line_id.lot_ids
        if reserved_quant and reserved_quant.lot_id and reserved_quant.lot_id in selected_lots:
            vals['lot_id'] = reserved_quant.lot_id.id
        elif len(selected_lots) == 1:
            vals['lot_id'] = selected_lots.id
        elif self.sale_line_id.lot_id:
            vals['lot_id'] = self.sale_line_id.lot_id.id
            
        return vals