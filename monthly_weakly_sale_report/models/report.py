# # from odoo import fields, models
# # import base64
# #
# #
# # class SaleOrder(models.Model):
# #     _inherit = 'sale.order'
# #
# #     def
# #         sale = self.env['sale.order'].search([])
# #         user = self.env['report.sales'].search([])
# #         # user = self.env['ir.model.access'].search([('name','=','stock.scrap.manager')]).group_id.users
# #         # print('im',user)
# #
# #         datas = {'product': sale}
# #
# #         report_template_id = self.env.ref('monthly_weakly_sale_report.action_sale_report')._render_qweb_pdf(
# #             'monthly_weakly_sale_report.action_sale_report', self.id, data=datas)
# #         data_record = base64.b64encode(report_template_id[0])
# #         ir_values = {
# #             'name': "Sale Order",
# #             'type': 'binary',
# #             'datas': data_record,
# #             'store_fname': data_record,
# #             'mimetype': 'application/pdf',
# #         }
# #         email_values = {
# #
# #             'email_to': user
# #         }
# #         data_id = self.env['ir.attachment'].create(ir_values)
# #         print('dataaa', data_id.id)
# #         mail_template = self.env.ref('monthly_weakly_sale_report.sale_report_email_template')
# #         mail_template.attachment_ids = [(6, 0, [data_id.id])]
# #         print('asd', [data_id.id])
# #         mail_template.send_mail(self.id, email_values=email_values, force_send=True)
# #         mail_template.attachment_ids = [(3, data_id.id)]
# #         return True
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import csv
#
# def generate_sales_report(self):
#     # filter the sales order data based on the configuration fields
#     orders = self.env['sale.order'].search([
#         ('partner_id', 'in', self.customers.ids),
#         ('team_id', '=', self.sales_team.id),
#         ('date_order', '>=', self.from_date),
#         ('date_order', '<=', self.to_date)
#     ])
#     data = []
#     # write the data to a csv file
#     with open("sales_report.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["Customer", "Product", "Quantity", "Total"])
#         for order in orders:
#             for line in order.order_line:
#                 writer.writerow([order.partner_id.name, line.product_id.name, line.product_uom_qty, line.price_total])
#                 data.append([order.partner_id.name, line.product_id.name, line.product_uom_qty, line.price_total])
#     # create the email message
#     msg = MIMEMultipart()
#     msg['From'] = "your_email@example.com"
#     msg['To'] = ",".join(self.email_recipients)
#     msg['Subject'] = "Weekly Sales Report"
#     msg.attach(MIMEText(data))
#     # send the email