from odoo import models, fields, api
from collections import Counter

class BookRecommendation(models.Model):
    _name = 'book.recommendation'
    _description = 'Book Recommendation Results'
    _order = 'rank asc'  # Mengurutkan berdasarkan peringkat

    name = fields.Char(string='Item Name', required=True)
    type = fields.Selection([
        ('book', 'Book'),
        ('genre', 'Genre'),
        ('author', 'Author'),
    ], string='Type', required=True)
    sales_count = fields.Integer(string='Sales Count', help="Total quantity sold or frequency.")
    rank = fields.Integer(string='Rank', help="Ranking based on sales count.", compute='_compute_rank', store=True)

    @api.depends('sales_count')
    def _compute_rank(self):
        for rec in self:
            # Ambil semua rekomendasi yang ada dan urutkan berdasarkan sales_count
            recommendations = self.search([], order='sales_count desc')
            rec.rank = recommendations.ids.index(rec.id) + 1 if rec in recommendations else 0

    @api.model
    def generate_recommendations(self, limit=5):
        # Hapus data lama
        self.search([]).unlink()

        # Ambil data penjualan dari sale.order.line
        sale_lines = self.env['sale.order.line'].search([
            ('order_id.state', 'in', ['sale', 'done'])
        ])

        # Hitung frekuensi untuk buku, genre, dan penulis
        book_counter = Counter()
        genre_counter = Counter()
        author_counter = Counter()

        for line in sale_lines:
            product = line.product_id.product_tmpl_id
            qty = line.product_uom_qty
            genre = product.genre_id.name if product.genre_id else 'Unknown'
            author = product.author_id.name if product.author_id else 'Unknown'
            book_counter[product.name] += qty
            genre_counter[genre] += qty
            author_counter[author] += qty

        # Buat entri untuk top books
        for name, count in book_counter.most_common(limit):
            self.create({'name': name, 'type': 'book', 'sales_count': count})
        # Buat entri untuk top genres
        for name, count in genre_counter.most_common(limit):
            self.create({'name': name, 'type': 'genre', 'sales_count': count})
        # Buat entri untuk top authors
        for name, count in author_counter.most_common(limit):
            self.create({'name': name, 'type': 'author', 'sales_count': count})

    # Pastikan file ini diimpor di models/__init__.py
    # Tambahkan di models/__init__.py:
    # from . import book_recommendation