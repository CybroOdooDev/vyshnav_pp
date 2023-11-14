# -*- coding: utf-8 -*-
from odoo import models, fields


class RestrictionConfigurator(models.Model):
    """Class for adding name and restriction rules for attribute value"""
    _name = "restriction.configurator"
    _description = 'Restriction Configurator'

    name = fields.Char(string='Name',required= True)
    restriction_rule_ids = fields.One2many('restriction.rule',
                                           'restriction_configurator_id',
                                           string="Rules")
