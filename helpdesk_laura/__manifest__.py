# Copyright <2023> Javier Parra - jparra@ontinet.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Javier Parra",
    "summary": "Gestiona incidencias de helpdesk",
    "version": "16.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "category": "Helpdesk",
    "website": "https://ontinet.com",
    "author": "ONTINET, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/helpdesk_ticket_views.xml"
    ],
}