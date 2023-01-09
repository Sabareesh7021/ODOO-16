from ast import literal_eval

from odoo import models, fields, api


class BomConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    bom_id = fields.Many2many('mrp.bom', string='Bom Product')

    def set_values(self):
        res = super(BomConfigSetting, self).set_values()

        self.env['ir.config_parameter'].sudo().set_param('many2many.bom_id', self.bom_id.ids)
        return res


    @api.model
    def get_values(self):
        res = super(BomConfigSetting, self).get_values()

        with_user = self.env['ir.config_parameter'].sudo()
        params = with_user.get_param('many2many.bom_id')
        res.update(
            bom_id=[(6, 0, literal_eval(params))] if params else False, )
        return res

