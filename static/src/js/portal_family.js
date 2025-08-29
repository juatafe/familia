odoo.define('familia.portal_family', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const ajax = require('web.ajax');

    publicWidget.registry.PortalFamilyDropdown = publicWidget.Widget.extend({
        selector: '#select-familiar',

        events: {
            'change': '_onChangeFamiliar',
        },

        _onChangeFamiliar: function (ev) {
            const selected = ev.currentTarget.options[ev.currentTarget.selectedIndex];
            const detailsBox = document.getElementById('info-familiar');
            const infoBox = document.getElementById('info-familiar-body');

            if (!selected.value) {
                if (detailsBox) detailsBox.classList.add("d-none");
                return;
            }

            if (detailsBox) detailsBox.classList.remove("d-none");
            if (!infoBox) return;

            const id = selected.value;
            const name = selected.dataset.name;
            const limit = selected.dataset.limit === "true";
            const limitAmount = selected.dataset.limitAmount;
            const memberAdmin = (selected.dataset.memberAdmin || '').toLowerCase() === "true";
            const currentAdmin = (selected.dataset.currentAdmin || '').toLowerCase() === "true";
            const familiaSaldo = selected.dataset.familiaSaldo;
            const saldoAnual = parseFloat(selected.dataset.saldoAnual || 0);
            const editUrl = selected.dataset.editUrl;

            // 👉 Si NO és admin → només info
            if (!currentAdmin) {
                infoBox.innerHTML = `
                    <h5>${name}</h5>
                    <p>🏦 Saldo familiar actual: ${familiaSaldo} €</p>
                    ${saldoAnual > 0 ? `<p>📆 Límit anual: ${saldoAnual} €</p>` : ""}
                    ${limit ? `<p>📊 Límit diari: ${limitAmount} €</p>` : ""}
                `;
                return;
            }

            // 👉 Si ÉS admin → formulari editable
            infoBox.innerHTML = `
                <h5>${name}</h5>
                
                <!-- Límit diari -->
                <div class="form-check mb-2">
                  <input type="checkbox" class="form-check-input" id="chk-limit" ${limit ? 'checked' : ''}/>
                  <label class="form-check-label" for="chk-limit">Té límit diari</label>
                </div>
                <div class="input-group input-euro mb-2" style="max-width: 150px;">
                  <input type="number" id="txt-limit-amount" class="form-control form-control-sm" 
                         value="${limitAmount}" ${limit ? '' : 'disabled'} />
                  <span class="input-group-text">€</span>
                </div>

                <!-- Límit anual -->
                <div class="form-check mb-2">
                  <input type="checkbox" class="form-check-input" id="chk-saldo-anual" ${saldoAnual > 0 ? 'checked' : ''}/>
                  <label class="form-check-label" for="chk-saldo-anual">Té límit anual</label>
                </div>
                <div class="input-group input-euro mb-2" style="max-width: 150px;">
                  <input type="number" id="txt-saldo-anual" class="form-control form-control-sm" 
                         value="${saldoAnual}" ${saldoAnual > 0 ? '' : 'disabled'} />
                  <span class="input-group-text">€</span>
                </div>

                <!-- Admin -->
                <div class="form-check mb-2">
                  <input type="checkbox" class="form-check-input" id="chk-admin" ${memberAdmin ? 'checked' : ''}/>
                  <label class="form-check-label" for="chk-admin">Administrador</label>
                </div>

                <button class="btn btn-primary btn-sm mt-2" id="btn-save-member">💾 Desa</button>
                <hr/>
                <a href="${editUrl}" class="btn btn-secondary btn-sm">
                    ✏️ Modificar dades personals
                </a>
            `;

            // habilitar/deshabilitar límit diari
            const chkLimit = document.getElementById('chk-limit');
            const txtLimit = document.getElementById('txt-limit-amount');
            chkLimit.addEventListener('change', function() {
                txtLimit.disabled = !chkLimit.checked;
            });

            // habilitar/deshabilitar límit anual
            const chkAnual = document.getElementById('chk-saldo-anual');
            const txtAnual = document.getElementById('txt-saldo-anual');
            chkAnual.addEventListener('change', function() {
                txtAnual.disabled = !chkAnual.checked;
            });

            // botó desa → RPC
            document.getElementById('btn-save-member').addEventListener('click', function () {
                const values = {
                    tiene_limite: chkLimit.checked,
                    limite_gasto: parseFloat(txtLimit.value) || 0,
                    es_administrador: document.getElementById('chk-admin').checked,
                    saldo_anual: chkAnual.checked ? (parseFloat(txtAnual.value) || 0) : 0,
                };

                ajax.jsonRpc('/familia/update_member', 'call', {
                    member_id: id,
                    values: values
                }).then(result => {
                    if (result.success) {
                        alert("✅ Canvis guardats correctament!");
                    } else {
                        alert("⚠️ Error: " + result.error);
                    }
                });
            });
        },
    });
});
