from odoo import api, fields, models, _

SERVER_ACTION_CODE = (
    "action = {\n"
    "    'type': 'ir.actions.act_window',\n"
    "    'name': 'QR Code',\n"
    "    'res_model': 'qr_code_button.wizard',\n"
    "    'view_mode': 'form',\n"
    "    'target': 'new',\n"
    "    'context': {\n"
    "        'default_res_model': model._name,\n"
    "        'default_res_id': records[:1].id,\n"
    "    },\n"
    "}\n"
)


class QrCodeButtonConfig(models.Model):
    _name = 'qr_code_button.config'
    _description = 'QR Code Button Configuration'

    name = fields.Char(compute='_compute_name', store=True)
    model_id = fields.Many2one(
        'ir.model', string='Model', required=True, ondelete='cascade',
        domain=[('transient', '=', False)],
    )
    model_name = fields.Char(string='Model (technical name)', related='model_id.model', store=True, readonly=True)
    field_id = fields.Many2one(
        'ir.model.fields', string='Encoded field', ondelete='cascade',
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['char', 'text']), ('store', '=', True)]",
        help="Field whose value is encoded in the QR code (e.g. a serial number or reference). "
             "Leave empty to encode a link back to the record instead.",
    )
    field_name = fields.Char(related='field_id.name', store=True, readonly=True)
    active = fields.Boolean(default=True)
    server_action_id = fields.Many2one('ir.actions.server', readonly=True, copy=False, ondelete='set null')

    _model_uniq = models.Constraint('unique(model_id)', "Only one QR Code setup per model.")

    @api.depends('model_id.name', 'field_id.field_description')
    def _compute_name(self):
        for config in self:
            if config.model_id and config.field_id:
                config.name = _("%(model)s (%(field)s)", model=config.model_id.name, field=config.field_id.field_description)
            elif config.model_id:
                config.name = _("%(model)s (record link)", model=config.model_id.name)
            else:
                config.name = _("New QR Code Setup")

    def _get_or_create_server_action(self):
        self.ensure_one()
        # ir.actions.server has no `active` field: an inactive rule instead
        # clears `binding_model_id`, which removes the action from the
        # model's Actions menu without deleting the action record itself.
        vals = {
            'name': _('Show QR Code'),
            'model_id': self.model_id.id,
            'binding_model_id': self.model_id.id if self.active else False,
            'binding_type': 'action',
            'binding_view_types': 'form',
            'state': 'code',
            'code': SERVER_ACTION_CODE,
        }
        action = self.server_action_id
        if action:
            action.sudo().write(vals)
        else:
            action = self.env['ir.actions.server'].sudo().create(vals)
            self.server_action_id = action.id
        return action

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._get_or_create_server_action()
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            record._get_or_create_server_action()
        return res

    def unlink(self):
        actions = self.server_action_id
        res = super().unlink()
        actions.sudo().unlink()
        return res
