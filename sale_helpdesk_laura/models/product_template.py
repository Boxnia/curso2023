from odoo import fields, models, api, Command, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    helpdesk_tag_id = fields.Many2one('helpdesk.ticket.tag', string='Helpdesk Tag')