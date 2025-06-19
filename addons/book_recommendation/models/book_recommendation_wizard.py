from odoo import models, fields

class BookRecommendationWizard(models.TransientModel):
    _name = 'book.recommendation.wizard'
    _description = 'Generate Book Recommendations'

    limit_recommendations = fields.Integer(string='Limit Recommendations', default=5)

    def generate_recommendations(self):
        self.env['book.recommendation'].generate_recommendations(self.limit_recommendations)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'book.recommendation',
            'view_mode': 'tree,form',
            'target': 'current',
        }