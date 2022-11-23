from odoo import models, fields


class EventBooking(models.Model):
    _name = "event_booking"
    _description = "Event Booking"
    Event = fields.Char(required=True)
