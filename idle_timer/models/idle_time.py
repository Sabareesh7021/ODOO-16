from odoo import fields, models


class IdleTime(models.Model):
    _inherit = 'survey.survey'
    idle_timer = fields.Float('Idle Time(minutes)')
    idle = fields.Boolean()

