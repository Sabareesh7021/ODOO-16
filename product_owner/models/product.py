from odoo import fields, models


class ProductOwner(models.Model):
    _inherit = 'product.template'
    product_owner_id = fields.Many2one('res.partner', string="Owner")
