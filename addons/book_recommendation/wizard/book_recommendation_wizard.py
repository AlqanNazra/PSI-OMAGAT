# book_recommendation/wizard/book_recommendation_wizard.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict

class BookRecommendationWizard(models.TransientModel):
    _name = 'book.recommendation.wizard'
    _description = 'Generate Book Recommendations Wizard'

    limit_recommendations = fields.Integer(
        string='Number of Recommendations',
        default=10,
        help="Number of top items to display for each category (book, genre, author)."
    )

    def generate_recommendations(self):
        """
        Generates and updates book, genre, and author recommendations based on sales data.
        """
        self.ensure_one()

        # Hapus semua rekomendasi yang ada sebelumnya
        self.env['book.recommendation'].search([]).unlink()

        # Hitung frekuensi penjualan untuk buku, genre, dan penulis
        top_books = defaultdict(int)
        top_genres = defaultdict(int)
        top_authors = defaultdict(int)

        # Cari semua sale order lines yang sudah dikonfirmasi
        sale_lines = self.env['sale.order.line'].search([
            ('state', 'in', ['sale', 'done']), # Hanya order yang sudah dikonfirmasi/selesai
            ('product_id.is_book', '=', True) # Asumsi ada field is_book di product.template/product.product
        ])

        if not sale_lines:
            raise UserError(_("No sales data found for books. Please ensure you have book products and confirmed sales orders."))

        for line in sale_lines:
            product = line.product_id
            quantity = line.product_uom_qty

            # Rekomendasi Buku
            top_books[product.name] += quantity

            # Rekomendasi Genre (asumsi product.category sebagai genre)
            if product.categ_id:
                top_genres[product.categ_id.name] += quantity

            # Rekomendasi Penulis (asumsi product.template.author_id yang mengacu ke res.partner)
            # Anda perlu memastikan field author_id ada di product.template dan relevan untuk buku
            if product.product_tmpl_id and hasattr(product.product_tmpl_id, 'author_id') and product.product_tmpl_id.author_id:
                top_authors[product.product_tmpl_id.author_id.name] += quantity
            # Alternatif jika penulis disimpan sebagai Char:
            # if product.product_tmpl_id and hasattr(product.product_tmpl_id, 'author_name') and product.product_tmpl_id.author_name:
            #     top_authors[product.product_tmpl_id.author_name] += quantity

        # Urutkan dan simpan ke model book.recommendation
        self._create_recommendations(top_books, 'book', self.limit_recommendations)
        self._create_recommendations(top_genres, 'genre', self.limit_recommendations)
        self._create_recommendations(top_authors, 'author', self.limit_recommendations)

        # Tampilkan hasil setelah proses selesai
        return {
            'name': _("Book Recommendations"),
            'type': 'ir.actions.act_window',
            'res_model': 'book.recommendation',
            'view_mode': 'tree,form',
            'domain': [], # Tampilkan semua rekomendasi
            'target': 'current',
        }

    def _create_recommendations(self, data, rec_type, limit):
        """ Helper method to create records in book.recommendation model. """
        sorted_items = sorted(data.items(), key=lambda item: item[1], reverse=True)[:limit]
        for rank, (item_name, sales_count) in enumerate(sorted_items, 1):
            self.env['book.recommendation'].create({
                'name': item_name,
                'type': rec_type,
                'sales_count': sales_count,
                'rank': rank,
            })