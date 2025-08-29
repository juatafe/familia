from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Familia(models.Model):
    _name = 'familia.familia'
    _description = 'Familia'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # 👈 Afegim el chatter


    name = fields.Char(string='Nombre', required=True)
    numero_familia = fields.Char(string='Nº Familia', required=False, index=True)
    saldo_total = fields.Float(string='Saldo Total', readonly=True)
    miembros_ids = fields.One2many('familia.miembro', 'familia_id', string="Miembros")
    #saldo_anual = fields.Float(string='Saldo Anual', readonly=False, help="Saldo total disponible a l'any per al familiar.")


    _sql_constraints = [
        ('numero_familia_unique', 'unique(numero_familia)', 'El número de familia debe ser único.')
    ]

    def actualitzar_saldo_membres(self):
        for familia in self:
            for membre in familia.miembros_ids:
                partner = membre.partner_id
                partner.sudo().with_context(from_familia_sync=True).write({'saldo_a_favor': familia.saldo_total})
                _logger.info(f"S'ha actualitzat el saldo de {partner.name} a {familia.saldo_total} €.")
