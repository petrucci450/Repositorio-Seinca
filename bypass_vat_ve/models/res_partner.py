import re

from odoo import api, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat', 'country_id')
    def check_vat(self):
        for partner in self:
            vat = (partner.vat or '').strip().upper()

            if not vat:
                continue

            country_code = partner.country_id.code if partner.country_id else False

            if country_code and country_code != 'VE' and not re.match(r'^[VEJ]-?\d{7,8}(-\d)?$', vat):
                continue

            if re.match(r'^[VEJ]-?\d{7,8}$', vat):
                continue

            if re.match(r'^[VEJ]-?\d{8,9}-\d$', vat):
                continue

            raise ValidationError(
                'El número de identificación fiscal debe tener uno de estos formatos: '
                'V0000000, V-0000000, E0000000, E-0000000, J0000000, J-0000000, '
                'V00000000, V-00000000, E00000000, E-00000000, J00000000, J-00000000, '
                'V00000000-0, V-00000000-0, E00000000-0, E-00000000-0, '
                'J00000000-0 o J-00000000-0.'
            )