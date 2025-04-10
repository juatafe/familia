from odoo import models, fields, api

class Familia(models.Model):
    _name = 'familia.familia'
    _description = 'Familia'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # 👈 Afegim el chatter


    name = fields.Char(string='Nombre', required=True)
    numero_familia = fields.Char(string='Nº Familia', required=False, index=True)
    saldo_total = fields.Float(string='Saldo Total', readonly=True)
    miembros_ids = fields.One2many('familia.miembro', 'familia_id', string="Miembros")

    _sql_constraints = [
        ('numero_familia_unique', 'unique(numero_familia)', 'El número de familia debe ser único.')
    ]

