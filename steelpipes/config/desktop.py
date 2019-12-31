from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Steel Pipes",
			"category": "Modules",
			"label": _("Steel Pipes"),
			"color": "blue",
			"icon": "octicon octicon-graph",
			"type": "module",
			# "onboard_present": 1
			"description": "Pipe stock summary, Pipe stock Ledger, Havenir Insight"
		}
	]
