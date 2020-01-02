from __future__ import unicode_literals
import frappe
from frappe import _


def get_data():
    config = [
        {
            "label": _("Pipe Stock Reports"),
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
            "label": _("Party Reports"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Supplier Balance Report Generator",
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Customer Balance Report Generator",
                    "onboard": 1,
                }
            ]
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
        },
        {
            "label": _("Settings"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Pipe Stock Summary Setting",
                    "onboard": 1,
                }
            ]
        }
    ]

    return config
