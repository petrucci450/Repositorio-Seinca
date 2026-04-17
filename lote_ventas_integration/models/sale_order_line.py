from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one(
        'stock.production.lot',
        string='Lote'
    )

    @api.onchange('product_id')
    def _onchange_product_id_set_lot_domain(self):
        if len(self) != 1:
            return
        line = self
        
        if not line.product_id:
            # 1. Asignamos directamente en lugar de usar 'value'
            line.lot_id = False
            return {
                'domain': {'lot_id': [('id', 'in', [])]},
            }

        # Buscar lotes asociados a quants del producto
        quants = self.env['stock.quant'].search([
            ('product_id', '=', line.product_id.id),
            ('quantity', '>', 0),
        ])
        lot_ids = quants.mapped('lot_id').filtered(lambda l: l).ids

        # 2. Asignamos directamente en lugar de armar un diccionario 'value'
        if line.lot_id and line.lot_id.id not in lot_ids:
            line.lot_id = False

        return {
            'domain': {'lot_id': [('id', 'in', lot_ids)]},
        }

    def _prepare_procurement_values(self):
        vals = super()._prepare_procurement_values()
        # Incluir lot seleccionado en los valores de procurement para que se propague
        if self.lot_id:
            vals.update({'lot_id': self.lot_id.id})
        return vals