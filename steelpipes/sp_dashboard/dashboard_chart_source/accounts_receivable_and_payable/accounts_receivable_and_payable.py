# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils import add_to_date, date_diff, getdate, nowdate, get_last_day, formatdate
from erpnext.accounts.report.general_ledger.general_ledger import execute
from frappe.core.page.dashboard.dashboard import cache_source, get_from_date_from_timespan
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get_period_ending

from frappe.utils.nestedset import get_descendants_of

@frappe.whitelist()
@cache_source
def get(chart_name = None, chart = None, no_cache = None, from_date = None, to_date = None):
    if chart_name:
        chart = frappe.get_doc('Dashboard Chart', chart_name)
    else:
        chart = frappe._dict(frappe.parse_json(chart))
    timespan = chart.timespan
    timegrain = chart.time_interval
    filters = frappe.parse_json(chart.filters_json)

    account = filters.get("account")
    company = filters.get("company")

    if not to_date:
        to_date = nowdate()
    if not from_date:
        if timegrain in ('Daily','Weekly','Monthly', 'Quarterly'):
            from_date = get_from_date_from_timespan(to_date, timespan)

    # fetch dates to plot
    dates = get_dates_from_timegrain(from_date, to_date, timegrain)

    # Get balances on for set dates
    receivable = []
    for date in dates:
        sql_query_str = '''SELECT sum(debit)-sum(credit) FROM `tabGL Entry` WHERE company="{0}" AND party_type="Customer" AND posting_date<="{1}"'''.format(company,date)
        sql_query = frappe.db.sql(sql_query_str)
        if sql_query[0][0]==None:
            receivable.append(0)
        else:
            receivable.append(sql_query[0][0])
    payable = []
    for date in dates:
        sql_query_str = '''SELECT (sum(debit)-sum(credit))*-1 FROM `tabGL Entry` WHERE company="{0}" AND party_type="Supplier" AND posting_date<="{1}"'''.format(company,date)
        sql_query = frappe.db.sql(sql_query_str)
        if sql_query[0][0]==None:
            payable.append(0)
        else:
            payable.append(sql_query[0][0])

    return {
        "labels": [date for date in dates],
        "datasets": [{
            "name": 'Receivable',
            "values": receivable
        },
        {
            "name": 'Payable',
            "values": payable
        }]
    }


def get_dates_from_timegrain(from_date, to_date, timegrain):
    days = months = years = 0
    if "Daily" == timegrain:
        days = 1
    elif "Weekly" == timegrain:
        days = 7
    elif "Monthly" == timegrain:
        months = 1
    elif "Quarterly" == timegrain:
        months = 3

    dates = [get_period_ending(from_date, timegrain)]
    while getdate(dates[-1]) < getdate(to_date):
        date = get_period_ending(add_to_date(dates[-1], years=years, months=months, days=days), timegrain)
        dates.append(date)
    return dates