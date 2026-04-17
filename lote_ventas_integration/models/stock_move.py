from odoo import models, api, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        # Si la creación viene ligada a una línea de venta que contiene lote,
        # adjuntamos un move_line inicial con ese lote para facilitar la recepción.
        sale_line = False
        if vals.get('sale_line_id'):
            try:
                sale_line = self.env['sale.order.line'].browse(vals.get('sale_line_id'))
            except Exception:
                sale_line = False

        move = super(StockMove, self).create(vals)

        if sale_line and sale_line.lot_id and not move.move_line_ids:
            try:
                move.write({
                    'move_line_ids': [(0, 0, {
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'product_uom_qty': move.product_uom_qty,
                        'qty_done': 0.0,
                        'lot_id': sale_line.lot_id.id,
                    })]
                })
            except Exception:
                # Silencioso: si la estructura difiere en la versión instalada, no rompemos la creación
                pass

        return move
