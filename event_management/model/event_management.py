from datetime import datetime
from odoo import fields, models, _, api


class EventType(models.Model):
    _name = "event.type"
    _description = "Event Type"
    _rec_name = 'event_type'

    event_type = fields.Char(string="Event Type", required=True)
    code = fields.Integer(string="Code")
    image = fields.Image(string="Image")


class EventService(models.Model):
    _name = "event.service"
    _description = "Event Service"
    _rec_name = "service"

    service = fields.Char(string="Service")
    responsible_person = fields.Many2one('res.users', string="Responsible Person")
    order_id = fields.One2many("service.table", "relation_id", string="Order line")


class ServiceTable(models.Model):
    _name = "service.table"
    _description = "Service Table"

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    relation_id = fields.Many2one('event.service')
    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    sub_total = fields.Float(string="Sub Total")

    @api.onchange('unit_price', 'quantity')
    def _compute_sub_total(self):
        for rec in self:
            rec.sub_total = rec.unit_price * rec.quantity


class EventBooking(models.Model):
    _name = "event.booking"
    _inherit = 'mail.thread', 'mail.activity.mixin'
    _description = "Event Booking"
    _rec_name = "event"

    event = fields.Char(string="Event", compute="get_name", store=True)
    cust_name = fields.Many2one('res.partner', string="Customer", required=True)
    event_type = fields.Many2one('event.type', required=True)
    booking_date = fields.Date()
    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    duration_id = fields.Char(string='Duration')
    bool_field = fields.Boolean('Same text', default=False)
    invoice_id = fields.Many2one('account.move')
    catering_id = fields.Many2one('event.catering')
    # sale_order = fields.Many2one('sale.order')

    @api.onchange('start_date', 'end_date')
    def auto_duration(self):
        if self.start_date and self.end_date:
            start_date = datetime.strptime(str(self.start_date), '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(str(self.end_date), '%Y-%m-%d %H:%M:%S')
            duration = end_date - start_date
            self.duration_id = str(duration.days)
        else:
            self.duration_id = '0'

    @api.depends('event_type.event_type', 'cust_name.name', 'start_date', 'end_date')
    def get_name(self):
        result = []
        for event in self:
            result.append((event.id, '%s:%s / %s: %s' % (
                event.event_type.event_type, event.cust_name.name, event.start_date, event.end_date)))
            event.event = str(
                '%s:%s /%s: %s' % (event.event_type.event_type, event.cust_name.name, event.start_date, event.end_date))
            return result

    def catering_service(self):
        self.bool_field = True
        return {
            'name': _('Event Catering'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'event.catering',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ({'default_event_id': self.id})
        }

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirmed'),
            ("invoice", "Invoice"),
            ("paid", "Paid"),
            ('expired', 'Expired'),
        ], default="draft"
    )

    def action_confirm(self):
        self.state = 'confirm'
        self.env['event.catering'].search([('state', '=', 'draft')]).action_confirm()
        # self.env['sale.order'].search([('state', '!=', 'sale')]).action_confirm()

    def action_invoice(self):
        self.state = 'invoice'
        vals = []
        inv = self.env['event.catering'].search([('event_id', '=', self.id)])
        for rec in inv.category_welcome_drink_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        for rec in inv.category_break_fast_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        for rec in inv.category_lunch_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        for rec in inv.category_dinner_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        for rec in inv.category_snacks_and_drinks_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        for rec in inv.category_beverages_ids:
            vals.append((0, 0,
                         {
                             'name': rec.menu_id.name,
                             'quantity': rec.quantity,
                             'price_unit': rec.unit_price,
                             'price_subtotal': rec.sub_total,
                             'tax_ids': [],
                         }))
        self.write({'state': 'invoice'})
        invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.cust_name.id,
            'invoice_line_ids': vals,
        }])
        self.invoice_id = invoice.id
        return {
            'name': 'invoice',
            'view_mode': 'form',
            'res_id': invoice.id,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def get_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_id': self.invoice_id.id,
            'target': 'current',
            'context': {"create": False},
            }

    def action_view_catering(self):
        event = self.env['event.catering'].search([('event_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'catering',
            'view_mode': 'form',
            'res_model': 'event.catering',
            'res_id': event.id,
            'target': 'current',
        }


class Invoice(models.Model):
    _inherit = 'account.move'
    invoice_id = fields.Many2one("event.booking")

    def action_register_payment(self):
        res = super(Invoice, self).action_register_payment()
        for res in self:
            res.payment_state = "paid"
            state = self.env['event.booking'].search([('event.id', '=', self.id)])
            state.write({'state': 'paid'})
        return res


class EventCatering(models.Model):
    _name = 'event.catering'
    _description = "Event Catering"
    _rec_name = "sequence"

    sequence = fields.Char(required=True, readonly=True, default=lambda self: _('New'))
    event_id = fields.Many2one('event.booking', string='Event')
    date = fields.Date(string="Date", related="event_id.booking_date")
    s_date = fields.Datetime(string="Start Date", related="event_id.start_date")
    e_date = fields.Datetime(string="End Date", related="event_id.end_date")
    guests = fields.Integer(string="Guests")
    welcome_drink = fields.Boolean(string="Welcome Drink")
    category_welcome_drink_ids = fields.One2many('menu.tree', 'welcome_drink', string="welcome drink")
    break_fast = fields.Boolean(string="Break Fast")
    category_break_fast_ids = fields.One2many("menu.tree", "break_fast", string="Break Fast")
    lunch = fields.Boolean(string="Lunch")
    category_lunch_ids = fields.One2many("menu.tree", "lunch", string="Lunch")
    dinner = fields.Boolean(string="Dinner")
    category_dinner_ids = fields.One2many("menu.tree", "dinner", string="Dinner")
    snacks_and_drinks = fields.Boolean(string="Snacks & Drinks")
    category_snacks_and_drinks_ids = fields.One2many("menu.tree", "snacks_and_drinks", string="Snacks & Drinks")
    beverages = fields.Boolean(string="Beverages")
    category_beverages_ids = fields.One2many("menu.tree", "beverages", string="Beverages")
    grand_total = fields.Float(string='Grand Total', compute="_compute_grand_total", store=True)
    catering_id = fields.Many2one('event.booking')

    def action_confirm(self):
        self.state = 'confirm'

    def action_delivery(self):
        self.state = 'deliver'

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirmed'),
            ('deliver', 'Delivered'),
            ('expired', 'Expired'),
        ], default="draft"
    )

    @api.onchange('end_date')
    def _action_expired(self):
        current_date = fields.Date.today()
        for rec in self:
            if current_date > rec.end_date:
                self.state = 'expired'
            else:
                self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'event.code') or _('New ')

        res = super(EventCatering, self).create(vals)
        return res

    @api.depends('category_welcome_drink_ids.sub_total', 'category_break_fast_ids.sub_total', 'category_lunch_ids'
                                                                                              '.sub_total',
                 'category_dinner_ids.sub_total', 'category_snacks_and_drinks_ids.sub_total', 'category_beverages_ids'
                                                                                              '.sub_total')
    def _compute_grand_total(self):
        self.grand_total = sum(
            (self.category_welcome_drink_ids.mapped('sub_total')) + (self.category_break_fast_ids.mapped('sub_total')) +
            (self.category_lunch_ids.mapped('sub_total')) + (self.category_dinner_ids.mapped('sub_total')) +
            (self.category_snacks_and_drinks_ids.mapped('sub_total')) + (self.category_beverages_ids.mapped('sub_total')))


