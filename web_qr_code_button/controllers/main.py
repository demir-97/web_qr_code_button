from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class QrCodeButtonController(http.Controller):

    @http.route('/web_qr_code_button/print/<int:wizard_id>', type='http', auth='user')
    def print_qr_code(self, wizard_id, **kwargs):
        wizard = request.env['qr_code_button.wizard'].browse(wizard_id).exists()
        if not wizard or not wizard.qr_image:
            raise NotFound()
        return request.render('web_qr_code_button.qr_code_print_page', {
            'record_name': wizard.record_name,
            'qr_image': wizard.qr_image.decode('ascii'),
        })
