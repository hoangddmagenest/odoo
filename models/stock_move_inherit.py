from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import time


class StockMove(models.Model):
    _inherit = 'stock.move'

    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=True, required=True,
        check_company=True,  domain="""[('id', 'child_of', parent.location_id)]""",
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")

    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=True, index=True, required=True, domain="""[('id', 'child_of', parent.location_id)]""",
        check_company=True,
        help="Location where the system will stock the finished products.")

    @api.constrains('location_id')
    def _onchange_location_id(self):
        for rec in self:
            if not rec.picking_id:
                continue

            if rec.location_id:
                rec.move_line_ids.write({'location_id': rec.location_id.id})

    @api.constrains('location_dest_id')
    def _onchange_location_id(self):
        for rec in self:
            if not rec.picking_id:
                continue

            if rec.location_id:
                rec.move_line_ids.write({'location_dest_id': rec.location_dest_id.id})
