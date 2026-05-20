# -*- coding: utf-8 -*-
from odoo import models, fields, api
from markupsafe import Markup
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_template_id = fields.Many2one(
        'custom.template',
        string='Custom Template',
        domain=[('active', '=', True), ('model_name', '=', 'account.move')],
        help='Select a custom template for printing the invoice'
    )

    def render_custom_template_for_report(self):
        self.ensure_one()
        if not self.custom_template_id or not self.custom_template_id.template_view_id:
            return ""

        try:
            html_content = self.env['ir.qweb']._render(
                self.custom_template_id.template_view_id.id,
                {'doc': self}
            )
            return Markup(html_content)
        except Exception as e:
            _logger.error(f"Template render error for invoice {self.name}: {e}")
            return Markup(f'<div style="color: red; padding: 20px;">Template render error: {str(e)}</div>')

    def action_print_custom_template(self):
        self.ensure_one()

        if not self.custom_template_id:
            return self.env.ref('account.account_invoices').report_action(self)

        if self.custom_template_id.template_type == 'qweb':
            return self.env.ref('custom_sale_templates.action_report_account_move_custom').report_action(self)
        elif self.custom_template_id.template_type == 'odt':
            if self.custom_template_id.report_action_id:
                return self.custom_template_id.report_action_id.report_action(self)
            else:
                raise UserWarning('ODT template is not configured correctly')

        return self.env.ref('account.account_invoices').report_action(self)