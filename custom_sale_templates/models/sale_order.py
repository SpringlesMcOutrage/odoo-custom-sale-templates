# -*- coding: utf-8 -*-
from odoo import models, fields, api
from markupsafe import Markup
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_template_id = fields.Many2one(
        'custom.template',
        string='Custom Template',
        domain=[('active', '=', True), ('model_name', '=', 'sale.order')],
        help='Select a custom template for printing'
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
            _logger.error(f"Template render error for report {self.name}: {e}")
            return Markup(f'<div style="color: red; padding: 20px;">Template render error: {str(e)}</div>')

    def action_print_custom_template(self):
        self.ensure_one()

        if not self.custom_template_id:
            # Вибір стандартного звіту залежно від стану
            if self.state in ['draft', 'sent']:
                return self.env.ref('sale.action_report_saleorder').report_action(self)
            else:
                return self.env.ref('sale.action_report_saleorder').report_action(self)

        if self.custom_template_id.template_type == 'qweb':
            return self.env.ref('custom_sale_templates.action_report_sale_order_custom').report_action(self)
        elif self.custom_template_id.template_type == 'odt':
            if self.custom_template_id.report_action_id:
                return self.custom_template_id.report_action_id.report_action(self)
            else:
                raise UserWarning('ODT template is not configured correctly')

        return self.env.ref('sale.action_report_saleorder').report_action(self)