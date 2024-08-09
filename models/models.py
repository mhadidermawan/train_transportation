from odoo import models, fields, api

class TrainCity(models.Model):
    _name = 'train.city'
    _description = 'Train City'

    name = fields.Char(string="City Name", required=True)
    code = fields.Char(string="City Code", required=True)

class TrainStation(models.Model):
    _name = 'train.station'
    _description = 'Train Station'

    code = fields.Char(string="Station Code", required=True)
    name = fields.Char(string="Station Name", required=True)
    city_id = fields.Many2one('train.city', string="City", required=True)
    address = fields.Text(string="Address")

class TrainTrain(models.Model):
    _name = 'train.train'
    _description = 'Train'

    name = fields.Char(string="Train Name", required=True)
    code = fields.Char(string="Train Code", required=True)
    capacity = fields.Integer(string="Capacity", required=True)
    state = fields.Selection([
        ('ready', 'Ready'),
        ('not_ready', 'Not Ready'),
        ('maintenance', 'Maintenance')
    ], string="State", default='ready')
    active = fields.Boolean(string="Active", default=True)
    schedule_line_ids = fields.One2many('train.schedule', 'train_id', string="Schedules")

class TrainSchedule(models.Model):
    _name = 'train.schedule'
    _description = 'Train Schedule'

    code = fields.Char(string="Schedule Code", readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('train.schedule.code'))
    origin = fields.Many2one('train.station', string="Origin", required=True)
    destination = fields.Many2one('train.station', string="Destination", required=True)
    schedule_time = fields.Datetime(string="Schedule Time", required=True)
    duration = fields.Float(string="Duration (hours)", required=True)
    arrival_time = fields.Datetime(string="Arrival Time", compute="_compute_arrival_time", store=True)
    train_id = fields.Many2one('train.train', string="Train", required=True)
    capacity = fields.Integer(string="Capacity", related="train_id.capacity", store=True)

    @api.depends('schedule_time', 'duration')
    def _compute_arrival_time(self):
        for record in self:
            if record.schedule_time and record.duration:
                record.arrival_time = record.schedule_time + timedelta(hours=record.duration)

