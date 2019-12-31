from __future__ import unicode_literals
import frappe
from frappe import _


def get_data():
    config = [
        {
            "label": _("Pipe Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Pipe Stock Ledger",
                    "is_query_report": True,
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Dashboards"),
            "items": [
                {
                    "type": "Page",
                    "name": "Pipe Stock Summary",
                    "link": "pipe-stock-summary",
                    "description": _("Show pipe qty length and weight as a summary."),
                    "onboard": 1,
                },
            ]
        }
    ]

    return config
