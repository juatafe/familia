from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class PortalFamily(http.Controller):

    @http.route('/familia/update_member', type='json', auth='user')
    def update_member(self, member_id, values):
        miembro = request.env['familia.miembro'].sudo().browse(int(member_id))
        if not miembro.exists():
            return {'error': 'El membre no existeix'}

        try:
            miembro.check_family_admin()
        except AccessError as e:
            return {'error': str(e)}

        allowed = {'tiene_limite', 'limite_gasto', 'saldo_anual', 'es_administrador'}
        vals_to_write = {k: v for k, v in values.items() if k in allowed}
        if vals_to_write:
            miembro.sudo().write(vals_to_write)
        return {'success': True}

    # 🔹 Formulari per editar dades personals d’un membre
    @http.route('/familia/manage_member/<int:partner_id>', type='http', auth='user', website=True)
    def manage_member(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return request.not_found()

        miembro = request.env['familia.miembro'].sudo().search([('partner_id', '=', partner_id)], limit=1)
        if not miembro:
            return request.not_found()

        # Validar que l’usuari actual és admin de la família
        current = request.env['familia.miembro'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('familia_id', '=', miembro.familia_id.id)
        ], limit=1)
        if not current or not current.es_administrador:
            raise AccessError("No tens permisos per editar aquest membre.")

        values = {
            'page_name': 'manage_member',
            'partner': partner,
        }
        return request.render('familia.portal_manage_member', values)

    # 🔹 Guardar canvis del formulari
    @http.route('/familia/save_member', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def save_member(self, partner_id=None, **post):
        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return request.not_found()

        miembro = request.env['familia.miembro'].sudo().search([('partner_id', '=', partner.id)], limit=1)
        if not miembro:
            return request.not_found()

        current = request.env['familia.miembro'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('familia_id', '=', miembro.familia_id.id)
        ], limit=1)
        if not current or not current.es_administrador:
            raise AccessError("No tens permisos per editar aquest membre.")

        vals = {}
        for field in ['name', 'email', 'phone', 'mobile', 'street', 'city', 'zip']:
            if field in post:
                vals[field] = post[field]

        if vals:
            partner.sudo().write(vals)

        return request.redirect('/my')
