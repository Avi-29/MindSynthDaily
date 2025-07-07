from odoo import models, fields

class PropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Property Type'
    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'Property type name must be unique.')
    ]

    name = fields.Char(required=True)