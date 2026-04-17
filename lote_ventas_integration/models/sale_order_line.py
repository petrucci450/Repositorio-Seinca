from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Agregamos el dominio directamente aquí.
    # Esto le dice a Odoo: "Muestra solo los stock.lot cuyo product_id sea igual al product_id de esta línea"
    lot_id = fields.Many2one(
        'stock.lot',
        string='Lote',
        domain="[('product_id', '=', product_id)]"
    )

    @api.onchange('product_id')
    def _onchange_product_id_clear_lot(self):
        # El onchange ahora solo lo usamos para limpiar el lote si el usuario cambia el producto
        # a mitad de camino, para evitar inconsistencias.
        for line in self:
            if line.lot_id and line.lot_id.product_id != line.product_id:
                line.lot_id = False

    def _prepare_procurement_values(self):
        vals = super()._prepare_procurement_values()
        # Propagar el ID del lote
        if self.lot_id:
            vals['sale_line_lot_id'] = self.lot_id.id
        return vals