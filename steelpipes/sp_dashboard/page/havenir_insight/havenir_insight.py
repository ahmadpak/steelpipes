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
def generate_total_pipe_labels_and_data_sets(period='This Month', resolution='1'):
    data = {}
    labels = []
    datasets = []
    today = datetime.today()
    if period == 'This Month':
        from_date = datetime(today.year, today.month, 1)
        to_date = today
        days = days_between(from_date, to_date)
    elif period == 'Last Month':
        from_date = datetime(today.year, today.month - 1, 1)
        temp_date = datetime(today.year, today.month, 1)
        print(temp_date)
        to_date = today - timedelta(days_between(temp_date, today))
        print('to date is: {0}'.format(to_date))
        days = days_between(from_date, to_date)
        print('days: {0}'.format(days))
    week_no = 0
    temp_dict = {}
    temp_dict['name'] = "Pipes Sold"
    temp_array = []
    total_pipe_sold = 0

    for day in range(days):
        date = from_date + timedelta(day)
        print(date)
        pipe_sold = frappe.db.get_list('Sales Invoice',
                                       filters={
                                           'posting_date': date,
                                           'docstatus': 1
                                       },
                                       fields=['total_weight_um'],)
        if resolution == '2':
            if period in ['This Month', 'Last Month']:
                for weight in pipe_sold:
                    total_pipe_sold += weight.total_weight_um/1000
                if date.strftime("%A") == 'Sunday':
                    week_no += 1
                    labels.append("Week {}".format(week_no))
                else:
                    labels.append(str(day+1))
                temp_array.append(total_pipe_sold)
                total_pipe_sold = 0

        elif resolution == '1':
            if period in ['This Month', 'Last Month']:
                for weight in pipe_sold:
                    total_pipe_sold += weight.total_weight_um/1000
                if date.strftime("%A") == 'Sunday':
                    week_no += 1
                    labels.append("Week {}".format(week_no))
                    temp_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1:
                    week_no += 1
                    labels.append("Week {}".format(week_no))
                    temp_array.append(total_pipe_sold)
                    total_pipe_sold = 0

    print('resolution: {}'.format(resolution))
    print('period: {}'.format(period))
    temp_dict['values'] = temp_array
    datasets.append(temp_dict)
    data['labels'] = labels
    data['datasets'] = datasets
    print(data)
    dummy = 'This is dummy data'
    return [data,dummy]
