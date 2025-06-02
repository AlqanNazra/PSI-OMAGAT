# book_recommendation/__manifest__.py
{
    'name': "Book Recommendation",
    'summary': """
        Module to provide book, genre, and author recommendations based on sales data.
    """,
    'description': """
        This module analyzes historical sales data to identify top-selling books, genres, and authors,
        providing valuable insights for store managers and enhancing customer experience.
    """,
    'author': "Your Name",
    'website': "http://www.yourcompany.com",
    'category': 'Sales',
    'version': '1.0',
    'depends': ['base', 'sale', 'product', 'contacts'], # Dependensi pada modul sale dan product
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_inherit_views.xml',
        'wizard/book_recommendation_wizard_views.xml', # Tampilan wizard
        'views/book_recommendation_views.xml', # Tampilan hasil rekomendasi
        'views/book_recommendation_menus.xml', # Menu untuk modul
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}