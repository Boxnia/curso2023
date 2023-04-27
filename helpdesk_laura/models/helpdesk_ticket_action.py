from odoo import  fields, models

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Helpdesk Ticket Action'

  
    #Crear un nuevo modelo acciones, con titulo y estado ( todo o done).
    name = fields.Char(
        required=True,
        string='Title'
    )
    
    state = fields.Selection(
        selection=[
            ('todo', 'To do'),
            ('done', 'Done')
        ],
        default='todo',
    )
    
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket'
    )
    
    def set_done(self):
        self.write({'state': 'done'})
    
    def set_todo(self):
        self.write({'state': 'todo'})