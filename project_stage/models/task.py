from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = "project.task"
    sequence_no = fields.Integer(string='Sequence Number')

    @api.onchange('sequence_no')
    def onchange_sequence_stage(self):
        sequence = self.search([('project_id', '=', self.project_id.id)])
        for rec in sequence:
            if rec.sequence_no == self.sequence_no:
                raise ValidationError("Should be unique")

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        tasks = self.search([('project_id', '=', self.project_id.id)])
        for task in self:
            if task.stage_id.name == 'done':
                next_task = task.search([('sequence_no', '>', task.sequence_no), ('project_id', '=', task.project_id.id)],
                                        order='sequence_no', limit=1)
                next_task.write({'stage_id': task.stage_id.id - 1})
            else:
                for rec in tasks:
                    if rec.stage_id == task.stage_id and rec.stage_id.sequence > 0:
                        raise ValidationError("Already a task exist.")
