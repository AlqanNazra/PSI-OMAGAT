# book_recommendation/models/book_recommendation.py
from odoo import models, fields, api

class BookRecommendation(models.Model):
    _name = 'book.recommendation'
    _description = 'Book Recommendation Results'
    _order = 'rank asc' # Mengurutkan berdasarkan peringkat

    name = fields.Char(string='Item Name', required=True)
    type = fields.Selection([
        ('book', 'Book'),
        ('genre', 'Genre'),
        ('author', 'Author'),
    ], string='Type', required=True)
    sales_count = fields.Integer(string='Sales Count', help="Total quantity sold or frequency.")
    rank = fields.Integer(string='Rank', help="Ranking based on sales count.")

    # Jika Anda ingin menyimpan referensi ke objek sebenarnya (misalnya, produk, penulis), Anda bisa menambahkannya
    # product_id = fields.Many2one('product.product', string='Product', ondelete='cascade')
    # author_id = fields.Many2one('res.partner', string='Author', ondelete='cascade') # Asumsi penulis adalah res.partner

    # _sql_constraints = [
    #     ('name_type_unique', 'UNIQUE(name, type)', 'The combination of item name and type must be unique!'),
    # ]