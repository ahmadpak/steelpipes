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
import json


class SupplierBalanceReportGenerator(Document):
    pass


@frappe.whitelist()
def generate_supplier_balance(data=None):
    data = json.loads(data)
    file_name = get_file_name(data)

    workbook = xlsxwriter.Workbook(
        '{0}'.format(file_name))			# Creating a xlsx file
    worksheet = workbook.add_worksheet(
        name='supplier-balance')		# Adding new worksheet
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

    # Todays Time and date
    now = datetime.now()
    worksheet.write(0, 0,  now.strftime("%B %d, %Y %H:%M:%S"), format6)

    # Creating Party String
    partystr = ''
    if data['supplier_group'] not in ['', None]:
        partystr = 'Supplier Group: {0} | '.format(data['supplier_group'])
    if data['supplier_type'] not in ['', None]:
        partystr += 'Supplier Type: {0} | '.format(data['supplier_type'])

    worksheet.merge_range('B1:H1', partystr, merge_right)

    # Creating balance string
    balancestr = ''
    if data['all_balances'] == 1 and data['get_advances'] == 0:
        balancestr = 'All Balances'
    elif data['all_balances'] == 1 and data['get_advances'] == 1:
        balancestr = 'All Advances'
    elif data['all_balances'] == 0 and data['get_advances'] == 0:
        balancestr = 'Balance less than ' + str(data['balance_less_than'])
    elif data['all_balances'] == 0 and data['get_advances'] == 1:
        balancestr = 'Advances less than ' + str(data['balance_less_than'])
    worksheet.merge_range('A2:H2', balancestr, merge_center)

    # Creating Balance section
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

    # Adding up balances
    supplier_list = frappe.db.get_list('Supplier', filters={'disabled': 'No'}, fields=[
                                       'name'], page_length=2000000000)
    balances = get_balances(data, supplier_list)

    # Arranging list
    for i in range(len(balances)):
        if i+1 < len(balances):
            if balances[i]['balance'] > balances[i+1]['balance']:
                a = balances[i]
                balances[i] = balances[i+1]
                balances[i+1] = a

    # Inserting data into Sheet
    for balance in balances:
        sup = frappe.db.get_list('Supplier', filters={'name': balance['name']}, fields=[
                                 'supplier_group', 'supplier_type', 'last_balance_comparison_date', 'balance_matched', 'last_payment_date', 'last_payment_amount'])
        goahead = 1
        if data['supplier_group'] not in ['', None]:
            if sup[0].supplier_group != data['supplier_group']:
                goahead = 0
        if data['supplier_type'] not in ['', None]:
            if sup[0].supplier_type != data['supplier_type']:
                goahead = 0
        if goahead == 1:
            worksheet.set_row(current_row, 19.5)
            if cell_col == 0:
                # name,last_payment_date,last_payment_amount,balance
                worksheet.write(current_row, 0, balance['name'],
                                cell_format_comic_sans_ms)
                if sup[0].last_payment_date == None:
                    worksheet.write(current_row, 1, '-',
                                    cell_format_arial_date)
                else:
                    worksheet.write(
                        current_row, 1, sup[0].last_payment_date, cell_format_arial_date)
                if sup[0].last_payment_amount == None or sup[0].last_payment_amount == 0:
                    worksheet.write(current_row, 2, '-', cell_format_arial)
                else:
                    worksheet.write(
                        current_row, 2, sup[0].last_payment_amount, cell_format_arial)
                worksheet.write(
                    current_row, 3, balance['balance'], cell_format_arial)
                cell_col = 1
            else:
                    # name,last_payment_date,last_payment_amount,balance
                worksheet.write(current_row, 4, balance['name'],
                                cell_format_comic_sans_ms)
                if sup[0].last_payment_date == None:
                    worksheet.write(current_row, 5, '-',
                                    cell_format_arial_date)
                else:
                    worksheet.write(
                        current_row, 5, sup[0].last_payment_date, cell_format_arial_date)
                if sup[0].last_payment_amount == None or sup[0].last_payment_amount == 0:
                    worksheet.write(current_row, 6, '-', cell_format_arial)
                else:
                    worksheet.write(
                        current_row, 6, sup[0].last_payment_amount, cell_format_arial)
                worksheet.write(
                    current_row, 7, balance['balance'], cell_format_arial)
                cell_col = 0
            if cell_col == 0:
                current_row += 1

    workbook.close()


