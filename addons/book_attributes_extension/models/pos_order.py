from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _compute_discount(self):
        for order in self:
            fantasy_books = 0
            education_books = 0
            lines = order.lines
            for line in lines:
                product = line.product_id.product_tmpl_id
                if product.is_book:
                    if product.genre and product.genre.name == 'Fantasy':
                        fantasy_books += line.qty
                    elif product.genre and product.genre.name == 'Edukasi':
                        education_books += line.qty
            # Diskon 10% untuk 2+ buku Fantasy
            if fantasy_books >= 2:
                for line in lines:
                    if line.product_id.product_tmpl_id.is_book and line.product_id.product_tmpl_id.genre and line.product_id.product_tmpl_id.genre.name == 'Fantasy':
                        line.discount = 10.0
            # Diskon 15% untuk 3+ buku Edukasi
            if education_books >= 3:
                for line in lines:
                    if line.product_id.product_tmpl_id.is_book and line.product_id.product_tmpl_id.genre and line.product_id.product_tmpl_id.genre.name == 'Edukasi':
                        line.discount = 15.0

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        return order_fields

    def _prepare_invoice_vals(self):
        vals = super(PosOrder, self)._prepare_invoice_vals()
        return vals

    def _create_invoice(self):
        invoice = super(PosOrder, self)._create_invoice()
        for line in self.lines:
            if line.product_id.product_tmpl_id.is_book:
                description = f"{line.product_id.name} (Author: {line.product_id.product_tmpl_id.author or 'N/A'}, Publisher: {line.product_id.product_tmpl_id.publisher or 'N/A'}, Genre: {line.product_id.product_tmpl_id.genre.name or 'N/A'}, Age: {line.product_id.product_tmpl_id.age or 'N/A'})"
                invoice_line = invoice.invoice_line_ids.filtered(lambda l: l.product_id == line.product_id)
                if invoice_line:
                    invoice_line.name = description
        return invoice