class EventCateringMenu(models.Model):
    _name = "catering.menu"
    _description = "Catering Menu"
    _rec_name = "name"

    name = fields.Char(string='Item')
    category = fields.Selection(string='Category',
                                selection=[('welcome drink', 'Welcome Drink'), ('break fast', 'Break Fast'),
                                           ('lunch', 'Lunch'), ('snacks ''and ''drinks', 'Snacks ' 'And ''Drinks'),
                                           ('beverages', 'Beverages')])
    image = fields.Binary(string='Image')
    description = fields.Char(string='Description')
    quantity = fields.Integer(string='Quantity', default=1)
    unit_measure = fields.Many2one('uom.uom', string='Unit of Measure')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    unit_price = fields.Monetary(string='Unit Price')


class MenuTree(models.Model):
    _name = 'menu.tree'
    _description = 'Menu Tree'

    menu_id = fields.Many2one('catering.menu', string='Item')
    description = fields.Char(string='Description')
    quantity = fields.Integer(string='Quantity', default=1)
    unit_measure = fields.Many2one('uom.uom', string='Unit of Measure', related='menu_id.unit_measure')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    unit_price = fields.Monetary(string='Unit Price', related='menu_id.unit_price')
    sub_total = fields.Monetary(string='subtotal')
    welcome_drink = fields.Many2one("event.catering")
    break_fast = fields.Many2one("event.catering")
    lunch = fields.Many2one("event.catering")
    dinner = fields.Many2one("event.catering")
    snacks_and_drinks = fields.Many2one("event.catering")
    beverages = fields.Many2one("event.catering")

    @api.onchange('unit_price', 'quantity')
    def _suba_total(self):
        self.sub_total = self.unit_price * self.quantity
