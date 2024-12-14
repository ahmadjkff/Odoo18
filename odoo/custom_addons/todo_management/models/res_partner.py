from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    task_ids = fields.Many2many(
        'todo.task',  # Related model
        'todo_task_res_partner_rel',  # Name of the relation table
        'partner_id',  # Column for this model
        'task_id',  # Column for the related model
        string='Tasks'
    )