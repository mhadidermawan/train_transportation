from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    train_state = fields.Selection([
        ('passenger', 'Passenger'),
        ('machinist', 'Machinist')
    ], string='Train State')

    identity = fields.Char(string='Nomor Identitas')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    born_date = fields.Date(string='Born Date')

    @api.constrains('identity', 'gender', 'born_date', 'train_state')
    def _check_train_state_constraints(self):
        for record in self:
            if record.train_state and not (record.identity and record.gender and record.born_date):
                raise models.ValidationError(
                    "Identity, Gender, dan Born Date Harus diisi jika train_state diisi."
                )
