from odoo import http
from odoo.http import request, Response
import json

class TechnicalServiceApiController(http.Controller):

    # Autenticación por token
    def _authenticate(self, token):
        if not request.env['api.auth.token'].is_valid_token(token):
            return Response(
                json.dumps({'error': 'Token inválido o inactivo'}),
                status=401,
                headers=[('Content-Type', 'application/json')]
            )
        return None

   
    @http.route('/api/technical-requests', type='http', auth='none', methods=['GET'], csrf=False)
    def get_technical_requests(self, **kwargs):
        # 1. Verificar token
        token = kwargs.get('token') or request.httprequest.headers.get('Authorization')
        auth_error = self._authenticate(token)
        if auth_error:
            return auth_error

        domain = []
        if kwargs.get('state'):
            domain.append(('state', '=', kwargs['state']))
        if kwargs.get('priority'):
            domain.append(('priority', '=', kwargs['priority']))

        requests = request.env['technical.service.request'].sudo().search_read(
            domain=domain,
            fields=['name', 'customer_id', 'equipment', 'priority', 'state', 'date_requested']
        )

        return Response(
            json.dumps(requests),
            status=200,
            headers=[('Content-Type', 'application/json')]
        )