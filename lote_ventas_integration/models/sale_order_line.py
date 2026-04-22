from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._normalize_lot_vals(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        vals = self._normalize_lot_vals(vals)
        return super().write(vals)

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

    def _normalize_lot_vals(self, vals):
        vals = dict(vals)

        if 'lot_id' in vals and vals['lot_id']:
            if 'lot_ids' not in vals:
                vals['lot_ids'] = [(4, vals['lot_id'])]

        if 'lot_ids' in vals and 'lot_id' not in vals:
            lot_commands = vals.get('lot_ids') or []
            selected_lot_ids = self._extract_lot_ids_from_commands(lot_commands)
            vals['lot_id'] = selected_lot_ids[0] if selected_lot_ids else False

        if 'lot_id' in vals and not vals['lot_id'] and 'lot_ids' not in vals:
            vals['lot_ids'] = [(5, 0, 0)]

        return vals

    def _extract_lot_ids_from_commands(self, commands):
        lot_ids = []
        for command in commands:
            if not isinstance(command, (list, tuple)) or not command:
                continue
            operation = command[0]
            if operation == 6:
                return list(command[2] or [])
            if operation == 4 and command[1]:
                lot_ids.append(command[1])
            if operation == 5:
                return []
        return lot_ids