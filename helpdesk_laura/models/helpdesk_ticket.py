from odoo import  fields, models

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'

    #Nombre
    name = fields.Char(
        required=True,
        help="Resume en pocas palabras un título para la incidencia",
        index=True
    )
    #Descripcion
    description = fields.Text(
        help="Escribe detalladamente la incidencia y como replicarla.",
        default="""Version a la que afecta:
    Modulo:
    Pasos para replicar:
    Modulos personalizados:
        """
    )
    #Fecha
    date = fields.Date()    
    #Fecha y hora limite
    date_limit = fields.Datetime(
        string='Limi Date & Time')    
    #Asignado (Verdadero o Falso) solo lectura
    assigned = fields.Boolean(
        readonly=True,
    )
    #Acciones a realizar (Html)

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assidned to')
    
    # Añadir el campo Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('assigned', 'Assigned'),
            ('in_process', 'In Process'),
            ('pending', 'Pending'),
            ('resolved', 'Resolved'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )

    #Añádir campo sequence y hacer el widget handle.
    sequence = fields.Integer(
        default=10,
        help="Secuencia para el orden de las incidencias",
    )


    actions_todo = fields.Html()