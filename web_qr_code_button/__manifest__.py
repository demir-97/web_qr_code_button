{
    'name': 'QR Code Button | Print & Share a QR Code From Any Record',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'author': 'Meisanqo',
    'support': 'meisanqo@outlook.com',
    'summary': 'Add a "Show QR Code" action to any record, from Settings.',
    'description': """
QR Code Button
================

Generate a QR code for any record in two clicks, from a menu you turn on
yourself — no code, no report template to design.

Getting started
----------------

Settings > Technical > QR Code Button: pick a model and save. A
"Show QR Code" action now appears in the gear (Actions) menu of every
record of that model.

What's in the QR code
-----------------------

- By default, the QR code encodes a link back to the record — scan it and
  the record opens.
- Optionally pick a Char/Text field on the model (a serial number,
  reference, asset tag, ...): the QR code then encodes that value instead,
  ready for asset labels, product tags or warehouse bins.

The QR code is generated on the fly from Odoo's own barcode engine (used
for invoices' QR payment codes) — no external service, nothing leaves
your server. The popup shows the code full-size, ready to right-click and
save, or print from the browser.
""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/qr_code_config_views.xml',
        'views/qr_code_print_templates.xml',
        'views/qr_code_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'price': 9.0,
    'currency': 'USD',
}
