from odoo import fields, models, api, _


class Company(models.Model):
    _inherit = 'res.company'

    map_provider_id = fields.Many2one(comodel_name='base.geo_provider', gruoup='base.group_no_one')
