# Copyright (c) 2013, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	return columns, data


def get_columns(filters):
	if filters.get('warehouse'):
		columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 95},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
		{"label": _("Est. Weight(KG)"), "fieldname": "estimate_weight", "fieldtype": "Float","precision":2, "width": 60},
		{"label": _("Scale Weight(KG)"), "fieldname": "scale_weight", "fieldtype": "Float","precision":2, "width": 60},
		{"label": _("Total Scale Weight(KG)"), "fieldname": "total_scale_weight", "fieldtype": "Float","precision":2, "width": 100},
		{"label": _("Qty"), "fieldname": "actual_qty", "fieldtype": "Float","precision":2, "width": 60, "convertible": "qty"},
		{"label": _("Balance Qty"), "fieldname": "qty_after_transaction", "fieldtype": "Float","precision":2, "width": 100, "convertible": "qty"},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 110},
		{"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
		]
		return columns	
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 95},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
		{"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 100},
		{"label": _("Est. Weight(KG)"), "fieldname": "estimate_weight", "fieldtype": "Float","precision":2, "width": 60},
		{"label": _("Scale Weight(KG)"), "fieldname": "scale_weight", "fieldtype": "Float","precision":2, "width": 60},
		{"label": _("Total Scale Weight(KG)"), "fieldname": "total_scale_weight", "fieldtype": "Float","precision":2, "width": 100},
		{"label": _("Qty"), "fieldname": "actual_qty", "fieldtype": "Float","precision":2, "width": 100, "convertible": "qty"},
		{"label": _("Balance Qty"), "fieldname": "qty_after_transaction", "fieldtype": "Float","precision":2, "width": 100, "convertible": "qty"},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 110},
		{"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
	]

	return columns