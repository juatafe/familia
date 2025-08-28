odoo.define('familia.portal_family', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    console.log("✅ portal_family.js carregat!");

    publicWidget.registry.PortalFamilyDropdown = publicWidget.Widget.extend({
        selector: '#select-familiar',

        start: function () {
            console.log("👉 Widget PortalFamilyDropdown inicialitzat");
            return this._super.apply(this, arguments);
        },

        events: {
            'change': '_onChangeFamiliar',
        },

        _onChangeFamiliar: function (ev) {
            console.log("🔄 Canvi detectat al desplegable de familiars");

            const select = ev.currentTarget;
            const selected = select.options[select.selectedIndex];
            const infoBox = document.getElementById('info-familiar');

            if (!infoBox) {
                console.warn("⚠️ No s'ha trobat el div #info-familiar");
                return;
            }

            const name = selected.textContent.trim();
            const email = selected.dataset.email || '-';
            const phone = selected.dataset.phone || '-';
            const saldo = selected.dataset.saldo || '0';

            console.log(`📌 Familiar seleccionat: ${name}, Email: ${email}, Telèfon: ${phone}, Saldo: ${saldo}`);

            infoBox.innerHTML = `
                <div class="card shadow-sm mt-2">
                    <div class="card-body">
                        <h5>${name}</h5>
                        <p>📧 ${email}</p>
                        <p>📞 ${phone}</p>
                        <p>💰 Saldo a favor: ${saldo} €</p>
                    </div>
                </div>`;
        },
    });
});
