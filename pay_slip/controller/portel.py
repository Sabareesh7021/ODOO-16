from odoo.addons.portal.controllers import portal
from odoo.http import request


class CustomerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payslip_count' in counters:
            payslips = request.env['hr.payslip'].sudo().search([])
            print(payslips)
            print(payslips.employee_id.user_id)
            print(request.env.user.id)


            values['payslip_count'] = payslips.sudo().search_count([('employee_id.user_id','=',request.env.user.id)])
            print(values['payslip_count'])

        return values
