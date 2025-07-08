from  odoo import models,fields


class PropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Property Tag'
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Property tag name must be unique.')
    ]
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
