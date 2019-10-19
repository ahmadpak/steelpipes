# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "steelpipes"
app_title = "Steel Pipes"
app_publisher = "Havenir"
app_description = "App for steel pipe traders and manufacturers"
app_icon = "octicon octicon-project"
app_color = "grey"
app_email = "info@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/steelpipes/css/steelpipes.css"
# app_include_js = "/assets/steelpipes/js/steelpipes.js"

# include js, css files in header of web template
# web_include_css = "/assets/steelpipes/css/steelpipes.css"
# web_include_js = "/assets/steelpipes/js/steelpipes.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

#fixtures = [{
#        "dt":"Custom Field", "filters": [
#            [
#                "dt","in", (
#                            "Sales Order","Sales Order Item",
#                            "Delivery Note","Delivery Note Item",
#                            "Sales Invoice","Sales Invoice Item",
#                            "Purchase Order","Purchase Order Item",
#                            "Purchase Receipt","Purchase Receipt Item",
#                            "Purchase Invoice","Purchase Invoice Item"
#                            )
#            ]
#        ]
#}]

fixtures = [{
    'dt': 'Custom Field', 'filters':[
        [
            'name', 'in', [
                "Sales Order-estimate_weight_um"
                "Sales Order Item-weight_section",
                "Sales Order Item-um",
                "Sales Order Item-rate_um",
                "Sales Order Item-column_break_8",
                "Sales Order Item-weight_um",
                "Sales Order Item-length_um",
                "Sales Order Item-total_length_um",
                "Sales Order Item-total_weight_um",
                "Sales Order Item-rate_um_per_qty",
                "Sales Order Item-amount_um",
                "Delivery Note-empty_vehicle_weight_um",
                "Delivery Note-loaded_vehicle_weight_um",
                "Delivery Note-estimate_weight_um",
                "Delivery Note-section_break_61",
                "Delivery Note-weight_difference_um",
                "Delivery Note-weight_difference_percentage_um",
                "Delivery Note-column_break_64",
                "Delivery Note-total_weight_um",
                "Delivery Note-total_scale_weight_um",
                "Delivery Note-has_weight",
                "Delivery Note-update_weight_calculations_um",
                "Delivery Note-total_um",
                "Delivery Note-apply_auto_discount",
                "Delivery Note Item-um",
                "Delivery Note Item-rate_um",
                "Delivery Note Item-weight_section",
                "Delivery Note Item-scale_weight_um",
                "Delivery Note Item-weight_um",
                "Delivery Note Item-length_um",
                "Delivery Note Item-column_break_11",
                "Delivery Note Item-total_scale_weight_um",
                "Delivery Note Item-total_weight_um",
                "Delivery Note Item-total_length_um",
                "Delivery Note Item-rate_um_per_qty",
                "Delivery Note Item-amount_um",
                "Sales Invoice-weight_calculations",
                "Sales Invoice-empty_vehicle_weight_um",
                "Sales Invoice-loaded_vehicle_weight_um",
                "Sales Invoice-total_scale_weight_um",
                "Sales Invoice-column_break_72",
                "Sales Invoice-estimate_weight_um",
                "Sales Invoice-total_weight_um",
                "Sales Invoice-weight_difference_um",
                "Sales Invoice-weight_difference_percentage_um",
                "Sales Invoice-total_um",
                "Sales Invoice-no_double_ledger",
                "Sales Invoice-apply_auto_discount",
                "Sales Invoice-transport",
                "Sales Invoice-cutting_labor",
                "Sales Invoice-loading",
                "Sales Invoice Item-weight_section",
                "Sales Invoice Item-rate_um",
                "Sales Invoice Item-scale_weight_um",
                "Sales Invoice Item-weight_um",
                "Sales Invoice Item-length_um",
                "Sales Invoice Item-column_break_10",
                "Sales Invoice Item-total_scale_weight_um",
                "Sales Invoice Item-total_weight_um",
                "Sales Invoice Item-total_length_um",
                "Sales Invoice Item-um",
                "Sales Invoice Item-rate_um_per_qty",
                "Sales Invoice Item-amount_um",
                "Purchase Order-estimate_weight_um",
                "Purchase Order Item-weight_section",
                "Purchase Order Item-um",
                "Purchase Order Item-rate_um",
                "Purchase Order Item-length_um",
                "Purchase Order Item-column_break_10",
                "Purchase Order Item-weight_um",
                "Purchase Order Item-total_weight_um",
                "Purchase Order Item-total_length_um",
                "Purchase Order Item-rate_um_per_qty",
                "Purchase Order Item-amount_um",
                "Purchase Receipt-has_weight",
                "Purchase Receipt-weight_calculations",
                "Purchase Receipt-empty_vehicle_weight_um",
                "Purchase Receipt-loaded_vehicle_weight_um",
                "Purchase Receipt-total_scale_weight_um",
                "Purchase Receipt-weight_difference_percentage_um",
                "Purchase Receipt-column_break_58",
                "Purchase Receipt-estimate_weight_um",
                "Purchase Receipt-total_weight_um",
                "Purchase Receipt-weight_difference_um",
                "Purchase Receipt-update_weight_calculations_um",
                "Purchase Receipt-total_um",
                "Purchase Receipt-apply_auto_discount",
                "Purchase Receipt Item-weight_section",
                "Purchase Receipt Item-um",
                "Purchase Receipt Item-rate_um",
                "Purchase Receipt Item-scale_weight_um",
                "Purchase Receipt Item-weight_um",
                "Purchase Receipt Item-length_um",
                "Purchase Receipt Item-column_break_12",
                "Purchase Receipt Item-total_scale_weight_um",
                "Purchase Receipt Item-total_weight_um",
                "Purchase Receipt Item-total_length_um",
                "Purchase Receipt Item-rate_um_per_qty",
                "Purchase Receipt Item-amount_um",
                "Purchase Invoice-weight_calculations",
                "Purchase Invoice-empty_vehicle_weight_um",
                "Purchase Invoice-loaded_vehicle_weight_um",
                "Purchase Invoice-total_scale_weight_um",
                "Purchase Invoice-column_break_69",
                "Purchase Invoice-estimate_weight_um",
                "Purchase Invoice-total_weight_um",
                "Purchase Invoice-weight_difference_um",
                "Purchase Invoice-weight_difference_percentage_um",
                "Purchase Invoice-total_um",
                "Purchase Invoice-no_double_ledger",
                "Purchase Invoice-apply_auto_discount",
                "Purchase Invoice Item-weight_section",
                "Purchase Invoice Item-rate_um",
                "Purchase Invoice Item-scale_weight_um",
                "Purchase Invoice Item-weight_um",
                "Purchase Invoice Item-length_um",
                "Purchase Invoice Item-column_break_8",
                "Purchase Invoice Item-um",
                "Purchase Invoice Item-total_scale_weight_um",
                "Purchase Invoice Item-total_weight_um",
                "Purchase Invoice Item-total_length_um",
                "Purchase Invoice Item-rate_um_per_qty",
                "Purchase Invoice Item-amount_um",
                "Item-section_break_44",
                "Item-last_quantity_received",
                "Item-last_weight_received",
                "Item-column_break_41",
                "Item-last_quantity_delivered",
                "Item-last_weight_delivered",
                "Item-weight_statistics",
                "Customer-outstanding_balance"
            ]
        ]
    ]
}]

