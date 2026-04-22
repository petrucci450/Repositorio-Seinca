from odoo import models
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_selected_sale_line_lots(self):
        self.ensure_one()
        if not self.sale_line_id:
            return self.env['stock.lot']
        return self.sale_line_id.lot_ids

    def _update_reserved_quantity(self, need, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
        self.ensure_one()

        selected_lots = self._get_selected_sale_line_lots()
        if lot_id or not selected_lots:
            return super()._update_reserved_quantity(need, location_id, lot_id, package_id, owner_id, strict)

        taken_quantity = 0
        lots_to_reserve = selected_lots
        if self.sale_line_id.lot_id and self.sale_line_id.lot_id in selected_lots:
            lots_to_reserve = self.sale_line_id.lot_id | (selected_lots - self.sale_line_id.lot_id)

        for selected_lot in lots_to_reserve:
            remaining_need = need - taken_quantity
            if float_compare(remaining_need, 0.0, precision_rounding=self.product_id.uom_id.rounding) <= 0:
                break
            taken_quantity += super()._update_reserved_quantity(
                remaining_need,
                location_id,
                lot_id=selected_lot,
                package_id=package_id,
                owner_id=owner_id,
                strict=True,
            )

        return taken_quantity

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