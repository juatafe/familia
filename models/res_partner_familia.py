from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartnerFamilia(models.Model):
    _inherit = 'res.partner'

    saldo_a_favor = fields.Float(string='Saldo a Favor', store=True, readonly=False)

    def write(self, vals):
        # Evitem processar si venim d'un unlink amb context
        if self.env.context.get('skip_saldo'):
            return super().write(vals)

        if 'saldo_a_favor' in vals:
            for partner in self:
                nou_valor = vals['saldo_a_favor']
                diferencia = nou_valor - partner.saldo_a_favor

                miembro = self.env['familia.miembro'].search([('partner_id', '=', partner.id)], limit=1)
                if miembro and miembro.familia_id:
                    familia = miembro.familia_id
                    nou_total = familia.saldo_total + diferencia
                    familia.sudo().write({'saldo_total': nou_total})
                    _logger.info(f"{partner.name} ha ingressat {diferencia} €. Nou saldo familiar: {nou_total}")
                else:
                    _logger.info(f"Ignorat canvi de saldo de {partner.name} perquè ja no té família.")

        return super().write(vals)


# from odoo import models, fields, api

# class ResPartnerFamilia(models.Model):
#     _inherit = 'res.partner'

#     saldo_a_favor = fields.Float(string='Saldo a Favor', compute='_compute_saldo_a_favor', store=False)

#     def _compute_saldo_a_favor(self):
#         for partner in self:
#             miembro = self.env['familia.miembro'].search([('partner_id', '=', partner.id)], limit=1)
#             if miembro and miembro.familia_id:
#                 # Si es miembro de una familia, su saldo a favor es el saldo total de la familia
#                 partner.saldo_a_favor = miembro.familia_id.saldo_total
#             else:
#                 # Si no es miembro de una familia, el saldo es cero
#                 partner.saldo_a_favor = 0.0

#     def write(self, vals):
#         if 'saldo_a_favor' in vals:
#             for partner in self:
#                 miembro = self.env['familia.miembro'].search([('partner_id', '=', partner.id)], limit=1)
#                 if miembro and miembro.familia_id:
#                     familia = miembro.familia_id
#                     diferencia = partner.saldo_a_favor - vals['saldo_a_favor']
#                     # Disminuir el saldo total de la familia en la misma medida que el saldo personal del miembro
#                     familia.saldo_total -= diferencia

#         return super(ResPartnerFamilia, self).write(vals)
