from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_ids = fields.Many2many(
        'stock.lot',
        'sale_order_line_stock_lot_rel',
        'sale_line_id',
        'lot_id',
        string='Lotes',
        domain="[('product_id', '=', product_id)]"
    )
    lot_id = fields.Many2one(
        'stock.lot',
        string='Lote principal',
        domain="[('product_id', '=', product_id)]"
    )

    @api.onchange('product_id')
    def _onchange_product_id_clear_lot(self):
        for line in self:
            if line.lot_ids:
                line.lot_ids = line.lot_ids.filtered(lambda lot: lot.product_id == line.product_id)
            if line.lot_id and line.lot_id.product_id != line.product_id:
                line.lot_id = False
            if line.lot_id and line.lot_id not in line.lot_ids:
                line.lot_ids |= line.lot_id

    @api.onchange('lot_ids')
    def _onchange_lot_ids_sync_principal_lot(self):
        for line in self:
            if not line.lot_ids:
                line.lot_id = False
                continue
            if line.lot_id not in line.lot_ids:
                line.lot_id = line.lot_ids[:1]

    def _prepare_procurement_values(self, **kwargs):
        vals = super()._prepare_procurement_values(**kwargs)

        if self.lot_ids:
            vals['sale_line_lot_ids'] = self.lot_ids.ids
        if self.lot_id:
            vals['sale_line_lot_id'] = self.lot_id.id

        return vals