doctype_js = {
    #"Sales Order"   :   [   "sp_delivery_note/sp_delivery_note_item.js"
     #                   ],
    "Sales Order"   :   [   
                            "sp_sales_order/sp_sales_order_item.js",
                            "sp_sales_order/sp_sales_order.js"
                        ],
    "Delivery Note" :   [   
                            "sp_delivery_note/sp_delivery_note.js",
                            "sp_delivery_note/sp_delivery_note_item.js"
                        ],
    "Sales Invoice" :   [
                            "sp_sales_invoice/sp_sales_invoice_item.js"
                        ],                    
    "Purchase Order":   [
                            "sp_purchase_order/sp_purchase_order_item.js"
                        ],
    "Purchase Receipt": [
                            "sp_purchase_receipt/sp_purchase_receipt.js",
                            "sp_purchase_receipt/sp_purchase_receipt_item.js"
                        ],
    "Purchase Invoice": [
                            "sp_purchase_invoice/sp_purchase_invoice_item.js"
                        ]                                                            
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "steelpipes.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "steelpipes.install.before_install"
# after_install = "steelpipes.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "steelpipes.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Sales Order":{
        "validate"  :   "steelpipes.sp_sales_order.sp_sales_order.update_estimate_weight"
    },
    "Delivery Note":{
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um",
        "on_submit" :   "steelpipes.sp_delivery_note.sp_delivery_note_item.validate_weight_threshold"
    },
    "Sales Invoice":{
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um"
    },
    "Purchase Order":{
        "validate"  :   "steelpipes.sp_sales_order.sp_sales_order.update_estimate_weight"
    },
    "Purchase Receipt":{
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um",
        "on_submit" :   "steelpipes.sp_delivery_note.sp_delivery_note_item.validate_weight_threshold"
    },
    "Purchase Invoice":{
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um"
    },
    "Item":{
        "validate"  :   "steelpipes.sp_item.item.pipe_custom_name"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"steelpipes.tasks.all"
# 	],
# 	"daily": [
# 		"steelpipes.tasks.daily"
# 	],
# 	"hourly": [
# 		"steelpipes.tasks.hourly"
# 	],
# 	"weekly": [
# 		"steelpipes.tasks.weekly"
# 	]
# 	"monthly": [
# 		"steelpipes.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "steelpipes.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "steelpipes.event.get_events"
# }

