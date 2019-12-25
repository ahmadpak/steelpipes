import frappe
from datetime import datetime
from datetime import timedelta

week = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
today = datetime.today()

labels = []


def days_between(from_date=datetime(today.year, today.month, 1), to_date=today):
    return abs((from_date - to_date).days)


def get_first_date_of_week(date=datetime.today()):
    day = date.strftime("%A")
    i = 0
    for weekday in week:
        if day == weekday:
            date = date + timedelta(-i)
            return date
        i += 1


def get_first_day_of_month(date=datetime.today()):
    date = datetime(date.year, date.month, 1)
    return date.strftime("%A")


def generate_labels(from_date=datetime(today.year, today.month, 1), to_date=today, duration='Monthly'):
    days = days_between(from_date, to_date)
    week_no = 0
    for day in range(days):
        date = from_date + timedelta(day)
        if days <= 31 and duration in ['Monthly','Weekly']:
            if date.strftime("%A") == 'Monday':
                week_no += 1
                labels.append("Week {}".format(week_no))
                print(week_no)
            else:
                labels.append(str(day+1))
        if days >31 and duration in ['Quarterly', 'Yearly']:
            pass



generate_labels()
print(labels)

# @frappe.whitelist
# def get_total_production(from_date=add_to_date(today(), months=-1), to_date=today(), duration='Monthly'):
#     total_days = date_diff(to_date, from_date)
#     if duration == 'Monthly':
#         if total_days < 30:
#             frappe.throw(
#                 'Please select date range of more than 30 DAYS', title='Data Selector')

#         labels = []
#         values = []
#     for i in range(total_days):
#         pass

#     result = frappe.db.get_list('Sales Invoice', filter={
#         'Document Status': 'Submitted',
#         'date': ['between', '{0} to {1}'.format(from_date, to_date)]}, page_length=20, as_list=True, group_by='status')
