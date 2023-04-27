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
        string='Limit Date & Time')    
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
    
    # En el ticket añadir campo m2o apuntando al contacto (Asignado a).
    user_id = fields.Many2one(
        "res.users",
        string="Assigned to",
    )
    
    #Crear en el ticket un campo o2m apuntando a las acciones.
    #cada record tiene sus acciones, no se comparten con los demas
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions'
    )
    
    #Crear en el ticket un campo m2m apuntando a las etiquetas.
    #estos campos no son necesarios 
    #comparte campos entre records
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        # relation='helpdesk_ticket_tag_rel',
        # column1='ticket_id',
        # column2='tag_id',
        string='Tags')

        
    #api multi, se ejecuta sobre un conjunto de registros
    #clase api.one, se ejecuta sobre un registro
    #record -> objeto
    #recorsed -> conjunto de records
    #si no se dice nada se entiende que es api.multi
    def update_description(self):
        #self podría ser un objeto o varios
        # con el ensure te aseguras que self sea un objeto
        #self.ensure_one()
        #self.description = 'OK'
        #cuando es un recorset se hace un for
        # for record in self:
        #     record.name = 'OK'
        self.write({'name': 'OK'})

    def update_all_description(self):
        #self.ensure_one()
        #self es un conjunto de registros
        #self.update({'description': 'OK'})
        all_tickets = self.env['helpdesk.ticket'].search([])
        all_tickets.update_description()
        #self.write({'description': 'OK'})
        
        
    def set_action_as_done(self):
        self.ensure_one()
        self.action_ids.set_done()