import frappe
import mysql.connector
import json
import xlsxwriter
import time
import io
from datetime import date, datetime
from string import ascii_uppercase
from frappe.utils import get_site_name, get_site_info, get_site_base_path, get_site_path, get_files_path, get_bench_path, get_site_url, get_datetime


@frappe.whitelist()
def get_charges_account(steel_pipes_charges_settings):
    charges_doc = frappe.get_doc(steel_pipes_charges_settings)
    return {'loading_head': charges_doc.loading_account_head, 'cutting_labor_head': charges_doc.cutting_labor_account_head, 'transport_head': charges_doc.transport_account_head}


# Pipe Stock Summary Sheet
@ frappe.whitelist()
def get_pipe_stock(warehouse):
    xlsx_name = '/tmp/pipstocksheet-{0}.xlsx'.format(warehouse)
    # Creating file
    workbook = xlsxwriter.Workbook(xlsx_name)
    # Creating Worksheet
    worksheet = workbook.add_worksheet(name=warehouse)
    # Setting column width
    worksheet.set_column(1, 24, 6)
    border = workbook.add_format()
    border.set_align('center')
    border.set_align('vcenter')
    border.set_border()
    for row in range(0, 61, 1):
        for column in range(0, 24, 1):
            worksheet.write(row, column, None, border)
    # Setting Formats
    bold = workbook.add_format({'bold': True})
    bold.set_border()
    format6 = workbook.add_format(
        {'num_format': 'dd/mm/yyyy hh:mm AM/PM', 'bold': True})
    merge_format = workbook.add_format({'align': 'center', 'bold': True})
    merge_format.set_border()

    worksheet.write('A1', str(warehouse), bold)
    now = datetime.now()
    worksheet.write('F1', now.strftime("%B %d, %Y %H:%M:%S"), format6)
    cellTitle = 0
    cellTitlerow = 2

    id_num = 0
    sizes = ['1/2 INCH', '3/4 INCH', '1 INCH', '1 1/4 INCH', '1 1/2 INCH', '2 INCH', '2 1/2 INCH',
             '3 INCH', '4 INCH', '5 INCH', '6 INCH', '7 INCH', '8 INCH', '10 INCH', '12 INCH']
    size_id = ['pipe1_2inch', 'pipe3_4inch', 'pipe1inch', 'pipe11_4inch', 'pipe11_2inch', 'pipe2inch', 'pipe21_2inch',
               'pipe3inch', 'pipe4inch', 'pipe5inch', 'pipe6inch', 'pipe7inch', 'pipe8inch', 'pipe10inch', 'pipe12inch']
    callbackreturn = {}
    for pipe_size in sizes:
        # print(pipe_size)
        i = 0
        myresult = frappe.db.get_list('Bin',
                                      filters={
                                          'warehouse': warehouse,
                                          'actual_qty': ['>', '0'],
                                          'item_code': ['like', 'Pipe-MS-{0}%'.format(pipe_size)]
                                      },
                                      fields=['item_code',
                                              'warehouse', 'actual_qty'],
                                      page_length=2000000000)
        

        if (myresult):
            tempTitle = ascii_uppercase[cellTitle] + str(cellTitlerow)
            worksheet.write(tempTitle, pipe_size, bold)
            mergetitle = ascii_uppercase[cellTitle] + str(
                cellTitlerow) + ':' + ascii_uppercase[cellTitle+3] + str(cellTitlerow)
            worksheet.merge_range(mergetitle, pipe_size, bold)
            worksheet.write(
                ascii_uppercase[cellTitle]+str(cellTitlerow+1), 'MM', bold)
            worksheet.write(
                ascii_uppercase[cellTitle+1]+str(cellTitlerow+1), 'FEET', bold)
            worksheet.write(
                ascii_uppercase[cellTitle+2]+str(cellTitlerow+1), 'QTY', bold)
            worksheet.write(
                ascii_uppercase[cellTitle+3]+str(cellTitlerow+1), 'KG', bold)

            callbackreturn[size_id[id_num]] = {}
            for x in myresult:
                print(x.item_code)
                thickness = frappe.db.get_list('Item Variant Attribute',
                                               filters={
                                                   'parent': x.item_code,
                                                   'attribute': 'Thickness (mm)'
                                               },
                                               fields=['attribute_value'],
                                               page_length=2000000000)
                print(thickness[0].attribute_value)
                length = frappe.db.get_list('Item Variant Attribute',
                                            filters={
                                                'parent': x.item_code,
                                                'attribute': 'Length (feet)'
                                            },
                                            fields=['attribute_value'],
                                            page_length=2000000000)
                print(length[0].attribute_value)
                item = frappe.get_doc('Item', x.item_code)
                print(item)
                pipe_weight = '-'
                for w in item.receiving_details:
                    if w:
                        if w.receiving_warehouse == warehouse:
                            pipe_weight = w.scale_weight
                callbackreturn[size_id[id_num]][i] = {'thickness': str(thickness[0].attribute_value), 'length': str(
                    length[0].attribute_value), 'qty': str(round(x.actual_qty, 2)), 'weight': str(pipe_weight)}
                worksheet.write(
                    ascii_uppercase[cellTitle]+str(cellTitlerow+2 + i), (float(thickness[0].attribute_value)), border)
                worksheet.write(
                    ascii_uppercase[cellTitle+1]+str(cellTitlerow+2 + i), (float(length[0].attribute_value)), border)
                worksheet.write(
                    ascii_uppercase[cellTitle+2]+str(cellTitlerow+2 + i), (round(x.actual_qty, 2)), border)
                worksheet.write(
                    ascii_uppercase[cellTitle+3]+str(cellTitlerow+2 + i), pipe_weight, border)
                i += 1
            cellTitle += 4
            if cellTitle == 24:
                cellTitle = 0
                cellTitlerow += 30
        id_num += 1
    callbackreturn = json.dumps(callbackreturn)

    workbook.close()
    return callbackreturn


@frappe.whitelist()
def generate_xlsx_item_stock(warehouse):
    file = io.open(
        '/tmp/pipstocksheet-{0}.xlsx'.format(warehouse), "rb", buffering=0)
    data = file.read()
    if not data:
        frappe.msgprint(('No Data'))
        return
    frappe.local.response.filecontent = data
    frappe.local.response.type = "download"
    frappe.local.response.filename = "pipestocksheet-{0}.xlsx".format(
        warehouse)


def update_delivered_item_weight_statistics(self, cdt):
    for d in self.items:
        if 'Pipe-MS' in str(d.item_code):
            item = frappe.get_doc('Item', d.item_code)
            item.db_set('last_weight_delivered', d.scale_weight_um)
            item.db_set('last_quantity_delivered', d.qty)


def update_received_item_weight_statistics(self, cdt):
    for d in self.items:
        if 'Pipe-MS' in str(d.item_code):
            item = frappe.get_doc('Item', d.item_code)
            item.db_set('last_weight_received', d.scale_weight_um)
            item.db_set('last_quantity_received', d.qty)
