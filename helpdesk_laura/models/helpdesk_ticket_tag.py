from odoo import  fields, models

class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Helpdesk Ticket Tag'

  
    #Crear un nuevo modelo etiquetas, con titulo.
    name = fields.Char(
        required=True,
        string='Title',
    )
        