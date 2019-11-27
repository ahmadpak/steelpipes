# Copyright (c) 2013, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	frappe.msgprint('starting the report')
	columns = get_columns(filters)
	items = get_items(filters)
	sl_entries = get_stock_ledger_entries(filters, items) 
	item_details = get_item_details(items, sl_entries)
	opening_row = get_opening_balance(filters, columns)

	data = []
	if opening_row:
		data.append(opening_row)

	for sle in sl_entries:
		item_detail = item_details[sle.item_code]

		sle.update(item_detail)
		voucher_type = sle['voucher_type']
		voucher_no = sle['voucher_no']
		item_code = sle['item_code']
		warehouse = sle['warehouse']

		if voucher_type in ['Purchase Receipt','Stock Entry', 'Delivery Note']:
			if voucher_type in ['Stock Entry']:
				voucher_type += ' Detail'
			else:
				voucher_type += ' Item'
			sql_query = '''
			SELECT 	qty,
					weight_um as estimate_weight, 
					scale_weight_um as scale_weight, 
					total_scale_weight_um as total_scale_weight
			FROM `tab{0}`
			WHERE parent='{1}' AND item_code='{2}' AND warehouse='{3}'
			'''.format(voucher_type,voucher_no,item_code,warehouse)
			query_result = frappe.db.sql(sql_query,as_dict=1)
			sle['estimate_weight'] = query_result[0]['estimate_weight']
			sle['scale_weight'] = query_result[0]['scale_weight']
			sle['total_scale_weight'] = query_result[0]['total_scale_weight']

		data.append(sle)

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

def get_stock_ledger_entries(filters, items):
	item_conditions_sql = ''
	if items:
		item_conditions_sql = 'and sle.item_code in ({})'\
			.format(', '.join([frappe.db.escape(i) for i in items]))

	return frappe.db.sql("""select concat_ws(" ", posting_date, posting_time) as date,
			item_code, warehouse, actual_qty, qty_after_transaction, voucher_type, voucher_no
		from `tabStock Ledger Entry` sle
		where company = %(company)s and
			posting_date between %(from_date)s and %(to_date)s
			{sle_conditions}
			{item_conditions_sql}
			order by posting_date asc, posting_time asc, creation asc"""\
		.format(
			sle_conditions=get_sle_conditions(filters),
			item_conditions_sql = item_conditions_sql
		), filters, as_dict=1)

def get_sle_conditions(filters):
	conditions = []
	if filters.get("warehouse"):
		warehouse_condition = get_warehouse_condition(filters.get("warehouse"))
		if warehouse_condition:
			conditions.append(warehouse_condition)
	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_warehouse_condition(warehouse):
	warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
	if warehouse_details:
		return " exists (select name from `tabWarehouse` wh \
			where wh.lft >= %s and wh.rgt <= %s and warehouse = wh.name)"%(warehouse_details.lft,
			warehouse_details.rgt)

	return ''

def get_item_details(items, sl_entries, include_uom = None):
	item_details = {}
	if not items:
		items = list(set([d.item_code for d in sl_entries]))

	if not items:
		return item_details

	cf_field = cf_join = ""
	if include_uom:
		cf_field = ", ucd.conversion_factor"
		cf_join = "left join `tabUOM Conversion Detail` ucd on ucd.parent=item.name and ucd.uom='%s'" \
			% (include_uom)

	res = frappe.db.sql("""
		select
			item.name, item.item_name, item.description, item.item_group, item.brand, item.stock_uom {cf_field}
		from
			`tabItem` item
			{cf_join}
		where
			item.name in ({item_codes})
	""".format(cf_field=cf_field, cf_join=cf_join, item_codes=','.join(['%s'] *len(items))), items, as_dict=1)

	for item in res:
		item_details.setdefault(item.name, item)

	return item_details

def get_opening_balance(filters, columns):
	if not (filters.item_code and filters.warehouse and filters.from_date):
		return

	from erpnext.stock.stock_ledger import get_previous_sle
	last_entry = get_previous_sle({
		"item_code": filters.item_code,
		"warehouse_condition": get_warehouse_condition(filters.warehouse),
		"posting_date": filters.from_date,
		"posting_time": "00:00:00"
	})
	row = {}
	row["item_code"] = _("'Opening'")
	for dummy, v in ((9, 'qty_after_transaction'), (11, 'valuation_rate'), (12, 'stock_value')):
			row[v] = last_entry.get(v, 0)

	return row