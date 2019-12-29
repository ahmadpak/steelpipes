import frappe
from datetime import datetime
from datetime import timedelta

week = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
    # Defaults
    pipe_sizes = ["3/4 INCH", "1 INCH", "1 1/2 INCH", "2 INCH", "2 1/2 INCH",
                  "3 INCH", "4 INCH", "5 INCH", "6 INCH", "7 INCH", "8 INCH", "10 INCH", "12 INCH"]
    pipe_thickness = ['1.00 MM', '1.50 MM', '2.00 MM', '2.50 MM', '3.00 MM', '3.50 MM',
                      '4.00 MM', '4.50 MM', '5.00 MM', '5.50 MM', '6.00 MM', '6.50 MM', '7.00 MM', '7.50 MM', '8.00 MM']
    today = datetime.today()
    week_no = 0
    month_no = 0

    # Defining data dictionaries
    total_pipe_sold_data = {}           # Total Pipe Sold
    individual_pipe_sold_data = {}      # Individual Pipe Sold
    thickness_pipe_sold_data = {}       # Thickness Pipe Sold

    # Defining labels
    total_pipe_sold_labels = []                     # Total Pipe Sold Labels
    individual_pipe_sold_labels = pipe_sizes        # Individual Pipe Sold Labels
    thickness_pipe_sold_labels = pipe_thickness     # Thickness Pipe Sold Labels

    # Defining Data sets
    total_pipe_sold_datasets = []       # Total Pipe Sold Datasets
    individual_pipe_sold_datasets = []  # Individual Pipe Sold Datasets
    thickness_pipe_sold_datasets = []   # Thickness Pipe Sold Datasets

    # Defining temporary dict and array for Total Pipe Sold
    temp_total_pipe_sold_data_dict = {}
    temp_total_pipe_sold_data_dict['name'] = "Pipes Sold"
    temp_total_pipe_sold_data_array = []
    total_pipe_sold = 0
    # Defining temporary dict and array for Individual Pipe Sold
    temp_individual_pipe_sold_data_dict = {}
    temp_individual_pipe_sold_data_dict['name'] = "Individual Pipes Sold"
    temp_individual_pipe_sold_data_array = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    individual_pipe_sold = 0
    # Defining temporary dict and array for Individual Pipe Sold
    temp_thickness_pipe_sold_data_dict = {}
    temp_thickness_pipe_sold_data_dict['name'] = "Individual Pipes Sold"
    temp_thickness_pipe_sold_data_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    thickness_pipe_sold = 0

    # From date, to date and days between for period 'This Month'
    if period == 'This Month':
        from_date = datetime(today.year, today.month, 1)
        to_date = today
        days = days_between(from_date, to_date)
    # From date, to date and days between for period 'This Quarter'
    elif period == 'This Quarter':
        temp_date = datetime(today.year, today.month, 1) - timedelta(90)
        from_date = datetime(temp_date.year, temp_date.month, 1)
        to_date = today
        days = days_between(from_date, to_date)
    # From date, to date and days between for period 'This Year
    elif period == 'This Year':
        from_date = datetime(today.year, 1, 1)
        to_date = today
        days = days_between(from_date, to_date)
    # From date, to date and days between for period 'Last Month'
    elif period == 'Last Month':
        from_date = datetime(today.year, today.month - 1, 1)
        temp_date = datetime(today.year, today.month, 1)
        to_date = today - timedelta(days_between(temp_date, today))
        days = days_between(from_date, to_date)
    # From date, to date and days between for period 'Last Quarter'
    elif period == 'Last Quarter':
        temp_date = datetime(today.year, today.month, 1) - timedelta(210)
        from_date = datetime(temp_date.year, temp_date.month, 1)
        temp_date = datetime(today.year, today.month, 1) - timedelta(90)
        to_date = datetime(temp_date.year, temp_date.month, 1)
        days = days_between(from_date, to_date)
    # From date, to date and days between for period 'Last Year'
    elif period == 'Last Year':
        from_date = datetime(today.year - 1, 1, 1)
        to_date = datetime(today.year - 1, 12, 31)
        days = days_between(from_date, to_date)

    for day in range(days):
        date = from_date + timedelta(day)
        pipe_sold = frappe.db.get_list('Sales Invoice',
                                       filters={
                                           'posting_date': date,
                                           'docstatus': 1
                                       },
                                       fields=['total_weight_um', 'name'],)
        for weight in pipe_sold:
            total_pipe_sold += weight.total_weight_um/1000
            sales_invoice = frappe.db.get_list('Sales Invoice Item',
                                               filters={
                                                   'docstatus': 1,
                                                   'parent': weight.name
                                               },
                                               fields=['item_code', 'total_scale_weight_um', 'warehouse'],)
            for items in sales_invoice:
                print(items.item_code)
                # Finding Pipe Size
                i=0
                for size in pipe_sizes:
                    if size in items.item_code:
                        print('Pipe Size: {}'.format(size))
                        temp_individual_pipe_sold_data_array[i] += items.total_scale_weight_um/1000
                    i += 1
                for thickness in pipe_thickness:
                    if thickness in items.item_code:
                        print('Pipe Thickness: {}'.format(thickness))

        if resolution == '2':
            if period in ['This Month', 'Last Month']:
                if date.strftime("%A") == 'Sunday':
                    week_no += 1
                    total_pipe_sold_labels.append("Week {}".format(week_no))
                else:
                    total_pipe_sold_labels.append(str(day+1))
                temp_total_pipe_sold_data_array.append(total_pipe_sold)
                total_pipe_sold = 0
            elif period in ['This Quarter', 'Last Quarter']:
                if date.strftime("%A") == 'Sunday':
                    week_no += 1
                    total_pipe_sold_labels.append("Week {}".format(week_no))
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1:
                    week_no += 1
                    total_pipe_sold_labels.append("Week {}".format(week_no))
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
            elif period in ['This Year', 'Last Year']:
                if date.day == 30:
                    total_pipe_sold_labels.append(month[date.month - 1])
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1:
                    total_pipe_sold_labels.append(month[date.month - 1])
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0

        elif resolution == '1':
            if period in ['This Month', 'Last Month']:
                if date.strftime("%A") == 'Sunday':
                    week_no += 1
                    total_pipe_sold_labels.append("Week {}".format(week_no))
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1:
                    week_no += 1
                    total_pipe_sold_labels.append("Week {}".format(week_no))
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
            elif period in ['This Quarter', 'Last Quarter']:
                if date.day == 30:
                    total_pipe_sold_labels.append(month[date.month - 1])
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1 and period != 'Last Quarter':
                    total_pipe_sold_labels.append(month[date.month - 1])
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
            elif period in ['This Year', 'Last Year']:
                if date.month % 3 == 0 and date.day == 30:
                    print("date.month%3 = {0} and month: {1}".format(
                        date.month % 3, date.month))
                    temp_month = "{0} {1}".format(
                        month[date.month - 1], date.year)
                    total_pipe_sold_labels.append(temp_month)
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0
                elif day == days-1:
                    temp_month = "{0} {1}".format(
                        month[date.month - 1], date.year)
                    total_pipe_sold_labels.append(temp_month)
                    temp_total_pipe_sold_data_array.append(total_pipe_sold)
                    total_pipe_sold = 0

    # Finalizing Total Pipe sold Data
    total_pipe_sold_data['labels'] = total_pipe_sold_labels
    temp_total_pipe_sold_data_dict['values'] = temp_total_pipe_sold_data_array
    total_pipe_sold_datasets.append(temp_total_pipe_sold_data_dict)
    total_pipe_sold_data['datasets'] = total_pipe_sold_datasets
    # Finalizing Individual Pipe Sold Data
    individual_pipe_sold_data['labels'] = individual_pipe_sold_labels
    temp_individual_pipe_sold_data_dict['values'] = temp_individual_pipe_sold_data_array
    individual_pipe_sold_datasets.append(temp_individual_pipe_sold_data_dict)
    individual_pipe_sold_data['datasets'] = individual_pipe_sold_datasets
    print(individual_pipe_sold_data)
    # Finalizing Individual Pipe Sold Data
    thickness_pipe_sold_data['labels'] = thickness_pipe_sold_labels
    temp_thickness_pipe_sold_data_dict['values'] = temp_thickness_pipe_sold_data_array
    thickness_pipe_sold_datasets.append(temp_thickness_pipe_sold_data_dict)
    thickness_pipe_sold_data['datasets'] = thickness_pipe_sold_datasets

    dummy = 'This is dummy data'
    return [total_pipe_sold_data, individual_pipe_sold_data]
