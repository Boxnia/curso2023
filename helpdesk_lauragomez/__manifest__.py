# Copyright <YEAR(S)> Laura Gómez -  lmoreno@ontinet.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Laura Gómez",
    "summary": "Gestión de incidencias",
    "version": "16.0.1.0.0",
    "category": "Helpdesk",
    "website": "https://github.com/Boxnia/curso2023",
    "author": "lmoreno, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/helpdesk_ticket_views.xml"

    ]
}