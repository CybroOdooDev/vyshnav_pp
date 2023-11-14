from odoo import http
from odoo.http import request
from odoo.addons.sale_product_configurator.controllers.main import \
    ProductConfiguratorController


class IntervlagProductConfig(http.Controller):

    @http.route(['/get_is_customsize'], type="json", auth="public")
    def get_iscustom(self, **post):
        # value_id = (post['id']) #if value_id available
        value_name = post.get('name')
        value = request.env['product.template.attribute.value'].sudo(

        ).search([('name', '=', value_name)], limit=1)
        is_custom_size = value.is_custom_size
        return is_custom_size


class NewProductConfiguratorController(ProductConfiguratorController):
    @http.route(['/sale_product_configurator/show_advanced_configurator'],
                type='json', auth="user", methods=['POST'])
    def show_advanced_configurator(self, product_id, variant_values,
                                   pricelist_id, **kw):
        pricelist = self._get_pricelist(pricelist_id)
        partner_id = http.request.context.get('partner_id')
        return self._show_new_advanced_configurator(product_id, partner_id,
                                                    variant_values,
                                                    pricelist, False, **kw)

    def _show_new_advanced_configurator(self, product_id, partner_id,
                                        variant_values, pricelist,
                                        handle_stock, **kw):
        product = request.env['product.product'].browse(int(product_id))
        combination = request.env['product.template.attribute.value'].browse(
            variant_values)
        add_qty = float(kw.get('add_qty', 1))
        no_variant_attribute_values = combination.filtered(
            lambda
                product_template_attribute_value: product_template_attribute_value.attribute_id.create_variant == 'no_variant'
        )
        if no_variant_attribute_values:
            product = product.with_context(
                no_variant_attribute_values=no_variant_attribute_values)
        return request.env['ir.ui.view']._render_template(
            "sale_product_configurator.optional_products_modal", {
                'product': product,
                'combination': combination,
                'add_qty': add_qty,
                'parent_name': product.name,
                'variant_values': variant_values,
                'pricelist': pricelist,
                'handle_stock': handle_stock,
                'already_configured': kw.get("already_configured", False),
                'mode': kw.get('mode', 'add'),
                'product_custom_attribute_values': kw.get(
                    'product_custom_attribute_values', None),
                'no_attribute': kw.get('no_attribute', False),
                'custom_attribute': kw.get('custom_attribute', False),
                'partner': partner_id
            })

