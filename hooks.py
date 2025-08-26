# familia/hooks.py
from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def _replace_any_pressupost_sql(cr, lang='ca'):
    # Canvis massius: Pressupost(s) -> Reserva(es)
    cr.execute("""
        UPDATE ir_translation
           SET value = regexp_replace(
                 regexp_replace(value, 'Pressupostos|Pressuposts', 'Reserves', 'gi'),
                 'Pressupost', 'Reserva', 'gi'
               )
         WHERE lang = %s
           AND value ILIKE %s
    """, (lang, '%Pressupost%'))
    return cr.rowcount

def _upsert_model_terms_sql(cr, xmlid, src, val, lang='ca'):
    # Necessitem el res_id (id de la vista) per a model_terms
    module, name = xmlid.split('.', 1)
    cr.execute("SELECT res_id FROM ir_model_data WHERE module=%s AND name=%s", (module, name))
    row = cr.fetchone()
    if not row:
        return 0
    res_id = row[0]
    name_key = f"model_terms:ir.ui.view,arch_db:{xmlid}"

    # Intenta UPDATE
    cr.execute("""
        UPDATE ir_translation
           SET value=%s, state='translated'
         WHERE lang=%s AND name=%s AND src=%s AND res_id=%s
         RETURNING id
    """, (val, lang, name_key, src, res_id))
    if cr.fetchone():
        return 1

    # Si no existeix, INSERT
    cr.execute("""
        INSERT INTO ir_translation (name, lang, type, src, value, state, res_id)
        VALUES (%s, %s, 'model_terms', %s, %s, 'translated', %s)
        ON CONFLICT DO NOTHING
    """, (name_key, lang, src, val, res_id))
    return 1

def post_init_hook(cr, registry):
    _logger.info("[familia] post_init_hook: aplicant correccions de traducció via SQL")

    # 1) Canvis genèrics Pressupost -> Reserva en ca
    _replace_any_pressupost_sql(cr, lang='ca')

    # 2) Forçar literals del portal (vistes de sale)
    fixes = [
        ('sale.portal_my_orders', 'Quotations',      'Reserves'),
        ('sale.portal_my_orders', 'Quotation #',     'Reserva #'),
        ('sale.portal_my_orders', 'Quotation Date',  'Data de reserva'),
        ('sale.portal_my_orders', 'My Quotations',   'Les meues reserves'),
        ('sale.portal_my_home',   'Quotations',      'Reserves'),
    ]
    for args in fixes:
        _upsert_model_terms_sql(cr, *args, lang='ca')

    # 3) No cal netejar caches ací: el servidor es reinicia en este punt
