# -*- coding: utf-8 -*-
from odoo import fields, models


class ComplaintCategory(models.Model):
    """Class for complaint Category which will be child of complaint department
     used in helpdesk tickets"""
    _name = "complaint.category"
    _description = "complaint category"

    name = fields.Char(string="Complaint Category Name")
