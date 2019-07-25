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
doctype_js = {
    #"Sales Order"   :   [   "sp_delivery_note/sp_delivery_note_item.js"
     #                   ],
    "Sales Order"   :   [   
                            "sp_sales_order/sp_sales_order_item.js"
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
    "Delivery Note": {
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um",
        "on_submit" :   "steelpipes.sp_delivery_note.sp_delivery_note_item.validate_weight_threshold"
    },
    "Purchase Order":{
        "validate"  :   "steelpipes.sp_sales_order.sp_sales_order.update_estimate_weight"
    },
    "Purchase Receipt": {
        "validate"  :   "steelpipes.sp_delivery_note.sp_delivery_note_item.update_pipe_weight_um",
        "on_submit" :   "steelpipes.sp_delivery_note.sp_delivery_note_item.validate_weight_threshold"
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

