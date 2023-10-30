# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api


class HelpdeskTicket(models.Model):
    """Inherited helpdesk.ticket class to add required fields and functions"""
    _inherit = "helpdesk.ticket"

    def _default_team_id(self):
        team_id = self.env['helpdesk.team'].search(
            [('member_ids', 'in', self.env.uid), ('use_helpdesk_sale_timesheet',
                                                  '=', True)], limit=1).id
        if not team_id:
            team_id = self.env['helpdesk.team'].search([], limit=1).id
        return team_id

    name = fields.Char(string="Name", default="New")
    complaint_department_id = fields.Many2one('complaint.department',
                                              string="Complaint Department")
    complaint_category_ids = fields.Many2many('complaint.category',
                                              string="Complaint Category")
    complaint_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')],
        string="Complaint Type")
    cost_of_restore = fields.Float(string="Cost Of Restore")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    start_date = fields.Date(string="Start Date", readonly=1)
    solved_date = fields.Date(string="Solved Date", readonly=1)
    new_sale_order_id = fields.Many2one('sale.order',
                                        string="New Sale Order", readonly=1)

    total_order_amount = fields.Monetary(related="sale_order_id.amount_total",
                                         string="Order Amount", store=True)
    ticket_status = fields.Selection(
        [('valid', 'Valid'), ('invalid', 'Invalid')],
        string='Complaint Validation',
        default='valid')
    desired_solutions = fields.Html(string="Desired Solutions")

    @api.onchange('complaint_department_id')
    def complaint_department_id_onchange(self):
        """Function to set domain for complaint category field"""
        return {'domain': {'complaint_category_ids': [('id', 'in',
                                                       self.
                                                       complaint_department_id.
                                                       complaint_category_ids.
                                                       ids)]}}

    @api.depends('sale_order_id', 'name')
    def _compute_name(self):
        for rec in self:
            if rec.sale_order_id:
                rec.name = 'Ticket' + ':' + str(rec.sale_order_id.name)
            elif rec._origin.id:
                rec.name = 'Ticket' + ':' + str(rec._origin.id)
            else:
                rec.name = 'Ticket' + ':' + "New"

    def action_create_sale_order(self):
        """Function to create sale order from ticket and to display created
        ticket"""
        new_sale_order_id = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'helpdesk_ticket_id': self.id
        })
        sale_order_line = self.sale_order_id.order_line
        for rec in sale_order_line:
            self.env['sale.order.line'].create({
                'order_id': new_sale_order_id.id,
                'name': rec.product_template_id.name,
                'product_id': rec.product_id.id,
                'product_template_id': rec.product_template_id.id,
                'product_uom_qty': rec.product_uom_qty
            })
        self.write({'new_sale_order_id': new_sale_order_id.id})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': new_sale_order_id.id,
            'target': 'current'
        }

    def action_timer_start(self):
        """overridden function to add start date"""
        if not self.start_date:
            self.start_date = date.today()
        super().action_timer_start()

    def action_timer_stop(self):
        """overridden function to add solved date"""
        self.solved_date = date.today()
        super().action_timer_stop()
        if self.user_timer_id.timer_start and self.display_timesheet_timer:
            minutes_spent = self.user_timer_id._get_minutes_spent()
            minimum_duration = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'timesheet_grid.timesheet_min_duration', 0))
            rounding = int(self.env['ir.config_parameter'].sudo().get_param(
                'timesheet_grid.timesheet_rounding', 0))
            minutes_spent = self._timer_rounding(minutes_spent,
                                                 minimum_duration, rounding)
            return self._action_open_new_timesheet(minutes_spent * 60 / 3600)
        return False

    @api.model_create_multi
    def create(self, vals_list):
        ticket = super(HelpdeskTicket, self).create(vals_list)
        if ticket.sale_order_id:
            ticket.name = ticket.sale_order_id.name
        else:
            ticket.name = 'Ticket' + '#' + str(ticket.ticket_ref)
        return ticket

    # def name_get(self):
    #     result = []
    #     for ticket in self:
    #         if ticket.sale_order_id:
    #             ticket.name = ticket.sale_order_id.name
    #         else:
    #             result.append(
    #                 (ticket.id, "%s (#%s)" % ('Ticket', ticket.ticket_ref)))
    #     return result
