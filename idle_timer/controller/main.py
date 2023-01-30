from odoo import http
from odoo.http import request


class IdleTimerController(http.Controller):
    @http.route('/survey/idle/timer', type='json', auth='public')
    def get_token_idle_timer(self, token):
        survey = request.env['survey.survey'].sudo().search([('access_token', '=', token)])
        print(token)
        # if survey.idle == True:
        values = {'idle_time': survey.idle_timer,
                  'idle': survey.idle,
                  }
        return values
