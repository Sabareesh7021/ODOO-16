from odoo import models, fields


class DueLimit(models.Model):
    _inherit = 'res.partner'
    limit = fields.Monetary(string='Limit')
