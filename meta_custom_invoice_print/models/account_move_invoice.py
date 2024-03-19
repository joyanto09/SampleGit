# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.http import request


class AccountMoveInvoice(models.Model):
    _inherit = 'account.move'

    def action_print_custom_invoice(self):
        print('success')
        data = {
            'form_data': self.read()[0],
            'line_data': self.invoice_line_ids.read(),
        }
        return self.env.ref(
            'meta_custom_invoice_print.action_account_custom_invoice_report').report_action([], data=data)

    def get_product_code(self, product_id):
        product = self.env['product.product'].browse(product_id)
        if product:
            code = product.default_code

            return code

    def get_line_calculation_data(self, product, move_line_id, move_id):
        print('HIt hERE')
        line = self.env['account.move.line'].browse(move_line_id)
        move = self.env['account.move'].browse(move_id)
        product = self.env['product.product'].browse(product)
        res = []
        vat_amount = 0.00
        vat_amount2 = 0.00
        for vat in line.tax_ids:
            total_vat = line.quantity * line.price_unit * (vat.amount / 100)
            vat_amount += total_vat
            vat_amount2 += total_vat / line.quantity

        coupon_program = self.env['coupon.program'].sudo().search([])
        discount = 0.00
        discount2 = 0.00
        for rec in coupon_program:
            is_coupon = False
            for itnm in rec.discount_specific_product_ids:
                if itnm.id == product.id:
                    is_coupon = True
                else:
                    is_coupon = False

            if is_coupon:
                promotion_line = self.env['account.move.line'].sudo().search([('move_id', '=', move.id),
                                                                              ('product_id', '=', rec.discount_line_product_id.id)])
                if promotion_line:
                    # print('Promotion line: %s' % promotion_line.price_unit)
                    discount = promotion_line.price_unit
                    discount2 = promotion_line.price_unit / line.quantity
        discount_amount = discount
        discount_amount2 = discount2

        total = ((line.quantity * line.price_unit) + vat_amount) + discount_amount
        unit_price = total / line.quantity
        return [{
            'price_unit': unit_price,
            'vat_amount': vat_amount,
            'vat_amount2': vat_amount2,
            'discount': discount_amount,
            'discount2': discount_amount2,
            'net_invoice': total}]



# res = []
#         for item in line_item:
#             res.append({
#                 'product': item.product,
#                 'quantity': item.product_qty,
#                 'uom': item.product_uom,
#                 'rate': item.product_rate,
#             })
#
#         return res