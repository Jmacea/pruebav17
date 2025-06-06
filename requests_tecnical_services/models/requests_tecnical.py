from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TechnicalServiceRequest(models.Model):
    _name = 'technical.service.request'
    _description = 'Technical Service Request'

    name = fields.Char(string='Request Number', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    equipment = fields.Char(string='Equipment', required=True)
    problem_description = fields.Text(string='Problem Description', required=True)

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='State', default='draft', tracking=True)

    assigned_user_id = fields.Many2one('res.users', string='Assigned Technician')

    date_requested = fields.Date(string='Date Requested', default=fields.Date.context_today)
    date_completed = fields.Date(string='Date Completed')


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('technical.service.request') or _('New')
        return super().create(vals)

    @api.constrains('date_requested', 'date_completed')
    def _check_dates(self):
        for record in self:
            if record.date_completed and record.date_requested and record.date_completed < record.date_requested:
                raise ValidationError(_('The completion date must be after the requested date.'))

    def write(self, vals):
        for rec in self:
            new_state = vals.get('state') or rec.state
            assigned_user = vals.get('assigned_user_id') or rec.assigned_user_id.id
            if new_state == 'done' and not assigned_user:
                raise ValidationError(_('You cannot close a request without assigning a technician.'))
        return super().write(vals)

    def action_start_process(self):
        self.ensure_one()
        self.state = 'in_process'

    def action_mark_done(self):
        self.ensure_one()
        if not self.assigned_user_id:
            raise ValidationError(_('A technician must be assigned before completing the request.'))
        self.state = 'done'
        self.date_completed = fields.Date.context_today(self)

    def action_cancel(self):
        self.ensure_one()
        self.state = 'canceled'

    def action_reset_to_draft(self):
        self.ensure_one()
        self.state = 'draft'
        self.date_completed = False
        
    def action_send_email(self):
        self.ensure_one()
        template_id = self.env.ref('requests_tecnical_services.email_template_tech_request').id	
        return {
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'target': 'new',
			'context': {
				'default_model': 'technical.service.request',
				'default_res_id': self.id,
				'default_use_template': bool(template_id),
				'default_template_id': template_id,
				'default_composition_mode': 'comment',
				'default_email_layout_xmlid': 'mail.mail_notification_light',
			},
		}
    
        


class ApiAuthToken(models.Model):
    _name = 'api.auth.token'
    _description = 'Tokens de API'

    name = fields.Char(string='Nombre del Cliente', required=True)
    token = fields.Char(string='Token', required=True, copy=False)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('token_unique', 'UNIQUE(token)', 'El token debe ser único.'),
    ]

    @api.model
    def is_valid_token(self, token):
        return bool(self.search([('token', '=', token), ('active', '=', True)]))