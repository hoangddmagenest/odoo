from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import time


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    location_check = fields.Many2one(related='picking_type_id.warehouse_id.view_location_id')
    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_src_id,
        check_company=True, required=True, readonly=True, domain="""[('id', 'child_of', location_check)]""",
        states={'draft': [('readonly', False)], 'waiting': [('readonly', False)], 'confirmed': [('readonly', False)],
                'assigned': [('readonly', False)]})

    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_dest_id,
        check_company=True, readonly=True, domain="""[('id', 'child_of', location_check)]""", required=True,
        states={'draft': [('readonly', False)], 'waiting': [('readonly', False)], 'confirmed': [('readonly', False)],
                'assigned': [('readonly', False)]})

