from odoo import fields, models

class BookGenre(models.Model):
    _name = 'book.genre'
    _description = 'Book Genre'

    name = fields.Char(string="Genre Name", required=True)

class BookBundle(models.Model):
    _name = 'book.bundle'
    _description = 'Book Bundle'

    name = fields.Char(string="Bundle Name", required=True)
    product_ids = fields.Many2many('product.product', string="Books")
    genre_id = fields.Many2one('book.genre', string="Genre")
    discount = fields.Float(string="Discount (%)")