{
       'name': "Book Attributes Extension",
       'version': '1.0',
       'depends': ['base', 'point_of_sale', 'product', 'stock', 'account'],
       'author': "Your Name",
       'category': 'Sales/Point of Sale',
       'description': "Extension module to add book attributes and discount logic to Odoo products.",
       'data': [
           'security/ir.model.access.csv',
           'data/book_genre_data.xml',
           'data/stock_notification_data.xml',
           'views/product_template_views.xml',
           'views/invoice_views.xml',
           'views/book_genre_views.xml',
       ],
       'assets': {
           'point_of_sale._assets_pos': [
               'book_attributes_extension/static/src/js/pos_discount.js',
               'book_attributes_extension/static/src/xml/pos_discount.xml',
           ],
       },
       'installable': True,
       'application': True,
   }