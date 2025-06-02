from odoo import fields, models, api
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _update_available_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, in_date=None):
        res = super(StockQuant, self)._update_available_quantity(product_id, location_id, quantity, lot_id, package_id, owner_id, in_date)
        quants = self.search([('product_id', '=', product_id.id), ('location_id', '=', location_id.id)])
        total_qty = sum(quant.quantity for quant in quants)
        if product_id.is_book and total_qty < 5:
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model'].search([('model', '=', 'product.product')]).id,
                'res_id': product_id.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
                'summary': f"Low Stock Alert for Book: {product_id.name}",
                'note': f"Stock for {product_id.name} is below 5 units. Current stock: {total_qty}.",
                'user_id': self.env.user.id,
            })
        return res