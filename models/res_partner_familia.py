from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartnerFamilia(models.Model):
    _inherit = 'res.partner'

    saldo_a_favor = fields.Float(string='Saldo a Favor', store=True, readonly=False)

    def write(self, vals):
        # ✂️ Evita recursivitat infinita
        if self.env.context.get('skip_saldo') or self.env.context.get('avoid_propagation') or self.env.context.get('from_familia_sync'):
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

                    # 🛡️ Prevenim recursió infinita
                    familia.with_context(avoid_propagation=True).sudo().actualitzar_saldo_membres()
                else:
                    _logger.info(f"Ignorat canvi de saldo de {partner.name} perquè ja no té família.")

        return super().write(vals)
