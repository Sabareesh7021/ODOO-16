from odoo import fields, models


class EventType(models.Model):
    _name = "event_type"
    _description = "Event Type"
    Event_Type = fields.Char('Event type', required=True)
    Code = fields.Integer()
    Image = fields.Image()
