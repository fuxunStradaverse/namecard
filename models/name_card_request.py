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

    # MY OWN SAMPLE
    # model: Agent.py
    #
    # from odoo import models, fields, api
    # # from odoo.exceptions import ValidationError
    #
    # class InsuranceAgent(models.Model):
    #     _name = "insurance.agent"
    #     _description = "Insurance Agent"
    #
    #     code = fields.Char(string='Code')
    #     name = fields.Char(string='Name', required=True)
    #     contactDetail = fields.Float(string='Contact Detail')
    #     emailID = fields.Char(string='Email ID')
    #     gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    #     relatedUser = fields.Many2one(string="Related User", comodel_name='res.users')
    #     commissionType = fields.Selection([('fixed', 'Fixed'), ('percent', 'Based on Percentage')],
    #                                       string="Commission Type", default='fixed')
    #     amount = fields.Float(string='Amount')
    #     percentage = fields.Float(string='Percentage')
    #     totalCommisionAmount = fields.Float(string='Total Commision Amount', compute='_compute_agent_commission_paying')
    #     insurance_management_ids = fields.One2many('insurance.management', 'insurance_management_id',
    #                                                string='insurance management')
    #
    #     @api.model
    #     def create(self, vals):
    #         vals['code'] = self.env['ir.sequence'].next_by_code('insurance.agent')
    #         return super(InsuranceAgent, self).create(vals)
    #
    #     @api.depends('insurance_management_ids.totalCommisionAmount')
    #
    # def _compute_agent_commission_paying(self):
    #     for agent in self:
    #         total_commission = sum(agent.insurance_management_ids.mapped('totalCommisionAmount'))
    #         agent.totalCommisionAmount = total_commission
    #
    # model: Insurance.py
    #
    # from datetime import timedelta  # from python
    # from dateutil.relativedelta import relativedelta  # from python
    # from odoo import models, fields, api  # from odoo file
    # # from odoo.exceptions import ValidationError
    #
    # class InsuranceManagement(models.Model):
    #     _name = "insurance.management"
    #     _description = "Insurance Management"
    #
    #     name = fields.Char(string='Name', readonly=True)
    #     customer = fields.Many2one(string="Customer", comodel_name='res.partner')
    #     policy = fields.Many2one(string="Policy", comodel_name='insurance.policy')
    #     # agent = fields.Many2one(string="Agent", comodel_name='insurance.agent')
    #     startDate = fields.Datetime(default=lambda self: fields.Datetime.now(), string="Start Date")
    #     maturityDate = fields.Datetime(string="Maturity Date", compute='_compute_premium_paying')
    #     pay = fields.Integer(related='policy.pay')
    #     paymentType = fields.Selection(related='policy.paymentType')
    #     paymentMode = fields.Selection(related='policy.paymentMode', string="Payment mode")
    #     premiumAmount = fields.Integer(related='policy.premiumAmount', string="Premium Amount")
    #     totalpolicyAmount = fields.Integer(related='policy.totalpolicyAmount', string='Total Policy Amount')
    #     totalCommisionAmount = fields.Integer(string='Total Commision Amount', compute='_compute_commission_paying',
    #                                           comodel_name='insurance_management_id.amount')
    #     insurance_premium_ids = fields.One2many('insurance.premium', 'insurance_id', string='Insurance Premium')
    #     insurance_management_id = fields.Many2one('insurance.agent', string="agent")
    #     noPremium = fields.Char(string='No of Premium', readonly=True)
    #     state = fields.Selection(
    #         [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('sent_email', 'Sent Email'), ('done', 'Done'),
    #          ('cancel', 'Cancel')],
    #         default='draft',
    #         string='Status', required=True)
    #
    #     @api.model
    #     def create(self, vals):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('insurance.management')
    #         return super(InsuranceManagement, self).create(vals)
    #
    #     def action_confirmed(self):
    #         Premium = self.env['insurance.premium']
    #         premium_records = []  # List to accumulate premium data
    #         for rec in self:
    #             rec.state = 'confirmed'
    #             if rec.paymentMode == 'monthly':
    #                 payment = 12
    #                 paymonth = 1
    #             elif rec.paymentMode == 'quarterly':
    #                 payment = 3
    #                 paymonth = 3
    #             elif rec.paymentMode == 'halfYearly':
    #                 payment = 2
    #                 paymonth = 6
    #             elif rec.paymentMode == 'yearly':
    #                 payment = 1
    #                 paymonth = 12
    #             else:
    #                 payment = 0
    #             maturity_date = fields.Datetime.from_string(rec.startDate)
    #             maturity_dates = []
    #             no_of_premium = payment * rec.pay
    #             # commisionperNet = rec.totalCommisionAmount / no_of_premium
    #             for i in range(1, no_of_premium + 1):
    #                 maturity_date += relativedelta(months=paymonth)  # Add one month
    #                 maturity_dates.append(maturity_date)
    #                 premium_records.append({
    #                     'name': str(i),
    #                     'maturityDate': maturity_date,
    #                     'premiumAmount': rec.premiumAmount,
    #                     'totalCommisionAmount': rec.totalCommisionAmount,
    #                     'insurance_id': rec.id
    #                 })
    #         # Create premium records
    #         Premium.create(premium_records)
    #
    #     def action_sent_email(self):
    #         for rec in self:
    #             rec.state = 'sent_email'
    #
    #     def action_done(self):
    #         for rec in self:
    #             rec.state = 'done'
    #
    #     def action_cancel(self):
    #         for rec in self:
    #             rec.state = 'cancel'
    #
    #     def action_reset_to_draft(self):
    #         for rec in self:
    #             rec.state = 'draft'
    #
    #     # if you have more fields, you can put at here: @api.depends('date_of_birth', 'multiple fields')
    #     @api.depends('startDate', 'pay')
    #     def _compute_premium_paying(self):
    #         print("self......", self)
    #         for rec in self:
    #             # today = date.today()
    #             # print("date.today()", date.today())
    #             if rec.startDate and rec.pay:
    #                 # print("rec", rec, rec.name, rec.date_of_birth)
    #                 rec.maturityDate = rec.startDate + timedelta(days=rec.pay * 365)
    #             else:
    #                 rec.maturityDate = False
    #
    #     @api.depends('paymentMode', 'pay', 'insurance_management_id')
    #     def _compute_commission_paying(self):
    #         for rec in self:
    #             if rec.paymentMode and rec.pay and rec.insurance_management_id.amount:
    #                 if rec.paymentMode == 'monthly':
    #                     rec.totalCommisionAmount = rec.insurance_management_id.amount + rec.pay
    #                 elif rec.paymentMode == 'quarterly':
    #                     rec.totalCommisionAmount = rec.insurance_management_id.amount + rec.pay * 3
    #                 elif rec.paymentMode == 'halfYearly':
    #                     rec.totalCommisionAmount = rec.insurance_management_id.amount + rec.pay * 6
    #                 elif rec.paymentMode == 'yearly':
    #                     rec.totalCommisionAmount = rec.insurance_management_id.amount + rec.pay * 12
    #             else:
    #                 rec.totalCommisionAmount = 0
    #
    #     @api.depends('insurance_management_id')
    #
    # def _compute_agent_policy(self):
    #     for rec in self:
    #         rec._compute_commission_paying()
    #         if rec.insurance_management_id.percentage:
    #             rec.totalCommisionAmount = (rec.insurance_management_id.percentage / 100) * (
    #                         rec.insurance_management_id.amount + rec.pay)
    #         else:
    #             rec.totalCommisionAmount
    #
    # class InsurancePremium(models.Model):
    #     _name = "insurance.premium"
    #     _description = "Insurance Premium"
    #
    #     name = fields.Char(string='Number')
    #     maturityDate = fields.Datetime(string="Due Date")
    #     premiumAmount = fields.Float(string="Premium Amount")
    #     totalCommisionAmount = fields.Integer(string='Commision Amount')
    #     insurance_id = fields.Many2one('insurance.management', string="insurance")
