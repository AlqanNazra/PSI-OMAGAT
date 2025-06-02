from odoo import models

class PosProduct(models.Model):
    _inherit = 'product.product'

    def _get_fields(self):
        fields = super(PosProduct, self)._get_fields()
        fields.update({
            'is_book': None,
            'author': None,
            'publisher': None,
            'genre': None,
            'age': None,
        })
        return fields