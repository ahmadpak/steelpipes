# -*- coding: utf-8 -*-
# Copyright (c) 2019, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.accounts.utils import get_balance_on
import xlsxwriter
from datetime import date, datetime
import io
from datetime import date, datetime
from string import ascii_uppercase


class CustomerBalanceReportGenerator(Document):
    pass


@frappe.whitelist()
def generate_customer_balance(company=None, customer_group=None, territory=None, sales_person=None, balance_less_than=None, get_advances=0, all_balances=0):
    get_advances = int(get_advances)
    all_balances = int(all_balances)
    balance_less_than = int(balance_less_than)
    now = datetime.now()
    file_name = get_file_name(
        sales_person, balance_less_than, get_advances, all_balances)

    workbook = xlsxwriter.Workbook(
        '{0}'.format(file_name))			# Creating a xlsx file
    worksheet = workbook.add_worksheet(
        name='customer-balance')		# Adding new worksheet
    # Setting column widths
    worksheet.set_column(0, 0, 30.5)
    worksheet.set_column(1, 1, 15.3)
    worksheet.set_row(0, 20.25)
    worksheet.set_row(1, 20.25)
    worksheet.set_row(2, 20.25)
    worksheet.set_column(4, 4, 30.5)
    worksheet.set_column(5, 5, 15.3)
    worksheet.set_column(2, 3, 12.67)
    worksheet.set_column(6, 7, 12.67)
    # Creating Border formats
    cell_format_font_14 = workbook.add_format(
        {'bold': True, 'font': 'Calibri', 'font_size': 11})
    cell_format_font_14.set_border()
    cell_format_font_14.set_align('vcenter')
    cell_format_font_14.set_align('center')
    format6 = workbook.add_format(
        {'num_format': 'dd/mm/yyyy hh:mm AM/PM', 'bold': True})
    # Creating Merge format
    merge_right = workbook.add_format(
        {'align': 'right', 'bold': True, 'font': 'Calibri', 'font_size': 11})
    merge_right.set_border()
    merge_right.set_align('vcenter')
    merge_center = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Calibri', 'font_size': 11})
    merge_center.set_border()
    merge_center.set_align('vcenter')

    # datestr = 'Date: ' + str(now)
    worksheet.write(0, 0,  now.strftime("%B %d, %Y %H:%M:%S"), format6)
    partystr = ''
    if customer_group:
        partystr = 'Customer Group: {0} | '.format(customer_group)
    if territory:
        partystr += 'Territory: {0} | '.format(territory)
    if sales_person == None:
        partystr += 'Parties: All Customers'
    else:
        partystr += 'Parties: ' + str(sales_person) + ' Customers'
    worksheet.merge_range('B1:H1', partystr, merge_right)

    balancestr = ''
    if all_balances == 1 and get_advances == 0:
        balancestr = 'All Balances'
    elif all_balances == 1 and get_advances == 1:
        balancestr = 'All Advances'
    elif all_balances == 0 and get_advances == 0:
        balancestr = 'Balance less than ' + str(balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        balancestr = 'Advances less than ' + str(balance_less_than)
    worksheet.merge_range('A2:H2', balancestr, merge_center)

    cell_format = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Calibri', 'font_size': 11})
    cell_format.set_border()
    cell_format.set_align('vcenter')
    worksheet.write(2, 0, 'Parties', cell_format)
    worksheet.write(2, 4, 'Parties', cell_format)
    cell_format = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Calibri', 'font_size': 9})
    cell_format.set_border()
    cell_format.set_align('vcenter')
    worksheet.write(2, 1, 'LAST DATE', cell_format)
    worksheet.write(2, 2, 'LAST PAID', cell_format)
    worksheet.write(2, 5, 'LAST DATE', cell_format)
    worksheet.write(2, 6, 'LAST PAID', cell_format)
    cell_format = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Arial', 'font_size': 9})
    cell_format.set_align('vcenter')
    cell_format.set_border()
    worksheet.write(2, 3, 'OUTSTANDING', cell_format)
    worksheet.write(2, 7, 'OUTSTANDING', cell_format)

    # Adding up balances
    customer_list = get_customer_balance_list(
        company, customer_group, territory, sales_person, balance_less_than, get_advances, all_balances)
    cell_col = 0
    cell_format_arial = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Arial', 'font_size': 10, 'num_format': '#,##,###'})
    cell_format_arial.set_align('vcenter')
    cell_format_arial.set_border()
    cell_format_arial_date = workbook.add_format(
        {'align': 'center', 'bold': True, 'font': 'Arial', 'font_size': 10})
    cell_format_arial_date.set_align('vcenter')
    cell_format_arial_date.set_border()
    cell_format_arial_date.set_num_format('d mmmm yyyy')
    cell_format_comic_sans_ms = workbook.add_format(
        {'align': 'left', 'bold': True, 'font': 'Calibri', 'font_size': 10})
    cell_format_comic_sans_ms.set_align('vcenter')
    cell_format_comic_sans_ms.set_border()
    current_row = 3
    for i in customer_list:
        worksheet.set_row(current_row, 19.5)
        if sales_person:
            sql_query_str = '''SELECT parent,sales_person FROM `tabSales Team` WHERE parent='{0}' AND sales_person='{1}';'''.format(
                i.name, sales_person)
            sql_query = frappe.db.sql(sql_query_str, as_dict=True)
            if sql_query:
                if cell_col == 0:
                    # name,last_payment_date,last_payment_amount,outstanding_balance
                    worksheet.write(current_row, 0, i.name,
                                    cell_format_comic_sans_ms)
                    if i.last_payment_date == None:
                        worksheet.write(current_row, 1, '-',
                                        cell_format_arial_date)
                    else:
                        worksheet.write(
                            current_row, 1, i.last_payment_date, cell_format_arial_date)
                    if i.last_payment_amount == None or i.last_payment_amount == 0:
                        worksheet.write(current_row, 2, '-', cell_format_arial)
                    else:
                        worksheet.write(
                            current_row, 2, i.last_payment_amount, cell_format_arial)
                    worksheet.write(
                        current_row, 3, i.outstanding_balance, cell_format_arial)
                    cell_col = 1
                else:
                    # name,last_payment_date,last_payment_amount,outstanding_balance
                    worksheet.write(current_row, 4, i.name,
                                    cell_format_comic_sans_ms)
                    if i.last_payment_date == None:
                        worksheet.write(current_row, 5, '-',
                                        cell_format_arial_date)
                    else:
                        worksheet.write(
                            current_row, 5, i.last_payment_date, cell_format_arial_date)
                    if i.last_payment_amount == None or i.last_payment_amount == 0:
                        worksheet.write(current_row, 6, '-', cell_format_arial)
                    else:
                        worksheet.write(
                            current_row, 6, i.last_payment_amount, cell_format_arial)
                    worksheet.write(
                        current_row, 7, i.outstanding_balance, cell_format_arial)
                    cell_col = 0
                if cell_col == 0:
                    current_row += 1
        else:
            if cell_col == 0:
                # name,last_payment_date,last_payment_amount,outstanding_balance
                worksheet.write(current_row, 0, i.name,
                                cell_format_comic_sans_ms)
                if i.last_payment_date == None:
                    worksheet.write(current_row, 1, '-',
                                    cell_format_arial_date)
                else:
                    worksheet.write(
                        current_row, 1, i.last_payment_date, cell_format_arial_date)
                if i.last_payment_amount == None or i.last_payment_amount == 0:
                    worksheet.write(current_row, 2, '-', cell_format_arial)
                else:
                    worksheet.write(
                        current_row, 2, i.last_payment_amount, cell_format_arial)
                worksheet.write(
                    current_row, 3, i.outstanding_balance, cell_format_arial)
                cell_col = 1
            else:
                # name,last_payment_date,last_payment_amount,outstanding_balance
                worksheet.write(current_row, 4, i.name,
                                cell_format_comic_sans_ms)
                if i.last_payment_date == None:
                    worksheet.write(current_row, 5, '-',
                                    cell_format_arial_date)
                else:
                    worksheet.write(
                        current_row, 5, i.last_payment_date, cell_format_arial_date)
                if i.last_payment_amount == None or i.last_payment_amount == 0:
                    worksheet.write(current_row, 6, '-', cell_format_arial)
                else:
                    worksheet.write(
                        current_row, 6, i.last_payment_amount, cell_format_arial)
                worksheet.write(
                    current_row, 7, i.outstanding_balance, cell_format_arial)
                cell_col = 0
            if cell_col == 0:
                current_row += 1

    workbook.close()


def get_file_name(sales_person, balance_less_than, get_advances, all_balances):
    filestr = None
    sp_str = None
    if sales_person:
        sp_str = str(sales_person) + '_'
    else:
        sp_str = ''
    if all_balances == 0 and get_advances == 0:
        filestr = '/tmp/{0}customer_balance_{1}.xlsx'.format(
            sp_str, balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        filestr = '/tmp/{0}customer_advances_{1}.xlsx'.format(
            sp_str, balance_less_than)
    elif all_balances == 1 and get_advances == 0:
        filestr = '/tmp/{0}customer_balance.xlsx'.format(sp_str)
    elif all_balances == 1 and get_advances == 1:
        filestr = '/tmp/{0}customer_advances.xlsx'.format(sp_str)
    return filestr


def get_customer_balance_list(company=None, customer_group=None, territory=None, sales_person=None, balance_less_than=None, get_advances=0, all_balances=0):
    customer_list = None
    customer_list = frappe.get_list(
        'Customer', filters={'Disabled': 'No'}, page_length=100000)

    for customer in customer_list:
        outstanding_balance = get_balance_on(
            date=date.today(), party_type='Customer', party=customer.name, company=company)
        frappe.db.set_value('Customer', customer.name,
                            'outstanding_balance', outstanding_balance)

    sql_query_str = get_filters(company, customer_group, territory,
                                sales_person, balance_less_than, get_advances, all_balances)
    customer_list = frappe.db.sql(sql_query_str, as_dict=True)
    return customer_list


def get_filters(company=None, customer_group=None, territory=None, sales_person=None, balance_less_than=None, get_advances=0, all_balances=0):
    sql_query_str = 'SELECT name,last_payment_date,last_payment_amount,outstanding_balance FROM tabCustomer WHERE'
    if customer_group:
        sql_query_str += ' customer_group="{0}" AND'.format(customer_group)
    if territory:
        sql_query_str += ' territory="{0}" AND'.format(territory)
    if all_balances == 0 and get_advances == 0:
        sql_query_str += ' outstanding_balance BETWEEN 1 AND {0}  ORDER BY outstanding_balance ASC LIMIT 1000000000;'.format(
            balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        sql_query_str += ' outstanding_balance BETWEEN {0} AND -1  ORDER BY outstanding_balance DESC LIMIT 1000000000;'.format(
            balance_less_than)
    elif all_balances == 1 and get_advances == 0:
        sql_query_str += ' outstanding_balance BETWEEN 1 AND 1000000000000  ORDER BY outstanding_balance ASC LIMIT 1000000000;'
    elif all_balances == 1 and get_advances == 1:
        sql_query_str += ' outstanding_balance BETWEEN -1000000000000 AND -1  ORDER BY outstanding_balance DESC LIMIT 1000000000;'
    return sql_query_str


@frappe.whitelist()
def generate_xlsx_customer_balance():
    doc = frappe.get_doc('Customer Balance Report Generator')
    file_path = get_file_name(
        doc.sales_person, doc.balance_less_than, doc.get_advances, doc.all_balances)
    file_name = get_download_file_name(
        doc.sales_person, doc.balance_less_than, doc.get_advances, doc.all_balances)
    file = io.open(file_path, "rb", buffering=0)
    data = file.read()
    if not data:
        frappe.msgprint(('No Data'))
        return
    frappe.local.response.filecontent = data
    frappe.local.response.type = "download"
    frappe.local.response.filename = file_name


def get_download_file_name(sales_person, balance_less_than, get_advances, all_balances):
    filestr = None
    sp_str = None
    if sales_person:
        sp_str = str(sales_person) + '_'
    else:
        sp_str = ''
    if all_balances == 0 and get_advances == 0:
        filestr = '{0}customer_balance_{1}.xlsx'.format(
            sp_str, balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        filestr = '{0}customer_advances_{1}.xlsx'.format(
            sp_str, balance_less_than)
    elif all_balances == 1 and get_advances == 0:
        filestr = '{0}customer_balance.xlsx'.format(sp_str)
    elif all_balances == 1 and get_advances == 1:
        filestr = '{0}customer_advances.xlsx'.format(sp_str)
    return filestr
