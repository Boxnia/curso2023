from odoo import fields, models


# models.Model es parte del ORM
class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    # si no se pone description (warning)
    _description = "Helpdesk ticket"

    # Nombre
    name = fields.Char(required=True)
    sequence = fields.Integer(
        string="Secuencia",
    )

    # Descrición
    description = fields.Text(
        help="Escribe detallamente la incidencia",
        default="""Versión a la que afecta:
    Módulo:
    Pasos para replicar:
    Módulos personalizados:
    """,
    )

    # Fecha
    date = fields.Date()

    # Fecha y hora límite
    date_limit = fields.Datetime(string="Limit Date & Time")

    # Asignado (Verdadero o falso)
    # El campo Asignado hacer que sea solo de lectura

    assigned = fields.Boolean(readonly=True)

    user_id = fields.Many2one(string="Assigned to", comodel_name="res.users")

    # Acciones a realizar (Html)
    actions_todo = fields.Html(
        string="Actions to do",
    )

    # Añadir el campo Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo
    # El campo nombre que sea obligatorio
    # En algún campo añadir un texto de ayuda indicando su funcionalidad, luego revisar que funciona.
    state = fields.Selection(
        [
            ("new", "New"),
            ("Assigned", "Assigned"),
            ("in_progress", "In progress"),
            ("pending", "Pending"),
            ("resolved", "Resolved"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        help="El estado de la entidad",
    )