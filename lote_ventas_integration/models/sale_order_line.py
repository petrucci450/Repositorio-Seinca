from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_ids = fields.Many2many(
        'stock.lot',
        'sale_order_line_stock_lot_rel',
        'sale_order_line_id',
        'lot_id',
        string='Lotes',
        domain="[('product_id', '=', product_id)]"
    )

    @api.onchange('product_id')
    def _onchange_product_id_clear_lots(self):
        for line in self:
            if line.lot_ids:
                # Filtra los lotes que no corresponden al producto seleccionado
                line.lot_ids = line.lot_ids.filtered(lambda l: l.product_id == line.product_id)

    def _prepare_procurement_values(self, **kwargs):
        vals = super()._prepare_procurement_values(**kwargs)
        # Propaga los IDs de los lotes seleccionados
        if self.lot_ids:
            vals['sale_line_lot_ids'] = self.lot_ids.ids
        return vals