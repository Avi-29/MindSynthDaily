from odoo import models, fields,api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class PropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float(string='Offer Price', required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('real.estate.property', string='Property', required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        string="Property Type"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price', 0)

            property_rec = self.env['real.estate.property'].browse(property_id)

            if property_rec.offer_ids and price <= max(property_rec.offer_ids.mapped('price')):
                raise ValidationError("Offer price must be higher than existing offers.")

            if property_rec.state not in ['offer_accepted', 'sold']:
                property_rec.state = 'offer_received'

        return super().create(vals_list)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for rec in self:
            create_dt = rec.create_date or fields.Datetime.now()
            rec.date_deadline = create_dt.date() + timedelta(days=rec.validity)

    def _inverse_deadline(self):
        for rec in self:
            create_dt = rec.create_date or fields.Datetime.now()
            if rec.date_deadline:
                rec.validity = (rec.date_deadline - create_dt.date()).days

    def action_accept_offer(self):
        for rec in self:
            # Mark all other offers as refused
            all_offers = self.env['real.estate.property.offer'].search([('property_id', '=', rec.property_id.id)])
            all_offers.write({'status': 'refused'})

            rec.status = 'accepted'
            rec.property_id.state = 'offer_accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer_id = rec.partner_id

    def action_refuse_offer(self):
        for rec in self:
            rec.status = 'refused'

    @api.constrains('price')
    def _check_offer_price(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError("Offer price must be strictly positive.")