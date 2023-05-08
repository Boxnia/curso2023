from odoo import  fields, models, api

class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Helpdesk Ticket Tag'

  
    #Crear un nuevo modelo etiquetas, con titulo.
    name = fields.Char(
        required=True,
        string='Title',
    )
    
    tickets_ids = fields.Many2many(
        "helpdesk.ticket",
        "helpdesk_ticket_tag_rel",
        "tag_id",
        "ticket_id",
        "Tickets"
    )
    
    @api.model
    def _delete_tags_not_assigned(self):
        self.search([('tickets_ids', '=', False)]).unlink()
            