from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = 'real.estate.property'

    def action_mark_sold(self):
        for property in self:
            if not property.buyer_id:
                raise ValidationError("Any Offer is not being accepted")

            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': '6% Commission',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    })
                ],
            }

            self.env['account.move'].create(invoice_vals)

        return super().action_mark_sold()
