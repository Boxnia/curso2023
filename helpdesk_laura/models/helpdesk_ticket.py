from odoo import fields, models, api, Command, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    # Nombre
    name = fields.Char(
        required=True,
        help="Resume en pocas palabras un título para la incidencia",
        index=True,
    )
    # Descripcion
    description = fields.Text(
        help="Escribe detalladamente la incidencia y como replicarla.",
        default="""Version a la que afecta:
    Modulo:
    Pasos para replicar:
    Modulos personalizados:
        """,
    )
    # Fecha
    date = fields.Date()
    
    # añadir un onchange para que al indicar la fecha ponga como fehca de vencimiento un dia más
    @api.onchange("date")
    def _onchange_date(self):
        if self.date:
            self.date_limit = self.date + timedelta(days=1)
    
    # Fecha y hora limite
    date_limit = fields.Datetime(
            string="Limit Date & Time",
            #compute = "_compute_date_limit",
            #inverse = "_inverse_date_limit",
            #store = True
        )

    """  def _compute_date_limit(self):
        for record in self:
            if self.date:
                self.date_limit = self.date + timedelta(days=1)
            else:
                self.date_limit = False
    
    def _inverse_date_limit(self):
        pass """
    # Asignado (Verdadero o Falso) solo lectura
    assigned = fields.Boolean(
        readonly=True,
    )
    # Acciones a realizar (Html)

    user_id = fields.Many2one(comodel_name="res.users", string="Assidned to")

    # Añadir el campo Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("assigned", "Assigned"),
            ("in_process", "In Process"),
            ("pending", "Pending"),
            ("resolved", "Resolved"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )

    # Añádir campo sequence y hacer el widget handle.
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

    # Crear en el ticket un campo o2m apuntando a las acciones.
    # cada record tiene sus acciones, no se comparten con los demas
    action_ids = fields.One2many(
        comodel_name="helpdesk.ticket.action",
        inverse_name="ticket_id",
        string="Actions",
    )

    #funciona añada una accion
    """  def add_function(self):
        self.ensure_one()
        self.write(
            {
                'action_ids': [
                    (0, 0, {"name": "ACTION"}),
                ]
            }
        ) """
        
    # Crear en el ticket un campo m2m apuntando a las etiquetas.
    # estos campos no son necesarios
    # comparte campos entre records
    tag_ids = fields.Many2many(
        comodel_name="helpdesk.ticket.tag",
        relation='helpdesk_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        string="Tags",
    )

    color = fields.Integer("Color Index", default=0)
    amount_time = fields.Float(string="Amount of time")
    
    #añadir una restricción para hace que el campo amount_time no sea menor que 0
    @api.constrains("amount_time")
    def _check_amount_time(self):
        for record in self:
            if record.amount_time < 0:
                    raise ValidationError(_("The PIN must be a sequence of digits." ))
    
        
        
    person_id = fields.Many2one(
        "res.partner", domain=[("is_company", "=", False)], string="Person"
    )

    # api multi, se ejecuta sobre un conjunto de registros
    # clase api.one, se ejecuta sobre un registro
    # record -> objeto
    # recorsed -> conjunto de records
    # si no se dice nada se entiende que es api.multi
    def update_description(self):
        # self podría ser un objeto o varios
        # con el ensure te aseguras que self sea un objeto
        # self.ensure_one()
        # self.description = 'OK'
        # cuando es un recorset se hace un for
        # for record in self:
        #     record.name = 'OK'
        self.write({"name": "OK"})

    def update_all_description(self):
        # self.ensure_one()
        # self es un conjunto de registros
        # self.update({'description': 'OK'})
        all_tickets = self.env["helpdesk.ticket"].search([])
        all_tickets.update_description()
        # self.write({'description': 'OK'})

    def set_action_as_done(self):
        self.ensure_one()
        self.action_ids.set_done()

    # Hacer que el campo assigned sea calculado, hacer que se pueda buscar 
    # con el atributo search y hacer que se pueda modificar de forma que si lo 
    # marco se actualice el usuario con el usuario conectado y si lo desmarco se limpie el campo del usuario.
    
    # Asignado (Verdadero o Falso) solo lectura
    is_assigned = fields.Boolean(
        compute="_compute_assigned",
        search="_search_assigned",
        inverse="_inverse_assigned",
    )
    
    # si esiste un usuario entonces se marca el checkbox is assigned a true
    @api.depends("user_id")
    def _compute_assigned(self):
        for record in self:
            record.is_assigned = bool(record.user_id)

    #busca y los actuliza
    def _search_assigned(self, operator, value):
        #cuando es asignado es cuando es igual a true
        #cuando digo no asignado es cuando es igual a false
        if operator not in ("=", "!=") or not isinstance(value, bool):
            raise UserError("Operador no permitido")
        if operator == "=" and value == True:
            operator = "!="
        else:
            operator  = "="
        return [("user_id", operator, False)]

    #recalcular, en este caso lo que hace que cuando desckeamo el checkbox asignado se quita el usuario (esto a nivel de frontend)
    def _inverse_assigned(self):
        for record in self:
            if not record.is_assigned:
                record.user_id = False
            else:
                record.user_id = self.env.user

    
    user_name = fields.Char(
        related="user_id.name",
        string="User Name",
        readonly=True,
    )
    
    # hacer un campo calculado que indique, dentro de un ticket, la cantidad de tiquets asociados al mismo ususario.
    tickets_count = fields.Integer(
        compute="_compute_tickets_count",
        string="Tickets Count",
    )
    # crear un campo nombre de etiqueta, y hacer un botón que cree la nueva etiqueta con ese nombre y lo asocie al ticket.
    @api.depends("user_id")
    def _compute_tickets_count(self):
        ticket_obj = self.env["helpdesk.ticket"]
        for record in self:
            tickets =  ticket_obj.search(
                [("user_id", "=", record.user_id.id)]
            )
            record.tickets_count = len(tickets)
    
    tag_name = fields.Char()
    
    #comman es igual que poner lo de las tuplas
    def create_tag(self):
        self.ensure_one()
        # self.write({'tag_ids': [(0,0,{'name': self.tag_name})]})
        # self.write({'tag_ids': [Command.create({'name': self.tag_name})]})
        self.tag_ids = [Command.create({'name': self.tag_name})]
    #import pdb; pdb.set_trace()   
    def clear_tag(self):
        self.ensure_one()
        tag_ids = self.env['helpdesk.ticket.tag'].search([('name', '=', 'otra')])
        # self.write({'tag_ids': [
        #     (5,0,0),
        #     (6,0,tag_ids.ids)]})
        self.tag_ids = [
            Command.clear(),
            Command.set(tag_ids.ids)]
    
    def get_related_action(self):
        self.ensure_one()
        #devolver la accion que abre la ventana con un dominio para mostrar solo los que son mios
        #buscar accion y devolverla
        action = self.env["ir.actions.actions"]._for_xml_id("helpdesk_laura.helpdesk_ticket_action_action")
        action['domain'] = [('ticket_id', '=', self.id)]
        action['context'] = {'default_ticket_id': self.id}
        return action
        
        
          
    """       def _get_action_view_picking(self, pickings):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''

        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action """