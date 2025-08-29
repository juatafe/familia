from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError
import logging

_logger = logging.getLogger(__name__)

class MiembroFamilia(models.Model):
    _name = 'familia.miembro'
    _description = 'Miembro de la Familia'

    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    familia_id = fields.Many2one('familia.familia', string='Familia', ondelete='cascade', required=True)
    saldo = fields.Float(string='Saldo', readonly=True, compute='_compute_saldo', store=True)
    tiene_limite = fields.Boolean(string='Tiene Límite de Gasto', default=False)
    limite_gasto = fields.Float(string='Límite de Gasto')
    es_administrador = fields.Boolean(string='Es Administrador')
    saldo_anual = fields.Float(
        string='Saldo Anual',
        help="Màxim de despesa anual per a aquest membre (0 = sense límit).",
        default=0.0
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def check_family_admin(self):
        """Comprova si l'usuari portal és administrador de la família"""
        partner = self.env.user.partner_id
        miembro = self.env['familia.miembro'].sudo().search([
            ('partner_id', '=', partner.id),
            ('familia_id', '=', self.familia_id.id),
        ], limit=1)
        if not (miembro and miembro.es_administrador):
            raise AccessError("No tens permisos per gestionar aquesta família.")
        return True

    @api.depends('familia_id.saldo_total')
    def _compute_saldo(self):
        for miembro in self:
            miembro.saldo = miembro.familia_id.saldo_total

    # ---------------------------------------------------------
    # Create / Write
    # ---------------------------------------------------------
    @api.model
    def create(self, vals):
        # 🔹 Si no hi ha límit anual marcat → posem saldo_anual = 0
        if 'saldo_anual' in vals and not vals['saldo_anual']:
            vals['saldo_anual'] = 0.0

        existing_member = self.env['familia.miembro'].search([
            ('partner_id', '=', vals.get('partner_id'))
        ])
        if existing_member:
            raise ValidationError(
                "Este miembro ya pertenece a una familia y no puede ser añadido a otra."
            )

        partner = self.env['res.partner'].browse(vals['partner_id'])
        saldo_miembro = partner.saldo_a_favor or 0.0
        familia = self.env['familia.familia'].browse(vals['familia_id'])

        if familia:
            if saldo_miembro > 0.0:
                nuevo_saldo_familia = familia.saldo_total + saldo_miembro
                familia.sudo().write({'saldo_total': nuevo_saldo_familia})
                _logger.info(
                    f"Transferit {saldo_miembro}€ de {partner.name} "
                    f"a la família {familia.name}. Nou saldo total: {nuevo_saldo_familia}"
                )
            else:
                nuevo_saldo_familia = familia.saldo_total

            partner.sudo().write({'saldo_a_favor': nuevo_saldo_familia})

        miembro = super().create(vals)

        # 🔁 Actualitzem saldo de tots els membres
        if familia:
            familia.sudo().actualitzar_saldo_membres()
            body = f"El membre <strong>{partner.name}</strong> s'ha unit a la família."
            if saldo_miembro > 0.0:
                body += f" Ha aportat {saldo_miembro:.2f} € al saldo familiar."
            familia.message_post(subject="Nou membre", body=body)

        # 🔐 Assignar grup si és administrador
        if vals.get('es_administrador'):
            user = miembro.partner_id.user_ids[:1]
            if user:
                group = self.env.ref('familia.group_family_admin')
                user.sudo().groups_id |= group

        return miembro

    def write(self, vals):
        # 🔹 Si es desmarca el límit anual → guardem com a 0
        if 'saldo_anual' in vals and not vals['saldo_anual']:
            vals['saldo_anual'] = 0.0

        res = super().write(vals)

        if 'es_administrador' in vals:
            group = self.env.ref('familia.group_family_admin')
            for miembro in self:
                user = miembro.partner_id.user_ids[:1]
                if user:
                    if vals['es_administrador']:
                        user.sudo().groups_id |= group
                    else:
                        user.sudo().groups_id -= group
        return res

    # ---------------------------------------------------------
    # Unlink
    # ---------------------------------------------------------
    def unlink(self):
        for miembro in self:
            cliente = miembro.partner_id
            familia = miembro.familia_id
            cliente.with_context(skip_saldo=True).sudo().write({'saldo_a_favor': 0.0})
            _logger.info(
                f"Saldo del client {cliente.name} posat a 0 després d'abandonar la família"
            )

            if familia:
                familia.message_post(
                    body=f"El membre <strong>{cliente.name}</strong> ha eixit de la família.",
                    subject="Baixa de membre"
                )

        return super().unlink()
