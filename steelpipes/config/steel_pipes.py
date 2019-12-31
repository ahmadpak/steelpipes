from __future__ import unicode_literals
import frappe
from frappe import _


def get_data():
    return[
        {
            "label": _("Pipe Reports"),
            "items": [
                {
                    "type": "page",
                    "link": "pipe-stock-summary",
                    "label": _("Pipe Stock Summary"),
                    "name": "Pipe Stock Summary",
                    "description": _("Show pipe qty length and weight as a summary."),
                },

                {
                    "type": "report",
                    "name": "Pipe Stock Ledger",
                    "doctype": "Stock Entry",
                    "is_query_report": True
                },
            ]
        }
    ]
