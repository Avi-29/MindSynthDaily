from odoo import models, fields ,api

class PropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Property Type'
    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'Property type name must be unique.')
    ]
    _order = "sequence, name"

    name = fields.Char(string="Property Type",required=True)
    property_ids = fields.One2many('real.estate.property', 'property_type_id', string="Properties")
    sequence=fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('real.estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)