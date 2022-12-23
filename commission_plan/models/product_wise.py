from odoo import fields, models


class ProductWise(models.Model):
    _name = 'product.wise'
    _description = 'Product Wise'

    product_wise_id = fields.Many2one('crm.commission')
    product = fields.Many2one("product.template", string="Product")
    product_category = fields.Many2one(related='product.categ_id', string="Product Category")

    rate_in_percentage = fields.Float(string="Rate in Percentage")
    max_commission_amount = fields.Float(string='Max Commission Amount')
