from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleBom(WebsiteSale):
    @http.route()
    def cart(self, access_token=None, revive='', **post):
        res = super(WebsiteSaleBom, self).cart(access_token=access_token, revive=revive, **post)
        bom_product_ids = request.env['ir.config_parameter'].sudo().get_param('many2many.bom_id')
        lst = eval(bom_product_ids)
        bom_ids = request.env['mrp.bom'].sudo().browse(lst).product_tmpl_id.ids
        values = res.qcontext
        values['bom'] = bom_ids
        return request.render("website_sale.cart", values)
        return res
