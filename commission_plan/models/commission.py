from odoo import fields, models, api


class Commission(models.Model):
    _name = "crm.commission"
    _description = "Commission Plan"
    _rec_name = "name"

    name = fields.Char(string="Name")
    active = fields.Boolean(string='Active', default=True)
    from_date = fields.Date(string="From")
    to_date = fields.Date(string='To')
    type = fields.Selection(string='Type',
                            selection=[('product wise', 'Product Wise'), ('revenue wise', 'Revenue Wise')])
    product_wise_ids = fields.One2many('product.wise', 'product_wise_id')
    type_revenue = fields.Selection(string='Revenue Method', selection=[('straight', 'Straight'), ('graduated', 'Graduated')])
    rate = fields.Float(string="Rate")
    graduated_commission_ids = fields.One2many('graduated.commission', 'commission_id')


class GraduatedCommission(models.Model):
    _name = "graduated.commission"
    _description = "Graduated Commission"

    sequence = fields.Integer(string='Sequence')
    amount_from = fields.Float(string='Amount (From)')
    amount_to = fields.Float(string='Amount (To)')
    graduated_rate = fields.Float(string='Rate')
    commission_id = fields.Many2one('crm.commission', invisible=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    commission_value = fields.Float(string="Commission", required=True)
    commission_plan_id = fields.Many2one(related='team_id.commission_plan_id')

    @api.onchange('order_line', 'commission_plan_id')
    def _commission(self):
        self.commission_value = 0
        commission = 0
        amount = self.amount_untaxed
        plan = self.commission_plan_id
        commission_type = self.commission_plan_id.type
        if commission_type == 'product wise':
            for record in plan.product_wise_ids:
                for rec in self.order_line:
                    if record.product == rec.product_template_id:
                        rate = record.rate_in_percentage
                        commission += rec.price_subtotal*rate
                        if commission > record.max_commission_amount:
                            commission = record.max_commission_amount
        elif commission_type == 'revenue wise':
            if plan.type_revenue == 'straight':
                commission = amount * plan.rate
            elif plan.type_revenue == 'graduated':
                for i in plan.graduated_commission_ids:
                    amount_from = i.amount_from
                    amount_to = i.amount_to
                    rate = i.graduated_rate
                    if amount < amount_from:
                        pass
                    elif amount_from < amount <= amount_to:
                        commission += amount * rate
                    elif amount > amount_to:
                        commission += amount_to * rate
                        amount = amount - amount_to
        self.commission_value = commission


class SalesTeam(models.Model):
    _inherit = 'crm.team'
    commission_plan_id = fields.Many2one('crm.commission', string='Commission Plan')
