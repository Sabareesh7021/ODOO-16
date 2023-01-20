from odoo import models, fields
from datetime import timedelta
import calendar
import base64


class Filter(models.Model):
    _name = 'report.sales'
    _description = 'Report filter'
    sales_team = fields.Many2one('crm.team', string='Sales Team')
    types = fields.Selection(selection=[('weekly', 'Weekly'), ('monthly', 'Monthly')], string='Type', required=True)
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    customers = fields.Many2many('res.partner')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    def action_monthly_mail(self):
        print(45678)
        report = self.env['report.sales'].search([])
        if report.types == 'monthly':
            name = 'Monthly Report'
            today = fields.Date.today()
            year = today.year
            month = today.month
            f_month = report.from_date.month
            print(f_month)
            f_year = report.from_date.year
            print(f_year)
            _, last_day = calendar.monthrange(year, month)
            end_date = fields.date(year=year, month=month, day=last_day)
            print('sdfrgthyjkl;', end_date)
            new_date = fields.Date.add(end_date, months=1)
            first_day_of_month = fields.Date.today().replace(day=1)
            print(first_day_of_month)
            print(new_date)
            customers = self.env['report.sales'].search([]).mapped('customers')
            for i in customers:
                if f_month == month and++++++ f_year == year:
                    datas = self.env['sale.order'].search([('team_id', '=', report.sales_team.id), ('date_order', '>=', report.from_date), ('date_order', '<=', end_date)])
                    print(23456789)
                    sales = {'product': datas,
                             'from_date': report.from_date,
                             'to_date': end_date,
                             'name': name}
                else:
                    datas = self.env['sale.order'].search([('team_id', '=', report.sales_team.id), ('date_order', '>=', first_day_of_month), ('date_order', '<=', end_date)])
                    sales = {'product': datas,
                             'from_date': first_day_of_month,
                             'to_date': end_date,
                             'name': name}
                    print(234567890)
            report_template_id = self.env.ref('monthly_weakly_sale_report.sale_report_pdf')._render_qweb_pdf('monthly_weakly_sale_report.sale_report_pdf',
                                                         self.id, data=sales)
            data_record = base64.b64encode(report_template_id[0])
            ir_values = {
                'name': "Sale Report",
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            }
            data_id = self.env['ir.attachment'].create(ir_values)

            template = self.env.ref('monthly_weakly_sale_report.sale_report_email_template')
            template.attachment_ids = [(6, 0, [data_id.id])]
            email_values = {'email_to': i.email,
                            'subject': 'Monthly Report'
                            }

            template.send_mail(self.id, email_values=email_values, force_send=True)
            template.attachment_ids = [(3, data_id.id)]
            return True
    
    def action_weekly_mail(self):
        report = self.env['report.sales'].search([])
        if report.types == 'weekly':
            name = 'Weekly Report'
            current_date = fields.Date.today()
            current_weekday = current_date.weekday()
            remaining_days = 6 - current_weekday
            sunday_of_current_week = current_date + timedelta(days=remaining_days)
            print(sunday_of_current_week)
            monday_of_current_week = current_date - timedelta(days=current_weekday)

            print(monday_of_current_week)
            # if monday_of_current_week == report.from_date:
            #     datas = self.env['sale.order'].search([('team_id', '=', report.sales_team.id), ('date_order', '>=', monday_of_current_week), ('date_order', '<=', sunday_of_current_week)])

            customers = self.env['report.sales'].search([]).mapped('customers')
            for i in customers:
                if monday_of_current_week < report.from_date and report.from_date < sunday_of_current_week:
                    print(23456789)
                    datas = self.env['sale.order'].search([('team_id', '=', report.sales_team.id), ('date_order', '>=', report.from_date), ('date_order', '<=', sunday_of_current_week)])
                    sales = {'product': datas,
                             'from_date': monday_of_current_week,
                             'to_date': sunday_of_current_week,
                             'name': name}

                else:
                    datas = self.env['sale.order'].search([('team_id', '=', report.sales_team.id), ('date_order', '>=', monday_of_current_week), ('date_order', '<=', sunday_of_current_week)])
                    sales = {'product': datas,
                             'from_date': monday_of_current_week,
                             'to_date': sunday_of_current_week,
                             'name': name}
            # sales = {'product': datas,
            #          'from_date': monday_of_current_week,
            #          'to_date': sunday_of_current_week,
            #          'name': name}
            print(datas)
            report_template_id = self.env.ref('monthly_weakly_sale_report.sale_report_pdf')._render_qweb_pdf(
                'monthly_weakly_sale_report.sale_report_pdf',
                self.id, data=sales)
            data_record = base64.b64encode(report_template_id[0])
            ir_values = {
                'name': "Sale Report",
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            }
            data_id = self.env['ir.attachment'].create(ir_values)

            template = self.env.ref('monthly_weakly_sale_report.sale_report_email_template')
            template.attachment_ids = [(6, 0, [data_id.id])]
            email_values = {'email_to': i.email,
                            'subject': 'Weekly Report'
                            }

            template.send_mail(self.id, email_values=email_values, force_send=True)
            template.attachment_ids = [(3, data_id.id)]
            return True
