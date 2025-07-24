from odoo import http
from odoo.http import request
from odoo.addons.restful.controllers.main import validate_token

class CustomAPI(http.Controller):

    @validate_token
    @http.route('/api/real_estate/create', type='json', auth='none', methods=['POST'], csrf=False)
    def create(self, **kwargs):
        try:
            name = kwargs.get('name')
            description = kwargs.get('description')

            if not name:
                return {'error': 'Missing required field: name'}, 400
            record = request.env['real.estate.property'].sudo().create({
                'name': name,
                'description': description
            })

            return {
                'status': 'success',
                'id': record.id,
                'name': record.name
            }, 201

        except Exception as e:
            return {'error': str(e)}, 500

    @validate_token
    @http.route('/api/real_estate/<int:record_id>', type='json', auth='none', methods=['GET'], csrf=False)
    def read(self, record_id):
        try:
            rec = request.env['real.estate.property'].sudo().browse(record_id)
            if not rec.exists():
                return {'error': 'Record not found'}, 404

            return {
                'id': rec.id,
                'name': rec.name,
                'description': rec.description
            }, 200

        except Exception as e:
            return {'error': str(e)}, 500

    @validate_token
    @http.route('/api/real_estate', type='json', auth='none', methods=['GET'], csrf=False)
    def read_all(self):
        try:
            records = request.env['real.estate.property'].sudo().search([])
            return [
                {'id': rec.id, 'name': rec.name, 'description': rec.description}
                for rec in records
            ], 200

        except Exception as e:
            return {'error': str(e)}, 500

    @validate_token
    @http.route('/api/real_estate/<int:record_id>', type='json', auth='none', methods=['PUT'], csrf=False)
    def update(self, record_id, **kwargs):
        try:
            record = request.env['real.estate.property'].sudo().browse(record_id)
            if not record.exists():
                return {'error': 'Record not found'}, 404

            record.write({
                'name': kwargs.get('name', record.name),
                'description': kwargs.get('description', record.description),
            })
            return {'success': True}, 200

        except Exception as e:
            return {'error': str(e)}, 500

    @validate_token
    @http.route('/api/real_estate/<int:record_id>', type='json', auth='none', methods=['DELETE'], csrf=False)
    def delete(self, record_id):
        try:
            record = request.env['real.estate.property'].sudo().browse(record_id)
            if not record.exists():
                return {'error': 'Record not found'}, 404

            record.unlink()
            return {'success': True}, 204

        except Exception as e:
            return {'error': str(e)}, 500
