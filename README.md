# Custom Sale Templates (QWeb + Py3o)

> Generate pixel-perfect PDF documents for quotations, sale orders, and invoices using fully customizable QWeb and Py3o templates — all managed directly inside Odoo.

[![Odoo 18](https://img.shields.io/badge/Odoo-18.0-875A7B?style=flat&logo=odoo)](https://odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Version](https://img.shields.io/badge/Version-18.0.2.0.0-green.svg)](https://github.com/SpringlesMcOutrage/odoo-custom-sale-templates)

---

## Overview

**Custom Sale Templates** gives you full control over how your business documents look. Create and manage unlimited QWeb (HTML/PDF) and Py3o (ODT/LibreOffice) templates for quotations, sale orders, and customer invoices — and select the right template per document, not just globally.

No more one-size-fits-all reports. Each customer, contract type, or product line can have its own professional layout.

---

## Features

### Template Management
- **Unlimited templates** — create as many QWeb or Py3o templates as you need
- **Live QWeb editor** — edit template code directly inside Odoo with instant preview
- **ODT upload** — upload `.odt` files (LibreOffice Writer format) for advanced print layouts
- **Per-document selection** — choose a specific template on each sale order or invoice

### Supported Document Types
| Document | QWeb | Py3o (ODT) |
|----------|:----:|:----------:|
| Quotation | ✅ | ✅ |
| Sale Order | ✅ | ✅ |
| Customer Invoice | ✅ | ✅ |

### Template Engines
- **QWeb** — standard Odoo HTML-to-PDF rendering via wkhtmltopdf
- **Py3o** — LibreOffice-based rendering for pixel-perfect, print-ready PDFs from `.odt` files

### Translations
Available in: 🇬🇧 English · 🇺🇦 Ukrainian · 🇩🇪 German · 🇪🇸 Spanish

---

## Requirements

| Dependency | Version |
|-----------|---------|
| Odoo | 18.0 |
| sale_management | included in Odoo |
| account | included in Odoo |
| report_py3o | required for ODT templates |
| LibreOffice | required on server for Py3o rendering |

> **Note:** If you only use QWeb templates, LibreOffice and `report_py3o` are not strictly required. ODT rendering needs both.

---

## Installation

1. Copy the `custom_sale_templates` folder into your Odoo addons directory
2. Restart the Odoo server
3. Go to **Settings → Apps**, click **Update Apps List**
4. Search for **Custom Sale Templates** and click **Install**

---

## Usage

### Creating a Template

1. Navigate to **Sales → Configuration → Custom Templates**
2. Click **New**
3. Select **Model** (Sale Order or Invoice) and **Template Type** (QWeb or ODT)
4. For QWeb — edit the template code inline
5. For ODT — upload your `.odt` file
6. Save — the template is registered automatically as a report action

### Using a Template on a Document

1. Open any quotation, sale order, or invoice
2. Find the **Custom Template** field in the document header
3. Select your template from the dropdown
4. Click **Print** — the document renders using the selected template

---

## Project Structure

```
custom_sale_templates/
├── models/
│   ├── custom_template.py      # Core template model, QWeb/Py3o sync logic
│   ├── sale_order.py           # Sale order extension (template field)
│   ├── account_move.py         # Invoice extension (template field)
│   └── py3o_parser.py          # Py3o rendering helpers
├── views/
│   ├── custom_template_views.xml
│   ├── sale_order_views.xml
│   └── account_move_views.xml
├── report/
│   └── sale_order_report.xml
├── security/
│   └── ir.model.access.csv
└── i18n/
    ├── uk.po
    ├── de.po
    └── es.po
```

---

## License

[LGPL-3](https://www.gnu.org/licenses/lgpl-3.0) © [deep](https://github.com/SpringlesMcOutrage)
