# Copyright (c) 2013, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns() 
	data = [{"date":"ABC","item_code":"pipe test","warehouse":"headoffice","estimate_weight":"95","scale_weight":"94.50"},
			{"date":"ABC","item_code":"pipe test","warehouse":"headoffice","estimate_weight":"95","scale_weight":"94.50"},
			{"voucher_type":"ABC","item_code":"pipe test","warehouse":"headoffice","estimate_weight":"95","scale_weight":"94.50"}
	]
	return columns, data


def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 95},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
		{"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
		{"label": _("Est. Weight(KG)"), "fieldname": "estimate_weight", "fieldtype": "Data", "width": 120},
		{"label": _("Scale Weight(KG)"), "fieldname": "scale_weight", "fieldtype": "Data", "width": 120},
		{"label": _("Total Scale Weight(KG)"), "fieldname": "total_scale_weight", "fieldtype": "Float", "width": 150},
		{"label": _("Qty"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 100, "convertible": "qty"},
		{"label": _("Balance Qty"), "fieldname": "qty_after_transaction", "fieldtype": "Float", "width": 100, "convertible": "qty"},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 110},
		{"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
	]

	return columns

def get_rows(filters=None):
	pass

def get_items(filters):
	conditions = []
	if filters.get("item_code"):
		conditions.append("item.name=%(item_code)s")
	else:
		if filters.get("brand"):
			conditions.append("item.brand=%(brand)s")
		if filters.get("item_group"):
			conditions.append(get_item_group_condition(filters.get("item_group")))

	items = []
	if conditions:
		items = frappe.db.sql_list("""select name from `tabItem` item where {}"""
			.format(" and ".join(conditions)), filters)
	return items

def get_item_group_condition(item_group):
	item_group_details = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"], as_dict=1)
	if item_group_details:
		return "item.item_group in (select ig.name from `tabItem Group` ig \
			where ig.lft >= %s and ig.rgt <= %s and item.item_group = ig.name)"%(item_group_details.lft,
			item_group_details.rgt)

	return ''