def get_file_name(data=None):
    if data['all_balances'] == 0 and data['get_advances'] == 0:
        filestr = '/tmp/supplier_balance_{0}.xlsx'.format(
            data['balance_less_than'])
    elif data['all_balances'] == 0 and data['get_advances'] == 1:
        filestr = '/tmp/supplier_advances_{0}.xlsx'.format(
            data['balance_less_than'])
    elif data['all_balances'] == 1 and data['get_advances'] == 0:
        filestr = '/tmp/supplier_balance.xlsx'
    elif data['all_balances'] == 1 and data['get_advances'] == 1:
        filestr = '/tmp/supplier_advances.xlsx'
    return filestr


def get_balances(data, supplier_list):
    balances = []
    temp_dict = {}
    for supplier in supplier_list:

        temp_dict['name'] = supplier.name
        temp_dict['balance'] = -get_balance_on(date=date.today(
        ), party_type='Supplier', party=supplier.name, company=data['company'])

        if data['all_balances'] == 0 and data['get_advances'] == 0:
            if data['balance_less_than']>=temp_dict['balance']>0:
                balances.append(temp_dict)
        if data['all_balances'] == 0 and data['get_advances'] == 1:
            if data['balance_less_than']<=temp_dict['balance']<0:
                balances.append(temp_dict)
        if data['all_balances'] == 1 and data['get_advances'] == 0:
            if temp_dict['balance']>0:
                balances.append(temp_dict)
        if data['all_balances'] == 1 and data['get_advances'] == 1:
            if temp_dict['balance']<0:
                balances.append(temp_dict)
        temp_dict = {}

    return balances


@frappe.whitelist()
def generate_xlsx_supplier_balance():
    doc = frappe.get_doc('Supplier Balance Report Generator')
    file_path = get_file_name_xlsx(
        doc.balance_less_than, doc.get_advances, doc.all_balances)
    file_name = get_download_file_name(doc.balance_less_than, doc.get_advances, doc.all_balances)
    file = io.open(file_path, "rb", buffering=0)
    data = file.read()
    if not data:
        frappe.msgprint(('No Data'))
        return
    frappe.local.response.filecontent = data
    frappe.local.response.type = "download"
    frappe.local.response.filename = file_name


def get_download_file_name(balance_less_than, get_advances, all_balances):
    filestr = None
    if all_balances == 0 and get_advances == 0:
        filestr = 'supplier_balance_{0}.xlsx'.format(balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        filestr = 'supplier_advances_{0}.xlsx'.format(balance_less_than)
    elif all_balances == 1 and get_advances == 0:
        filestr = 'supplier_balance.xlsx'
    elif all_balances == 1 and get_advances == 1:
        filestr = 'supplier_advances.xlsx'
    return filestr


def get_file_name_xlsx(balance_less_than, get_advances, all_balances):
    filestr = None
    if all_balances == 0 and get_advances == 0:
        filestr = '/tmp/supplier_balance_{}.xlsx'.format(balance_less_than)
    elif all_balances == 0 and get_advances == 1:
        filestr = '/tmp/supplier_advances_{}.xlsx'.format(balance_less_than)
    elif all_balances == 1 and get_advances == 0:
        filestr = '/tmp/supplier_balance.xlsx'
    elif all_balances == 1 and get_advances == 1:
        filestr = '/tmp/supplier_advances.xlsx'
    return filestr
