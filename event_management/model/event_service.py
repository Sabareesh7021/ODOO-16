from odoo import models, fields


class EventService(models.Model):
    _name = "event_service"
    _description = "Event Service"
    Service = fields.Char()
