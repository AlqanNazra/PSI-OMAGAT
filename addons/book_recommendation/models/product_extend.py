# book_recommendation/models/product_extend.py
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean(string="Is a Book", default=False,
                             help="Check if this product is a book.")
    author_id = fields.Many2one('res.partner', string='Author',
                                domain=[('is_company', '=', False), ('parent_id', '=', False)],
                                help="The author of the book. Assumes authors are partners.")