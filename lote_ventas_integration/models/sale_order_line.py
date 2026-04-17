from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # CORRECCIÓN: El modelo correcto en Odoo 17 es 'stock.lot'
    lot_id = fields.Many2one(
        'stock.lot',
        string='Lote'
    )

    @api.onchange('product_id')
    def _onchange_product_id_set_lot_domain(self):
        if len(self) != 1:
            return
            
        if not self.product_id:
            self.lot_id = False
            return {'domain': {'lot_id': [('id', 'in', [])]}}

        # Buscar lotes asociados a quants del producto con stock positivo
        quants = self.env['stock.quant'].search([
            ('product_id', '=', self.product_id.id),
            ('quantity', '>', 0),
        ])
        
        lot_ids = quants.mapped('lot_id').ids

        # Si el lote actual no está en los lotes disponibles, lo vaciamos
        if self.lot_id and self.lot_id.id not in lot_ids:
            self.lot_id = False

        return {'domain': {'lot_id': [('id', 'in', lot_ids)]}}

    def _prepare_procurement_values(self):
        vals = super()._prepare_procurement_values()
        # Esto asegura que el ID viaje en los valores de reabastecimiento (opcional pero buena práctica)
        if self.lot_id:
            vals['sale_line_lot_id'] = self.lot_id.id
        return vals