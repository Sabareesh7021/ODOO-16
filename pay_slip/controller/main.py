
from odoo import http
from odoo.http import request


class Products(http.Controller):
    @http.route(['/my/payslip'], type='http', auth="user", website=True)
    def _my_account_payslip(self, **kwargs):
        payslip_ids = request.env['hr.payslip'].sudo().search([('employee_id.user_id', '=', request.env.user.id)])
        print(payslip_ids)
        return http.request.render('pay_slip.portal_my_payslips', {'payslip_ids': payslip_ids})
