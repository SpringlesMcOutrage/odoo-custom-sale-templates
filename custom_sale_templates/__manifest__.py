# -*- coding: utf-8 -*-
{
    'name': 'Custom Sale Templates (QWeb + Py3o)',
    'version': '18.0.2.0.0',
    'category': 'Sales/Accounting',
    'author': 'deep',
    'website': 'https://github.com/SpringlesMcOutrage',
    'summary': 'Custom QWeb and Py3o templates for quotations, sale orders, and invoices',
    'description': """
Custom Sale Templates (QWeb + Py3o)
====================================
Generate professional PDF documents using fully customizable templates.

Features
--------
* Custom QWeb templates (HTML/PDF) for quotations, sale orders, and invoices
* Custom ODT templates via Py3o engine for advanced document layouts
* Per-document template selection on sale orders and invoices
* Supports Odoo 18 QWeb report engine out of the box

Supported document types
------------------------
* Quotations / Sale Orders (draft, sent, confirmed, done)
* Customer Invoices (account.move)

Template types
--------------
* QWeb — standard Odoo HTML-to-PDF rendering
* ODT (Py3o) — LibreOffice-based rendering for pixel-perfect layouts
    """,
    'depends': [
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_template_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'report/sale_order_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}