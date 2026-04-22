from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        # Si la línea de venta tiene varios lotes seleccionados, crear una move line por cada lote
        if self.sale_line_id and self.sale_line_id.lot_ids:
            lot_ids = self.sale_line_id.lot_ids
            total_qty = self.product_uom_qty
            qty_per_lot = total_qty / len(lot_ids) if lot_ids else total_qty
            move_lines = []
            for lot in lot_ids:
                move_line_vals = vals.copy()
                move_line_vals['lot_id'] = lot.id
                move_line_vals['qty_done'] = qty_per_lot
                move_lines.append(move_line_vals)
            return move_lines
        return vals