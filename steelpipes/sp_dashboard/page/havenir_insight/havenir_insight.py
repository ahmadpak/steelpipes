import frappe
from datetime import datetime
from datetime import timedelta

week = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
today = datetime.today()


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


@frappe.whitelist()
def generate_labels_and_data_sets(from_date=datetime(datetime.today().year, datetime.today().month, 1), to_date=today, duration='Monthly'):
    data = {}
    labels = []
    datasets = []
    days = days_between(from_date, to_date)
    week_no = 0
    temp_dict = {}
    temp_dict['name'] = "Pipe Sold in Tons"
    temp_array = []

    for day in range(days):
        date = from_date + timedelta(day)
        if days <= 31 and duration in ['Monthly', 'Weekly']:
            if date.strftime("%A") == 'Monday':
                week_no += 1
                labels.append("Week {}".format(week_no))
            else:
                labels.append(str(day+1))
        if days > 31 and duration in ['Quarterly', 'Yearly']:
            pass
        pipe_sold = frappe.db.get_list('Sales Invoice',
                                       filters={
                                           'posting_date': date,
                                           'docstatus': 1
                                       },
                                       fields=['total_weight_um'],)
        total_pipe_sold = 0
        for weight in pipe_sold:
            total_pipe_sold += weight.total_weight_um/1000
        temp_array.append(total_pipe_sold)
        # print('Pipe in weight sold on date {0} is {1}'.format(
        #     date, total_pipe_sold))

    temp_dict['values'] = temp_array
    datasets.append(temp_dict)
    data['labels'] = labels
    data['datasets'] = datasets
    print(data)
    return data
