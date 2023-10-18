# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    """Inherited sale.order  class to add helpdesk ticket id field,helpdesk
    ticket count and functions to compute ticket count and to show generated
    tickets"""
    _inherit = 'sale.order'

    helpdesk_ticket_id = fields.Many2one("helpdesk.ticket",
                                         string="HelpDesk Ticket")
    helpdesk_ticket_count = fields.Integer(string="tickets",
                                           compute=
                                           "_compute_helpdesk_ticket_count")

    def _compute_helpdesk_ticket_count(self):
        """Function to compute the number of tickets generated from sale
        order"""
        for rec in self:
            rec.helpdesk_ticket_count = (self.env['helpdesk.ticket'].
            search_count(
                [('id', '=', self.helpdesk_ticket_id.id)]))

    def action_generate_ticket(self):
        """Function to generate ticket"""
        team_id = self.env['helpdesk.team'].search(
            [('use_helpdesk_sale_timesheet',
              '=', True)], limit=1)
        helpdesk_ticket = self.env['helpdesk.ticket'].create({
            'name': 'Ticket' + ':' + str(self.name),
            'team_id': team_id.id,
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id
        })
        self.write({'helpdesk_ticket_id': helpdesk_ticket.id})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Helpdesk Ticket',
            'view_mode': 'form',
            'res_model': 'helpdesk.ticket',
            'res_id': helpdesk_ticket.id,
            'target': 'current'
        }
