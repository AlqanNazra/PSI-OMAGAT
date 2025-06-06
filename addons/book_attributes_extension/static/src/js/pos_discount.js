odoo.define('book_attributes_extension.PosDiscount', ['point_of_sale.PosComponent', 'point_of_sale.Registries', 'point_of_sale.models'], function (require) {
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
                if (!order || !order.orderlines) return;
                order.orderlines.forEach(line => {
                    const product = line.get_product();
                    if (product && product.is_book) {
                        if (product.genre && product.genre[1] === 'Fantasy') {
                            fantasy_books += line.get_quantity();
                        } else if (product.genre && product.genre[1] === 'Edukasi') {
                            education_books += line.get_quantity();
                        }
                    }
                });
                if (fantasy_books >= 2 && this.get_product().genre && this.get_product().genre[1] === 'Fantasy') {
                    this.set_discount(10);
                }
                if (education_books >= 3 && this.get_product().genre && this.get_product().genre[1] === 'Edukasi') {
                    this.set_discount(15);
                }
            }
        };

    Registries.Model.extend(Orderline, PosDiscountOrderline);
});