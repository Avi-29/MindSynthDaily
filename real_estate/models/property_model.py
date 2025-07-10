from odoo import models, fields ,api
from odoo.exceptions import UserError,ValidationError

class Property(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    image = fields.Image(string="Property Image")
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Float(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Float(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )
    property_type_id = fields.Many2one('real.estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('real.estate.property.offer', 'property_id', string='Offers')
    property_tag = fields.Many2many('real.estate.property.tag',string='tags')
    is_available = fields.Boolean(string='Available', default=True)
    signature = fields.Char(string='Sign')
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, default='new')

    def unlink(self):
        for rec in self:
            if rec.state not in ['new', 'cancelled']:
                raise UserError("Only properties in state 'New' or 'Cancelled' can be deleted.")
        return super().unlink()

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            prices = rec.offer_ids.mapped('price')
            rec.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10.0
                rec.garden_orientation = 'north'
            else:
                rec.garden_area = 0.0
                rec.garden_orientation = False

    def action_mark_sold(self):
        for rec in self:
            if rec.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            accepted_offer = rec.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if not accepted_offer:
                raise UserError("You must accept an offer before selling the property.")
            rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            rec.state = 'cancelled'

    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError("Expected price must be strictly positive.")
            if rec.selling_price and rec.selling_price <= 0:
                raise ValidationError("Selling price must be positive.")
            if rec.selling_price and rec.selling_price < rec.expected_price * 0.9:
                raise ValidationError("Selling price cannot be lower than 90% of expected price.")


