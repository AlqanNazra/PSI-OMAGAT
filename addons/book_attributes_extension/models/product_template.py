from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean(string="Is a Book", default=False)
    author = fields.Char(string="Author")
    publisher = fields.Char(string="Publisher")
    genre = fields.Many2one('book.genre', string="Genre")
    age = fields.Selection(
        selection=[
            ('children', 'Anak-anak'),
            ('teen', 'Remaja'),
            ('adult', 'Dewasa'),
        ],
        string="Recommended Age",
        default='adult',
    )