# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api, _
from odoo.exceptions import MissingError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Warning to check if the qty of configured product is zero. And also to create new attribute custom value"""
        res = super(SaleOrder, self).action_confirm()
        self.ensure_one()
        list_product = list(self.order_line.mapped('product_template_id'))
        list_qty = list(self.order_line.mapped('product_uom_qty'))
        zero_qty_products = []
        if 0 in list_qty:
            zero_qty_products = [x.name for x, y in zip(list_product, list_qty)
                                 if y == float(
                    0) and x.has_configurable_attributes]
        if zero_qty_products:
            raise MissingError(
                _('Configured product(s) %s with zero quantity cannot be '
                  'sold, please add the qunatity and proceed. ',
                  (", ".join(zero_qty_products))))

        for rec in self.order_line:
            if rec.design_code_custom_flag.get('is_to_save') == "True":
                for item in rec.product_no_variant_attribute_value_ids._origin:
                    if item.is_custom_size:
                        customs = rec.product_custom_attribute_value_ids
                        for record in customs:
                            attr = record.custom_product_template_attribute_value_id.attribute_id
                            if record.custom_product_template_attribute_value_id.is_custom_size:
                                custom = record.custom_value
                                if custom:
                                    size_string = custom.replace("Custom ", "")
                                    find_attr = self.env[
                                        'product.attribute.value'].search(
                                        [('name', '=', size_string)])
                                    if not find_attr:
                                        if attr.display_type != 'color':
                                            new_attr_value = self.env[
                                                'product.attribute.value'].create(
                                                {
                                                    'name': size_string,
                                                    'attribute_id': attr.id,
                                                    'partner_id': self.partner_id.id
                                                })
                                            attribute_line = self.env[
                                                'product.template.attribute.line'].sudo().search(
                                                [('attribute_id', '=',
                                                  attr.id), (
                                                     'product_tmpl_id', '=',
                                                     rec.product_template_id.id)])
                                            attribute_line.write(
                                                {'value_ids': [
                                                    (4, new_attr_value.id)]})
        return res


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_attributes = fields.Json('Product Attributes', store=True,
                                     compute='_get_product_attributes')
    design_code_custom_flag = fields.Json('Design code & Custom flag',
                                          store=True)

    @api.depends('product_template_id')
    def _get_product_attributes(self):
        """Function modifies and assigns value to Json fields
        product_attributes will be used later for many purposes."""
        for rec in self:
            if not rec.product_custom_attribute_value_ids and not rec.product_no_variant_attribute_value_ids:
                return ""
            attributes = {}
            partner_id = self.order_id.partner_id
            customs = rec.product_custom_attribute_value_ids

            for item in rec.product_no_variant_attribute_value_ids._origin:
                attributes.update({
                    item.attribute_id.name: item.name})

            for record in customs:
                custom = record.custom_value
                if custom:
                    attributes.update({
                        record.custom_product_template_attribute_value_id.name: custom})

                    if 'x' in custom and 'Custom Size :' in custom:
                        numbers = re.findall(r'\d+\.\d+|\d+', custom)
                        numbers = [int(x) if x.isdigit() else float(x)
                                   for x
                                   in
                                   numbers]

                        if len(numbers) == 2:
                            record.length_custom = numbers[0]
                            record.width_custom = numbers[1]

                            if partner_id:
                                rec.product_custom_attribute_value_ids.partner_id = partner_id.id
            rec.product_attributes = attributes

    # @api.model_create_multi
    # def create(self, vals_list):
    #     order_line = super(SalesOrderLine, self).create(vals_list)
    #     for rec in order_line:
    #         if not rec.product_custom_attribute_value_ids and not rec.product_no_variant_attribute_value_ids:
    #             return ""
    #         attributes = {}
    #         if rec.product_attributes:
    #             attributes = rec.product_attributes
    #         partner_id = self.order_id.partner_id
    #         customs = rec.product_custom_attribute_value_ids
    #
    #         for item in rec.product_no_variant_attribute_value_ids._origin:
    #             attributes.update({
    #                 item.attribute_id.name: item.name})
    #         for record in customs:
    #             custom = record.custom_value
    #             if custom:
    #                 attributes.update({
    #                     record.custom_product_template_attribute_value_id.name: custom})
    #
    #                 if 'x' in custom and 'Custom Size :' in custom:
    #                     numbers = re.findall(r'\d+\.\d+|\d+', custom)
    #                     numbers = [int(x) if x.isdigit() else float(x)
    #                                for x
    #                                in
    #                                numbers]
    #
    #                     if len(numbers) == 2:
    #                         record.length_custom = numbers[0]
    #                         record.width_custom = numbers[1]
    #
    #                         if partner_id:
    #                             rec.product_custom_attribute_value_ids.partner_id = partner_id.id
    #         rec.product_attributes = attributes
    #
    #     return order_line
