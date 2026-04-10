from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat', 'country_id')
    def check_vat(self):
        # Al sobreescribir el método nativo y colocar 'pass', 
        # neutralizamos la validación matemática del RIF/NIF.
        # Odoo aceptará lo que el usuario escriba en el campo 'vat'.
        pass

    # Opcional: Si el error proviene específicamente de la localización venezolana
    # que usa un chequeo independiente, también anulamos ese submétodo:
    def check_vat_ve(self, vat):
        return True