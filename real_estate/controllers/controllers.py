# controllers/my_model_api.py
from odoo import http
from odoo.http import request
import json

class CustomAPI(http.Controller):

    @http.route('/api/real_estate/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create(self, **kwargs):
        name = kwargs.get('name')  # from params.name
        description = kwargs.get('description')

        record = request.env['real.estate.property'].sudo().create({
            'name': name,
            'description': description
        })

        return {
            'status': 'success',
            'id': record.id,
            'name': record.name
        }

    @http.route('/api/real_estate/<int:record_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def read(self,record_id,):
        rec = request.env['real.estate.property'].sudo().browse(record_id)
        return {'id': rec.id, 'name': rec.name, 'description': rec.description}



    # READ (GET all)
    @http.route('/api/real_estate', type='json', auth='public', methods=['GET'], csrf=False)
    def read_all(self):
        records = request.env['real.estate.property'].sudo().search([])
        return [
            {'id': rec.id, 'name': rec.name, 'description': rec.description}
            for rec in records
        ]

    # UPDATE (PUT)
    @http.route('/api/real_estate/<int:record_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update(self, record_id, **kwargs):
        record = request.env['real.estate.property'].sudo().browse(record_id)
        if not record.exists():
            return {'error': 'Record not found'}
        record.write({
            'name': kwargs.get('name', record.name),
            'description': kwargs.get('description', record.description),
        })
        return {'success': True}

    # DELETE (DELETE)
    @http.route('/api/real_estate/<int:record_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete(self, record_id):
        record = request.env['real.estate.property'].sudo().browse(record_id)
        if not record.exists():
            return {'error': 'Record not found'}
        record.unlink()
        return {'success': True}
