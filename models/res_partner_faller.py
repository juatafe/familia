from odoo import models, fields

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
