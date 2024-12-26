from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def do_something(self):
        print('inside do_something method fffffffffffffffffffffffffff')