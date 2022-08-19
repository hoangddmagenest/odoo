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

    # @api.onchange('location_id')
    # def _onchange_location_id(self):
    #     print('11111111')
    #     if self.location_check:
    #         list_location = self.get_list_location_id(self.location_check)
    #         return {'domain': {'location_id': [('id', 'in', list_location)]}}
    #
    # def get_list_location_id(self, location_id):
    #     list_location = []
    #     if location_id.child_ids:
    #         for location in location_id.child_ids:
    #             list_location.append(location.id)
    #     return list_location
