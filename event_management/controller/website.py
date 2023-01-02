from odoo import http, fields
from odoo.http import request


class WebsitePage(http.Controller):
    @http.route('/event_booking', type='http', auth='public', website=True)
    def event_booking(self):
        et = request.env['event.type'].sudo().search([])
        customer = request.env['res.partner'].sudo().search([])
        return request.render("event_management.website_page_event", {'event': et, 'cust': customer})

    @http.route(['/event_booking/form/submit'], type='http', auth="public", website=True)
    def event_form_submit(self, **post):
        print(post)
        event = request.env['event.booking'].sudo().create({
            'event_type': int(post.get('event')),
            'cust_name': int(post.get('partner')),
            'booking_date': post.get('booking_date'),
            'start_date': fields.datetime.strptime(post.get('start_date'), '%Y-%m-%dT%H:%M'),
            'end_date': fields.datetime.strptime(post.get('end_date'), '%Y-%m-%dT%H:%M')
        })
        vals = {
            'event': event
        }
        return request.render("event_management.success", vals)
