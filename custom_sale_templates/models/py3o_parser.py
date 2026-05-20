# -*- coding: utf-8 -*-
from odoo import models
from num2words import num2words


def morph(n, forms):
    # forms = (singular, few, many)
    n = abs(n) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return forms[2]
    if 2 <= n1 <= 4:
        return forms[1]
    if n1 == 1:
        return forms[0]
    return forms[2]

class Py3oReport(models.TransientModel):
    _inherit = 'py3o.report'

    def _get_parser_context(self, model_instance, data):
        context = super()._get_parser_context(model_instance, data)

        def amount_to_text_ua(amount):
            try:
                amount = float(amount)
            except Exception:
                return str(amount)

            hryvnia = int(amount)
            kopiyka = int(round((amount - hryvnia) * 100))

            hryvnia_words = num2words(hryvnia, lang='uk') if hryvnia > 0 else 'нуль'
            kopiyka_words = num2words(kopiyka, lang='uk') if kopiyka > 0 else 'нуль'

            hryvnia_unit = morph(hryvnia, ('гривня', 'гривні', 'гривень'))
            kopiyka_unit = morph(kopiyka, ('копійка', 'копійки', 'копійок'))

            if kopiyka == 0:
                return f"{hryvnia_words} {hryvnia_unit}"
            else:
                return f"{hryvnia_words} {hryvnia_unit} {kopiyka_words} {kopiyka_unit}"

        context['amount_to_text_ua'] = amount_to_text_ua

        return context