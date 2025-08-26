# familia/hooks.py
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

LANGS = ["ca", "ca_ES", "ca_ES@valencia"]
REPLACEMENTS = [
    ("Pressupostos", "Reserves"),
    ("Pressuposts", "Reserves"),
    ("Els meus pressupostos", "Les meues reserves"),
    ("Pressupost #", "Reserva #"),
    ("Data de pressupost", "Data de reserva"),
    ("Pressupost", "Reserva"),
]

def _force_view_tr(env, xmlid, src, dst):
    name = f"model_terms:ir.ui.view,arch_db:{xmlid}"
    T = env["ir.translation"]
    for lang in LANGS:
        rec = T.search([("lang", "=", lang), ("name", "=", name), ("src", "=", src)], limit=1)
        if rec:
            if rec.value != dst:
                _logger.info(f"[familia] Update tr: {lang} {xmlid} :: {src!r} -> {dst!r}")
                rec.write({"value": dst, "state": "translated"})
        else:
            _logger.info(f"[familia] Create tr: {lang} {xmlid} :: {src!r} -> {dst!r}")
            T.create({
                "name": name, "lang": lang, "src": src, "type": "model_terms",
                "value": dst, "state": "translated",
            })

def _replace_any_pressupost(env):
    T = env["ir.translation"]
    total = 0
    for lang in LANGS:
        rows = T.search([("lang", "=", lang), ("value", "ilike", "%Pressupost%")])
        _logger.info(f"[familia] {len(rows)} traduccions trobades amb 'Pressupost' (lang={lang})")
        for tr in rows:
            v = tr.value or ""
            v2 = v
            for src, dst in REPLACEMENTS:
                v2 = v2.replace(src, dst)
            if v2 != v:
                tr.write({"value": v2, "state": "translated"})
                total += 1
                _logger.info(f"[familia] {lang} {tr.name}: {v!r} -> {v2!r}")
    return total

def apply_translation_fixes_env(env):
    """Crida açò des del shell amb l'`env` existent."""
    _logger.info("[familia] Inici apply_translation_fixes_env()")
    n = _replace_any_pressupost(env)
    _force_view_tr(env, "sale.portal_my_orders", "Quotations", "Reserves")
    _force_view_tr(env, "sale.portal_my_orders", "Quotation #", "Reserva #")
    _force_view_tr(env, "sale.portal_my_orders", "Quotation Date", "Data de reserva")
    _force_view_tr(env, "sale.portal_my_orders", "Order #", "Reserva #")
    _force_view_tr(env, "sale.portal_my_orders", "Order Date", "Data de reserva")
    _force_view_tr(env, "sale.portal_my_home",   "Quotations", "Reserves")
    _force_view_tr(env, "sale.portal_my_orders", "My Quotations", "Les meues reserves")
    # neteja cau
    env["ir.http"].clear_caches()
    env["ir.qweb"]._clear_caches()
    for w in env["website"].search([]):
        try:
            w.clear_caches()
        except Exception as e:
            _logger.warning(f"[familia] Error netejant cache website {w.id}: {e}")
    _logger.info(f"[familia] Fi apply_translation_fixes_env(). Canvis: {n}")
    return n

def post_init_hook(cr, registry):
    """Per a install/upgrade real del mòdul."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    apply_translation_fixes_env(env)
