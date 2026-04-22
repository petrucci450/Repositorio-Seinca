from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        # Obtenemos los valores estándar preparados por Odoo
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        
        # Si este movimiento de stock viene de una línea de venta y esa línea tiene un lote asignado
        if self.sale_line_id and self.sale_line_id.lot_id:
            # Asignamos el lote directamente a la línea de movimiento (stock.move.line)
            vals['lot_id'] = self.sale_line_id.lot_id.id
            
        return vals