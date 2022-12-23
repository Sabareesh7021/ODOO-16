from odoo import fields, models,_
from odoo.exceptions import ValidationError


class TestModelWizard(models.TransientModel):
    _name = 'test.model.wizard'
    _description = 'Test Model Wizard'
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    event_type_id = fields.Many2one("event.type", string='Event Type')
    catering = fields.Boolean(string="Catering")

    def print_event_management_pdf(self):
        query = """select DISTINCT eb.id as eid,c.id as cid,eb.event,rp.name as cust,eb.booking_date,eb.state,et.event_type,c.grand_total,
                cm.name,cm.category,cm.unit_price,uom_uom.name as uom,cl.description,cl.quantity,cl.sub_total  
                from event_booking as eb inner join res_partner as rp on rp.id = eb.cust_name 
                inner join event_type as et on et.id = eb.event_type
                inner join event_catering as c on c.event_id = eb.id
                inner join menu_tree as cl on c.id = cl.welcome_drink or cl.dinner = c.id 
                or cl.break_fast = c.id or cl.lunch = c.id
                or cl.snacks_and_drinks = c.id or cl.beverages = c.id
                inner join catering_menu as cm on cm.id = cl.menu_id
                inner join uom_uom on uom_uom.id = cm.unit_measure"""

        if self.event_type_id:
            query += """ where et.id = %d """ % self.event_type_id.id
        if self.date_from:
            query += """ and eb.start_date > '%s' """ % self.date_from
        if self.date_to:
            query += """ and eb.end_date < '%s' """ % self.date_to

        self.env.cr.execute(query)
        event = self.env.cr.dictfetchall()
        if not event:
            raise ValidationError('THERE IS NO EVENT BOOKING')
        data = {
            'form': self.read()[0],
            'val': event

        }
        return self.env.ref('event_management.action_event_management_report').report_action(None, data=data)
