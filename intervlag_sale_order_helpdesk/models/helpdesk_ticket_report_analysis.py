# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class HelpdeskTicketReportAnalysis(models.Model):
    """Inherited helpdesk.ticket.report.analysis class to add required fields
    and functions to display filters and measures on reporting section"""
    _inherit = "helpdesk.ticket.report.analysis"

    complaint_department_id = fields.Many2one('complaint.department',
                                              string='Complaint Department',
                                              readonly=True)
    complaint_category_ids = fields.Many2many('complaint.category',
                                              relation='complaint_category_helpdesk_ticket_rel',
                                              column1='helpdesk_ticket_id',
                                              column2='complaint_category_id',
                                              string='Complaint Category',
                                              readonly=True)
    complaint_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')],
        string="Complaint Type")
    ticket_status = fields.Selection([
        ('valid', 'Valid'),
        ('invalid', 'Invalid')], default=False)
    cost_of_restore = fields.Float(string="Cost Of Restore")
    valid_ticket_percentage = fields.Float(string="Valid Ticket percentage")
    total_order_amount = fields.Float(string="Total amount of orders")
    description = fields.Html(string="Description")
    average_cost = fields.Float(string="Average Cost Of Restore")

    def _select(self):
        """Function used for SELECT query"""
        select_str = super()._select()
        select_str += ", T.complaint_department_id as complaint_department_id"
        select_str += ", T.complaint_type as complaint_type"
        select_str += ", T.ticket_status as ticket_status"
        select_str += ", T.cost_of_restore as cost_of_restore"
        select_str += (
            ", (COUNT(CASE WHEN T.ticket_status = 'valid' THEN 1 ELSE NULL "
            "END) )"
            "/ COUNT(T.id) AS valid_ticket_percentage"
        )
        select_str += (
            ", T.cost_of_restore/COUNT(T.id) AS average_cost"
        )
        select_str += ", T.total_order_amount as total_order_amount"
        select_str += ", T.description as description"
        return select_str

    def _group_by(self):
        """Function used for GROUP BY query"""
        group_by_str = """
            GROUP BY T.id,
            EMP.parent_id,
            DEP.id,
            EMP.id
                """
        return group_by_str

    def init(self):
        """Function to execute the SQL query"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            )""" % (
            self._table, self._select(), self._from(), self._group_by()))
