from odoo import api, fields, models
from datetime import datetime

class NameCardRequest(models.Model):
    _name = 'namecard.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Name Card Request'

    name = fields.Char(string="Ref No.", readonly=True)
    staff = fields.Many2one(string="Staff Name", comodel_name='res.users', tracking=True)
    company_selection = fields.Selection([('SISB', 'SIGNATURE INTERNATIONAL'), ('SCSB', 'SIGNATURE CABINET SDN BHD'), ('SMSB', 'SIGNATURE MANUFACTURING SDN BHD'), ('SKSB', 'SIGNATURE KITCHEN SDN BHD'), ('SOSB', 'SIGNATURE OBICORP SDN BHD'), ('SASB', 'SIGNATURE ALUMINIUM SDN BHD'), ('KUBIQ', 'KUBIQ SDN BHD'), ('Others', 'OTHERS')], string="Company Selection")
    other_company = fields.Char(string="Other Company")
    branch = fields.Char(string="HQ / Branch")
    address = fields.Text(string="Full Address")
    card_name = fields.Char(string="Name to be appear on card")
    card_position = fields.Char(string="Position to be appear on the card")
    card_mobile = fields.Char(string="Handphone No.")
    card_general_line = fields.Char(string="General Line")
    card_did = fields.Char(string="DID")
    card_fax_no = fields.Char(string="Fax No.")
    card_email = fields.Char(string="Email Address")
    card_website = fields.Char(string="Website (If different from HQ)")
    card_quantity = fields.Selection([('200', '200 pcs'), ('400', '400 pcs')], string="Quantity Requested")
    state = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='draft', string='Tracking')
    submitted_by = fields.Many2one(string="Submitted By", comodel_name='res.users', readonly=True)
    submitted_date = fields.Datetime(string="Submitted Date", readonly=True)
    completed_by = fields.Many2one(string="Completed By", comodel_name='res.users', readonly=True)
    completed_date = fields.Datetime(string="Completed Date", readonly=True, help="completed date")
    # completed_date = fields.Datetime(default=lambda self: fields.Datetime.now(), string="Completed Date", readonly=True, help="completed date")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('namecard.request')
        return super(NameCardRequest, self).create(vals)

    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'
            rec.submitted_by = rec.staff
            rec.submitted_date = datetime.now()

    def action_complete(self):
        for rec in self:
            rec.state = 'completed'
            rec.completed_by = rec.staff
            rec.completed_date = datetime.now()

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'