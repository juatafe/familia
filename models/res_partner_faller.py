from odoo import models, fields

class ResPartnerFaller(models.Model):
    _inherit = 'res.partner'

    codifaller = fields.Integer(string='Codi Faller')
    dni = fields.Char(string='DNI')
    nom_faller = fields.Char(string='Nom')  # Alternativa si vols separar
    cognoms_faller = fields.Char(string='Cognoms')
    street = fields.Char(string='Adreça')  # Ja existeix en res.partner
    city = fields.Char(string='Població')  # Ja existeix en res.partner
    zip = fields.Char(string='Codi Postal')  # Ja existeix en res.partner
    provincia = fields.Char(string='Província')
    telefon = fields.Char(string='Telèfon fix')
    telefon_mobil = fields.Char(string='Telèfon mòbil')
    email = fields.Char(string='Correu electrònic')  # Ja existeix en res.partner

    data_naixement = fields.Date(string='Data de Naixement')
    sexe = fields.Selection([
        ('home', 'Home'),
        ('dona', 'Dona'),
    ], string='Home/Dona')

    codi_postal_personalitzat = fields.Char(string='CodiP')  # Si diferent de zip
    alta = fields.Boolean(string='Alta activa?')
    data_alta = fields.Date(string='Data d\'Alta')
    data_baixa = fields.Date(string='Data de Baixa')
    numero_familia = fields.Char(string='Nº Família')  # Textual, si no és ID relacionat

    es_regina_major = fields.Boolean(string='Regina Major')
    fallera_major_infantil = fields.Boolean(string='Fallera Major Infantil')
    regina_infantil = fields.Boolean(string='Regina Infantil')
    regina_o_major = fields.Boolean(string='Regina/o Major')
    regina_o_infantil = fields.Boolean(string='Regina/o Infantil')

    baremacio = fields.Boolean(string='Baremat')
    comentari = fields.Text(string='Comentari')
    antiguitat_previa = fields.Integer(string='Antiguitat Prèvia')
    n_comissions = fields.Integer(string='Nombre de Comissions')
