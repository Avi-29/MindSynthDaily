from odoo import models,fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'real.estate.property',
        'seller_id',
        string='Available Properties'
    )