from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartnerFaller(models.Model):
    _inherit = 'res.partner'

    codifaller = fields.Integer(string='CodFaller')  # Coincideix amb l'Excel
    vat = fields.Char(string='DNI')  # Perquè el camp fiscal reconega 'DNI'
    nom_faller = fields.Char(string='Nombre')
    cognoms_faller = fields.Char(string='Apellidos')
    street = fields.Char(string='Direccion')  # Ja existeix, però sobreescrivim l'etiqueta
    city = fields.Char(string='Poblacion')
    zip = fields.Char(string='CP')
    provincia = fields.Char(string='Provincia')
    phone = fields.Char(string='Telefono')  # Etiqueta Excel per telèfon fix
    mobile = fields.Char(string='TMovil')   # Etiqueta Excel per mòbil
    email = fields.Char(string='MAIL')

    data_naixement = fields.Date(string='FechaNacimiento')
    sexe = fields.Selection([
        ('home', 'Home'),
        ('dona', 'Dona'),
    ], string='HomeDona')

    codi_postal_personalitzat = fields.Char(string='CodiP')
    alta = fields.Boolean(string='Alta')
    data_alta = fields.Date(string='FechaAlta')
    data_baixa = fields.Date(string='FechaBaja')
    numero_familia = fields.Char(string='NºFamilia')

    es_regina_major = fields.Boolean(string='Regina Major')
    fallera_major_infantil = fields.Boolean(string='Fallera Major Infantil')
    regina_infantil = fields.Boolean(string='Regina Infantil')
    regina_o_major = fields.Boolean(string='Regina/o Major')
    regina_o_infantil = fields.Boolean(string='Regina/o Infantil')

    baremacio = fields.Boolean(string='Baremacio')
    comentari = fields.Text(string='Comentari')
    antiguitat_previa = fields.Integer(string='AntiguitatPrevia')
    n_comissions = fields.Integer(string='NComissions')

    @api.model
    def crear_membres_familia_des_de_numero(self):
        for partner in self.search([('numero_familia', '!=', False)]):
            # Buscar o crear la família corresponent
            familia = self.env['familia.familia'].search([
                ('numero_familia', '=', partner.numero_familia)
            ], limit=1)

            if not familia:
                familia = self.env['familia.familia'].create({
                    'name': f"Família {partner.numero_familia}",
                    'numero_familia': partner.numero_familia,
                })
                _logger.info(f"Creada família {familia.name} amb número {familia.numero_familia}")

            # Verificar que no estiga ja associat
            existeix = self.env['familia.miembro'].search([
                ('partner_id', '=', partner.id)
            ])
            if not existeix:
                self.env['familia.miembro'].create({
                    'partner_id': partner.id,
                    'familia_id': familia.id,
                })
                _logger.info(f"Afegit {partner.name} a la família {familia.numero_familia}")
