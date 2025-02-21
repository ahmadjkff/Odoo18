from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='New', translate=1)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Datetime(tracking=1, compute='_compute_date_availability')
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1)
    bedrooms = fields.Integer(groups="app_one.property_manager_group")
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ], default='north')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    state = fields.Selection([
        ('draft','Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft' ,tracking=1)
    active = fields.Boolean(default=1)
    create_time = fields.Datetime(default=fields.Datetime.now())

    line_ids = fields.One2many('property.line','property_id')

    _sql_constraints = [
        ('unique_name','unique("name")','This name already exist!'),
    ]

    @api.depends('create_time')
    def _compute_date_availability(self):
        for rec in self:
            rec.date_availability = rec.create_time + timedelta(hours=6)

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('please add valid number for bedrooms')

    def draft_action(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state': 'draft'
            # })
    def pending_action(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state= 'pending'

    def sold_action(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state= 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.state == 'closed':
                rec.is_late = False
                continue
            if rec.expected_selling_date and rec.expected_selling_date <= fields.date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    def action(self):
        print(self.env['property'].search(['|',('name','=','Property1'), ('postcode','!=','123')]))

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print('inside _compute_diff method')
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _on_expected_price_change(self):
        for rec in self:
            print('inside _on_expected_price_change method')
            if rec.expected_price < rec.selling_price:
                raise ValidationError("expected price can't be less than selling price")

    @api.onchange('line_ids')
    def _on_line_ids_change(self):
        for rec in self:
            if len(rec.line_ids) > rec.bedrooms:
                raise ValidationError('bedrooms must be greater than or equal to number of lines')

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=''):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason,
                'line_ids': [(0,0,{'description':line.description, 'area': line.area}) for line in rec.line_ids]
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_property_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id,'form']]
        return action

class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()