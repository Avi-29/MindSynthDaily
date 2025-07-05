from odoo import models, fields

class Property(models.Model):
    _name = 'real.estate.property'
    _description = 'Property'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    area = fields.Float(string='Area (sq ft)')
    price = fields.Float(string='Price')
    address = fields.Char(string='Address')
    available_from = fields.Date(string='Available From')
    is_available = fields.Boolean(string='Available', default=True)

