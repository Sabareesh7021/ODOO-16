from odoo import fields, models, api


class Margin(models.Model):
    _inherit = "sale.order.line"
    margin = fields.Float(string="Margin", compute='_compute_margin')

    @api.depends('price_subtotal', 'product_uom_qty', 'product_id.standard_price')
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty)


class SalesMargin(models.Model):
    _inherit = "sale.order"
    total_sum = fields.Monetary(string="Total Margin", compute='_compute_amount')

    @api.depends('order_line.margin')
    def _compute_amount(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.total_sum = sum(order_lines.mapped('margin'))
