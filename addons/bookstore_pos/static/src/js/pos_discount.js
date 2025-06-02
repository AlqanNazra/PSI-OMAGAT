odoo.define('bookstore_pos.PosDiscount', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { Orderline } = require('point_of_sale.models');

    const PosDiscountOrderline = (Orderline) =>
        class extends Orderline {
            compute_discount() {
                let fantasy_books = 0;
                let education_books = 0;
                const order = this.pos.get_order();
                order.orderlines.forEach(line => {
                    const product = line.get_product();
                    if (product.is_book) {
                        if (product.genre === 'Fantasy') {
                            fantasy_books += line.get_quantity();
                        } else if (product.genre === 'Edukasi') {
                            education_books += line.get_quantity();
                        }
                    }
                });
                if (fantasy_books >= 2 && this.get_product().genre === 'Fantasy') {
                    this.set_discount(10);
                }
                if (education_books >= 3 && this.get_product().genre === 'Edukasi') {
                    this.set_discount(15);
                }
            }
        };

    Registries.Model.extend(Orderline, PosDiscountOrderline);
});