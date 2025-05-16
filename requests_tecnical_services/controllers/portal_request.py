from odoo import http
from odoo.http import request, Response
import json

class PortalRequest(http.Controller):

    @http.route(['/request-service'], type='http', auth='public', website=True)
    def render_request_form(self, **kwargs):
        partners = request.env['res.partner'].sudo().search_read(
            fields=['id', 'name', 'email'])
        return request.render('requests_tecnical_services.template_request_form', {
            'partners': partners,
        })
        
    @http.route('/get-partners', type='http', auth="public", methods=['GET'], website=True)
    def get_partners(self, **kw):
        partners = request.env['res.partner'].sudo().search_read(
            fields=['id', 'name', 'email'],
        )
        return Response(json.dumps(partners), headers=[('Content-Type', 'application/json')])
        
    @http.route('/equipments', type='http', auth='public', methods=['GET'], website=True)
    def get_equipment_list(self, **kw):
        equipments = ['Laptop', 'Router', 'Printer', 'Server']
        return Response(json.dumps(equipments), headers={'Content-Type': 'application/json'})

    @http.route(['/request-service/submit'], type='http', auth='public', website=True, methods=['POST'])
    def submit_request(self, **post):
        customer_id = int(post.get('customer_id', 0))
        equipment = post.get('equipment')
        problem = post.get('problem_description')
        priority = post.get('priority')

        request.env['technical.service.request'].sudo().create({
            'customer_id': customer_id,
            'equipment': equipment,
            'problem_description': problem,
            'priority': priority,
            'state': 'draft'
        })
        return request.render('requests_tecnical_services.template_request_thank_you')
