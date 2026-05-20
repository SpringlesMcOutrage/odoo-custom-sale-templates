# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
import base64

_logger = logging.getLogger(__name__)


class CustomTemplate(models.Model):
    _name = 'custom.template'
    _description = 'Custom Template'
    _order = 'name'

    name = fields.Char('Template Name', required=True)
    model_name = fields.Selection([
        ('sale.order', 'Quotation / Sale Order'),
        ('account.move', 'Invoice')
    ], string='Model', required=True, default='sale.order')

    template_type = fields.Selection([
        ('qweb', 'QWeb (HTML/PDF)'),
        ('odt', 'ODT (py3o)')
    ], string='Template Type', required=True, default='qweb')

    template_view_id = fields.Many2one('ir.ui.view', string='Template View', ondelete='cascade', readonly=True,
                                       copy=False)
    qweb_code = fields.Text('QWeb Code', default="""<t t-call="web.external_layout">
    <div class="page">
        <h2>Document</h2>
        <p><strong>Number:</strong> <span t-field="doc.name"/></p>
        <p><strong>Date:</strong> <span t-field="doc.date_order" t-if="doc._name == 'sale.order'"/></p>
        <p><strong>Date:</strong> <span t-field="doc.invoice_date" t-if="doc._name == 'account.move'"/></p>
        <p><strong>Customer:</strong> <span t-field="doc.partner_id.name"/></p>

        <table class="table table-sm mt-4">
            <thead>
                <tr>
                    <th>Product / Description</th>
                    <th class="text-end">Quantity</th>
                    <th class="text-end">Price</th>
                    <th class="text-end">Amount</th>
                </tr>
            </thead>
            <tbody>
                <t t-if="doc._name == 'sale.order'">
                    <t t-foreach="doc.order_line" t-as="line">
                        <tr>
                            <td><span t-field="line.product_id.name"/></td>
                            <td class="text-end"><span t-field="line.product_uom_qty"/></td>
                            <td class="text-end"><span t-field="line.price_unit"/></td>
                            <td class="text-end"><span t-field="line.price_subtotal"/></td>
                        </tr>
                    </t>
                </t>
                <t t-if="doc._name == 'account.move'">
                    <t t-foreach="doc.invoice_line_ids" t-as="line">
                        <tr>
                            <td><span t-field="line.name"/></td>
                            <td class="text-end"><span t-field="line.quantity"/></td>
                            <td class="text-end"><span t-field="line.price_unit"/></td>
                            <td class="text-end"><span t-field="line.price_subtotal"/></td>
                        </tr>
                    </t>
                </t>
            </tbody>
        </table>

        <div class="row mt-4">
            <div class="col-6"/>
            <div class="col-6">
                <table class="table table-sm">
                    <tr>
                        <td><strong>Total:</strong></td>
                        <td class="text-end"><span t-field="doc.amount_total"/></td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</t>""")
    report_action_id = fields.Many2one('ir.actions.report', string='Report Action', ondelete='cascade', readonly=True,
                                       copy=False)
    odt_file = fields.Binary('ODT File', attachment=True)
    odt_filename = fields.Char('ODT Filename')

    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')

    @api.onchange('template_type')
    def _onchange_template_type(self):
        if self.template_type == 'qweb':
            self.odt_file = False
            self.odt_filename = False
        elif self.template_type == 'odt':
            self.qweb_code = False

    def _get_template_xmlid(self):
        self.ensure_one()
        return f'custom_sale_templates.custom_template_{self.id}'

    def _get_report_xmlid(self):
        self.ensure_one()
        return f'custom_sale_templates.report_action_{self.id}'

    def _sync_qweb_template(self):
        self.ensure_one()
        if self.template_type != 'qweb':
            return

        IrUiView = self.env['ir.ui.view'].sudo()
        IrModelData = self.env['ir.model.data'].sudo()

        template_xmlid = self._get_template_xmlid()
        module = 'custom_sale_templates'
        xml_name = f'custom_template_{self.id}'

        arch = self.qweb_code
        view = IrUiView.search([('key', '=', template_xmlid)], limit=1)

        vals = {
            'name': f'Custom Template: {self.name}',
            'type': 'qweb',
            'key': template_xmlid,
            'arch': arch,
            'mode': 'primary',
        }

        if view:
            view.write(vals)
            self.template_view_id = view.id
        else:
            view = IrUiView.create(vals)
            self.template_view_id = view.id

        ext_id = IrModelData.search([
            ('module', '=', module),
            ('name', '=', xml_name),
        ], limit=1)

        if ext_id:
            if ext_id.res_id != view.id:
                ext_id.write({'res_id': view.id})
        else:
            IrModelData.create({
                'name': xml_name,
                'module': module,
                'model': 'ir.ui.view',
                'res_id': view.id,
                'noupdate': True,
            })

        _logger.info(f"QWeb template synced: {self.name}")

    def _sync_odt_template(self):
        self.ensure_one()
        if self.template_type != 'odt':
            return

        IrActionsReport = self.env['ir.actions.report'].sudo()
        IrModelData = self.env['ir.model.data'].sudo()
        Py3oTemplate = self.env['py3o.template'].sudo()
        IrAttachment = self.env['ir.attachment'].sudo()

        report_xmlid = self._get_report_xmlid()
        module = 'custom_sale_templates'
        xml_name = f'report_action_{self.id}'

        py3o_template = None
        if self.odt_file:
            attachment_name = f'custom_template_{self.id}.odt'
            attachment = IrAttachment.search([
                ('name', '=', attachment_name),
                ('res_model', '=', 'custom.template'),
                ('res_id', '=', self.id),
            ], limit=1)

            if attachment:
                attachment.write({'datas': self.odt_file})
            else:
                attachment = IrAttachment.create({
                    'name': attachment_name,
                    'type': 'binary',
                    'datas': self.odt_file,
                    'res_model': 'custom.template',
                    'res_id': self.id,
                    'mimetype': 'application/vnd.oasis.opendocument.text',
                })

            py3o_template = Py3oTemplate.search([
                ('name', '=', f'Custom Template {self.id}')
            ], limit=1)

            py3o_vals = {
                'name': f'Custom Template {self.id}',
                'py3o_template_data': self.odt_file,
                'filetype': 'odt',
            }

            if py3o_template:
                py3o_template.write(py3o_vals)
            else:
                py3o_template = Py3oTemplate.create(py3o_vals)

        if self.model_name == 'sale.order':
            binding_model = self.env.ref('sale.model_sale_order')
        elif self.model_name == 'account.move':
            binding_model = self.env.ref('account.model_account_move')
        else:
            binding_model = False

        report = IrActionsReport.search([
            ('report_name', '=', f'custom.template.{self.id}')
        ], limit=1)

        vals = {
            'name': self.name,
            'model': self.model_name,
            'report_type': 'py3o',
            'report_name': f'custom.template.{self.id}',
            'report_file': f'custom.template.{self.id}',
            'py3o_filetype': 'pdf',
            'binding_type': 'report',
        }

        if binding_model:
            vals['binding_model_id'] = binding_model.id

        if py3o_template:
            vals['py3o_template_id'] = py3o_template.id

        if report:
            report.write(vals)
            self.report_action_id = report.id
        else:
            report = IrActionsReport.create(vals)
            self.report_action_id = report.id

        ext_id = IrModelData.search([
            ('module', '=', module),
            ('name', '=', xml_name),
        ], limit=1)

        if ext_id:
            if ext_id.res_id != report.id:
                ext_id.write({'res_id': report.id})
        else:
            IrModelData.create({
                'name': xml_name,
                'module': module,
                'model': 'ir.actions.report',
                'res_id': report.id,
                'noupdate': True,
            })

        _logger.info(f"ODT template synced: {self.name}")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            try:
                if record.template_type == 'qweb':
                    record._sync_qweb_template()
                elif record.template_type == 'odt':
                    record._sync_odt_template()
            except Exception as e:
                _logger.error(f"Template sync error for {record.name}: {e}")
        return records

    def write(self, vals):
        result = super().write(vals)
        for record in self:
            try:
                if record.template_type == 'qweb' and any(
                        field in vals for field in ['qweb_code', 'name', 'active', 'template_type', 'model_name']):
                    record._sync_qweb_template()
                elif record.template_type == 'odt' and any(
                        field in vals for field in ['odt_file', 'name', 'active', 'template_type', 'model_name']):
                    record._sync_odt_template()
            except Exception as e:
                _logger.error(f"Template sync error for {record.name}: {e}")
        return result

    def unlink(self):
        IrModelData = self.env['ir.model.data'].sudo()
        IrAttachment = self.env['ir.attachment'].sudo()
        Py3oTemplate = self.env['py3o.template'].sudo()

        for record in self:
            if record.template_view_id:
                ext_id = IrModelData.search([
                    ('model', '=', 'ir.ui.view'),
                    ('res_id', '=', record.template_view_id.id),
                ])
                ext_id.unlink()
                record.template_view_id.unlink()

            if record.report_action_id:
                if record.report_action_id.py3o_template_id:
                    record.report_action_id.py3o_template_id.unlink()

                ext_id = IrModelData.search([
                    ('model', '=', 'ir.actions.report'),
                    ('res_id', '=', record.report_action_id.id),
                ])
                ext_id.unlink()
                record.report_action_id.unlink()

            attachments = IrAttachment.search([
                ('res_model', '=', 'custom.template'),
                ('res_id', '=', record.id),
            ])
            attachments.unlink()

        return super().unlink()