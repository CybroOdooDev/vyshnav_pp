# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.osv import expression


class HelpdeskTeam(models.Model):
    """Inherited helpdesk.team class to add required fields and functions to
    display valid and invalid tickets on dashboard"""
    _inherit = "helpdesk.team"

    valid_ticket_count = fields.Integer(string="Valid ticket count",
                                        compute="compute_valid_ticket_count")
    invalid_ticket_count = fields.Integer(string="Invalid ticket count",
                                          compute="compute_invalid_ticket_count")

    def compute_valid_ticket_count(self):
        """Function to compute the count of valid tickets"""
        for rec in self:
            rec.valid_ticket_count = (self.env['helpdesk.ticket'].
            search_count(
                [('ticket_status', '=', 'valid'), ('team_id', 'in', rec.ids)]))

    def compute_invalid_ticket_count(self):
        """Function to compute the count of invalid tickets"""
        for rec in self:
            rec.invalid_ticket_count = (self.env['helpdesk.ticket'].
            search_count(
                [('ticket_status', '=', 'invalid'),
                 ('team_id', 'in', rec.ids)]))

    def action_view_valid_ticket(self):
        """Function to display  the valid tickets"""
        action = self.action_view_ticket()
        action_params = self._get_action_view_ticket_params()
        action.update({
            'context': action_params['context'],
            'domain': expression.AND(
                [action_params['domain'], [('ticket_status', '=', 'valid')]]),
        })
        return action

    def action_view_invalid_ticket(self):
        """Function to display invalid tickets"""
        action = self.action_view_ticket()
        action_params = self._get_action_view_ticket_params()
        action.update({
            'context': action_params['context'],
            'domain': expression.AND(
                [action_params['domain'], [('ticket_status', '=', 'invalid')]]),
        })
        return action
