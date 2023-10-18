# -*- coding: utf-8 -*-
from odoo import fields, models


class ComplaintDepartment(models.Model):
    """Class for complaint department used in helpdesk tickets"""
    _name = "complaint.department"
    _description = "complaint department"

    name = fields.Char(string="Department Name", help="add department name in "
                                                      "this field")
    complaint_category_ids = fields.Many2many("complaint.category",
                                              string="Complaint Categories",
                                              help="Choose complaint Categories"
                                              )
