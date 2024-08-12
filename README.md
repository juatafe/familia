# Módulo de Odoo: Gestión de Familias

<p align="center">
  <img src="static/description/icon.png" alt="Icono del Módulo">
</p>

## Descripción

El módulo **Familia** para Odoo 16, desarrollado por **JB Talens**, permite gestionar clientes como unidades familiares, facilitando la administración de sus saldos y relaciones. Este módulo es ideal para negocios que manejan grupos de clientes como familias y requieren un control centralizado de los saldos familiares.

### Características principales

- **Gestión de Familias**: Agrupa a varios clientes como miembros de una familia, permitiendo la gestión conjunta de sus saldos.
- **Control de Saldo Total**: El saldo total de la familia se gestiona automáticamente, sumando el saldo de cada miembro al añadirse y ajustando el saldo al eliminar un miembro.
- **Restricciones de Membresía**: Un cliente solo puede pertenecer a una familia a la vez, garantizando la coherencia en la gestión de saldos.
- **Interfaz de Usuario Personalizada**: Incluye vistas y menús específicos para facilitar la gestión de familias y miembros dentro de Odoo.
- **Seguridad**: Configuración de seguridad específica para gestionar el acceso y los permisos dentro del módulo.

## Requisitos Previos

- **Odoo 16.0 o superior**
- **Módulos de CRM y Ventas**: Los módulos de CRM y ventas deben estar instalados.
- **Módulo saldo_favor**: Módulo personalizado para gestionar los saldos a favor de los clientes. Puedes encontrarlo en [saldo_favor](https://github.com/juatafe/saldo_favor).

## Instalación

Para instalar el módulo **Familia**, sigue estos pasos:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/juatafe/familia.git
