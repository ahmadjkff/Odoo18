from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTasks(models.Model):
    _name = 'todo.task'
    _description = 'To-Do Task'

    name = fields.Char(string='Task Name', required=True)
    assign_to =  fields.Many2many(
        'res.partner',  # Related model
        'todo_task_res_partner_rel',  # Name of the relation table
        'task_id',  # Column for this model
        'partner_id',  # Column for the related model
    )
    description = fields.Text()
    due_date = fields.Date()
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed', 'Closed')
    ], default='new')
    estimated_time = fields.Integer()
    todo_line_ids = fields.One2many('todo.line','todo_id')
    active = fields.Boolean(default=True)
    is_todo_late = fields.Boolean()
    total_duration = fields.Integer(compute="_compute_total_duration", store=True)

    def new_action(self):
        for rec in self:
            rec.status='new'

    def in_progress_action(self):
        for rec in self:
            rec.status='in_progress'

    def completed_action(self):
        for rec in self:
            rec.status='completed'

    @api.depends('todo_line_ids.duration')
    def _compute_total_duration(self):
        for rec in self:
            rec.total_duration = sum(line.duration for line in rec.todo_line_ids)
            if rec.total_duration > rec.estimated_time:
                raise ValidationError("Total duration can't be greater than estimated time.")

    def action_closed(self):
        self.status = 'closed'

    def check_due_date(self):
        todo_ids = self.search([])
        for rec in todo_ids:
            if rec.due_date and rec.due_date <= fields.date.today():
                rec.is_todo_late = True
            else:
                rec.is_todo_late = False
class TodoLine(models.Model):
    _name = 'todo.line'

    todo_id = fields.Many2one('todo.task')
    duration = fields.Float(digits='2')
    description = fields.Text()