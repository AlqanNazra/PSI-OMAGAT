{
    'name': "Bookstore POS",
    'version': '1.0',
    'depends': ['base', 'point_of_sale', 'product', 'stock', 'account'],
    'author': "Your Name",
    'category': 'Sales/Point of Sale',
    'description': "Custom module for bookstore POS with book attributes, discount bundles, inventory, and invoicing integration.",
    'data': [
        'data/book_genre_data.xml',
        'data/discount_rules.xml',
        'data/stock_notification_data.xml',
        'views/product_template_views.xml',
        'views/pos_templates.xml',
        'views/invoice_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'bookstore_pos/static/src/js/pos_discount.js',
            'bookstore_pos/static/src/xml/pos_discount.xml',
        ],
    },
    'installable': True,
    'application': True,
}