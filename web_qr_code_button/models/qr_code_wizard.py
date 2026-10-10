from odoo import api, fields, models
from odoo.tools import BinaryBytes


class QrCodeButtonWizard(models.TransientModel):
    _name = 'qr_code_button.wizard'
    _description = 'Show QR Code'

    res_model = fields.Char(required=True)
    res_id = fields.Integer(required=True)
    record_name = fields.Char(compute='_compute_record_name')
    qr_value = fields.Char(compute='_compute_qr_value')
    qr_image = fields.Binary(compute='_compute_qr_image')

    @api.depends('res_model', 'res_id')
    def _compute_record_name(self):
        for wizard in self:
            name = ''
            if wizard.res_model and wizard.res_id and wizard.res_model in self.env:
                record = self.env[wizard.res_model].browse(wizard.res_id)
                if record.exists():
                    name = record.display_name
            wizard.record_name = name

    @api.depends('res_model', 'res_id')
    def _compute_qr_value(self):
        # Odoo 20 replaced the untyped get_param() with typed accessors
        # (get_str/get_int/get_bool/get_float).
        base_url = self.env['ir.config_parameter'].sudo().get_str('web.base.url', '')
        for wizard in self:
            value = ''
            if wizard.res_model and wizard.res_id:
                config = self.env['qr_code_button.config'].sudo().search(
                    [('model_name', '=', wizard.res_model), ('active', '=', True)], limit=1,
                )
                if config and config.field_name and config.field_name in self.env[wizard.res_model]._fields:
                    record = self.env[wizard.res_model].browse(wizard.res_id)
                    if record.exists():
                        value = record[config.field_name] or ''
                if not value:
                    # Odoo 18 replaced the /web# hash router with the
                    # /odoo/<model>/<id> path form, which is what a scanned
                    # link should open on 20.
                    value = f"{base_url}/odoo/{wizard.res_model}/{wizard.res_id}"
            wizard.qr_value = value

    @api.depends('qr_value')
    def _compute_qr_image(self):
        Report = self.env['ir.actions.report']
        for wizard in self:
            if wizard.qr_value:
                png = Report.barcode('QR', wizard.qr_value, width=300, height=300)
                # Odoo 20 Binary fields hold a BinaryValue carrying the raw
                # bytes; assigning base64 bytes now raises a TypeError.
                wizard.qr_image = BinaryBytes(png, 'qr.png')
            else:
                wizard.qr_image = False

    def action_download(self):
        self.ensure_one()
        filename = f"qr-{self.res_model}-{self.res_id}.png"
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/qr_code_button.wizard/{self.id}/qr_image?download=true&filename={filename}',
            'target': 'self',
        }

    def action_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web_qr_code_button/print/{self.id}',
            'target': 'new',
        }
