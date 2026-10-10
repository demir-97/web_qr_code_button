{
    'name': 'QR Code Button | Print & Share a QR Code From Any Record',
    'version': '17.0.1.0.1',
    'category': 'Productivity',
    'author': 'Meisanqo',
    'support': 'meisanqo@outlook.com',
    'summary': "Generate a QR code for any record in two clicks: switch the model on in Settings and a \"Show QR Code\" action appears in the Actions menu of every record. The QR code encodes a link back to the record, or the value of a Char or Text field you choose, ready for asset labels, product tags and warehouse bins. Print QR code labels straight from the browser or download the QR code as a PNG image. Built on Odoo's own barcode engine: no external service is called and nothing leaves your server.",
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
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/qr_code_config_views.xml',
        'views/qr_code_print_templates.xml',
        'views/qr_code_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
