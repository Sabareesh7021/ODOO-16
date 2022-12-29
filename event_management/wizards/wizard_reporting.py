from odoo import fields, models
from odoo.tools import date_utils, date
from odoo.exceptions import ValidationError
import io
import json
from odoo.tools.misc import xlsxwriter
import xlsxwriter


class TestModelWizard(models.TransientModel):
    _name = 'test.model.wizard'
    _description = 'Test Model Wizard'
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    event_type_id = fields.Many2one("event.type", string='Event Type')
    catering = fields.Boolean(string="Catering")

    def print_event_management_pdf(self):
        query = """select DISTINCT eb.id as eid,c.id as cid,eb.event,rp.name as cust,eb.booking_date,eb.state,et.event_type,c.grand_total,
                    cm.name,cm.category,cm.unit_price,cl.sub_total  
                    from event_booking as eb inner join res_partner as rp on rp.id = eb.cust_name 
                    inner join event_type as et on et.id = eb.event_type
                    inner join event_catering as c on c.event_id = eb.id
                    inner join menu_tree as cl on c.id = cl.welcome_drink or cl.dinner = c.id 
                    or cl.break_fast = c.id or cl.lunch = c.id
                    or cl.snacks_and_drinks = c.id or cl.beverages = c.id
                    inner join catering_menu as cm on cm.id = cl.menu_id
                    inner join uom_uom on uom_uom.id = cm.unit_measure"""

        if self.event_type_id:
            query += """ where et.id = %d""" % self.event_type_id.id
        if self.date_from:
            query += """ and eb.start_date >= '%s' """ % self.date_from
        if self.date_to:
            query += """ and eb.end_date <= '%s' """ % self.date_to

        self.env.cr.execute(query)
        event = self.env.cr.dictfetchall()
        if not event:
            raise ValidationError('THERE IS NO EVENT BOOKING')
        val = []
        total = 0
        for rec in event:
            if {'event': rec['event'], 'event_type': rec['event_type'], 'cust': rec['cust'], 'booking_date': rec['booking_date'], 'state': rec['state'], 'grand_total': rec['grand_total']} in val:
                pass
            else:
                val.append({'event': rec['event'],
                            'event_type': rec['event_type'],
                            'cust': rec['cust'],
                            'booking_date': rec['booking_date'],
                            'state': rec['state'],
                            'grand_total': rec['grand_total']
                            })
                total = total + rec['grand_total']
        data = {
            'form_data': self.read()[0],
            'event': event,
            'val': val,
            'total': total

        }
        return self.env.ref('event_management.action_event_management_report').report_action(None, data=data)

    def print_xlsx(self):

        query = """select eb.event,rp.name as cust,eb.booking_date,eb.state,et.event_type,ec.grand_total,eb.start_date,eb.end_date
                    from event_booking as eb 
                    inner join res_partner as rp on rp.id = eb.cust_name 
                    inner join event_type as et on et.id = eb.event_type
                    inner join event_catering as ec on ec.event_id = eb.id"""
        if self.event_type_id:
            query += """ where et.id = %d""" % self.event_type_id.id
        if self.date_from:
            query += """ and eb.start_date >'%s' """ % self.date_from
        if self.date_to:
            query += """ and eb.end_date <'%s' """ % self.date_to

        self.env.cr.execute(query)
        event = self.env.cr.dictfetchall()
        if not event:
            raise ValidationError('THERE IS NO EVENT BOOKING')
        data = {
            'from_date': self.date_from,
            'to_date': self.date_to,
            'event': event,
            'event_type_id': self.event_type_id.event_type,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'test.model.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        current = str(date.today())

        cell_format = workbook.add_format({'font_size': '12px', 'bold': True})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'align': 'center', 'font_size': '10px'})
        table_head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '10px', 'bg_color': '#808080'})
        sheet.set_column('C:C', 10)
        sheet.set_column('D:D', 70)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 15)

        sheet.merge_range('D2:E3', 'Event Management', head)
        if data['event_type_id']:
            sheet.merge_range('D4:E4', data['event_type_id'], txt)
        if data['from_date']:
            sheet.write('C7', 'From Date:', cell_format)
            sheet.write('D7', data['from_date'], cell_format)
            if data['to_date']:
                sheet.write('C8', 'To Date:', cell_format)
                sheet.write('D8', data['to_date'], cell_format)
        else:
            sheet.write('C8', 'Date:', cell_format)
            sheet.write('D8', current, cell_format)
        row = 9
        col = 2
        sheet.write(row, col, 'References', table_head)
        sheet.write(row, col + 1, 'Event Name', table_head)
        sheet.write(row, col + 2, 'Event Type', table_head)
        if data['event_type_id']:
            sheet.write(row, col + 3, 'Customer', table_head)
            sheet.write(row, col + 4, 'Booking Date', table_head)
            sheet.write(row, col + 5, 'Status', table_head)
            sheet.write(row, col + 6, 'Total Amount', table_head)
        ref = 0
        total = 0
        for event in data['event']:
            row += 1
            ref += 1
            sheet.write(row, col, ref)
            sheet.write(row, col + 1, event['event'])
            sheet.write(row, col + 2, event['event_type'])
            if data['event_type_id']:
                sheet.write(row, col + 3, event['cust'])
                sheet.write(row, col + 4, event['booking_date'])
                sheet.write(row, col + 5, event['state'])
                sheet.write(row, col + 6, event['grand_total'])
                total = total + event['grand_total']

        if data['event_type_id']:
            sheet.write(row + 1, col + 5, "Total", cell_format)
            sheet.write(row + 1, col + 6, total)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()