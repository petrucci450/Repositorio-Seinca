from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one(
        'stock.lot',
        string='Lote',
        domain="[('product_id', '=', product_id)]"
    )

    @api.onchange('product_id')
    def _onchange_product_id_clear_lot(self):
        for line in self:
            if line.lot_id and line.lot_id.product_id != line.product_id:
                line.lot_id = False

    # CORRECCIÓN AQUÍ: Agregamos **kwargs para aceptar group_id y cualquier otro parámetro
    def _prepare_procurement_values(self, **kwargs):
        # Pasamos los **kwargs a la función original
        vals = super()._prepare_procurement_values(**kwargs)
        
        # Propagamos el ID del lote
        if self.lot_id:
            vals['sale_line_lot_id'] = self.lot_id.id
            
        return vals