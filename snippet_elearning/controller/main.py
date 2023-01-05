from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route(['/elearning_snippet'], type="json", auth="public")
    def elearning_snippet(self):
        elearning = request.env['slide.channel'].sudo().search_read([('website_published', '=', True)], ['name', 'image_1920', 'id', 'description'], order='create_date desc')
        return elearning
