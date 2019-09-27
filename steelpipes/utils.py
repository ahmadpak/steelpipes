import frappe
import mysql.connector
import json
import xlsxwriter
import time
import io
from datetime import date,datetime
from string import ascii_uppercase
from frappe.utils import get_site_name,get_site_info,get_site_base_path,get_site_path,get_files_path,get_bench_path,get_site_url,get_datetime

@frappe.whitelist()
def get_charges_account(steel_pipes_charges_settings):
    charges_doc = frappe.get_doc(steel_pipes_charges_settings)
    return {'loading_head': charges_doc.loading_account_head, 'cutting_labor_head': charges_doc.cutting_labor_account_head, 'transport_head': charges_doc.transport_account_head}

@ frappe.whitelist()
def get_pipe_stock(warehouse):
    # Connecting to database
    report_settings = frappe.get_doc('Pipe Stock Summary Setting')
    mydb = mysql.connector.connect(
        host=report_settings.host,
        user=report_settings.user,
        passwd=report_settings.password
    )
    workbook = xlsxwriter.Workbook('/tmp/pipstocksheet.xlsx')                                   # Creating file
    worksheet = workbook.add_worksheet(name=warehouse)                                          # Creating Worksheet
    worksheet.set_column(1, 24, 6)                                                              # Setting column width
    border = workbook.add_format()
    border.set_border()
    for row in range(0,61,1):
        for column in range(0,24,1):
            worksheet.write(row,column,None,border)
    # Setting Formats
    bold = workbook.add_format({'bold': True})
    bold.set_border()
    format6 = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm AM/PM','bold':True})
    merge_format = workbook.add_format({'align': 'center','bold':True})
    merge_format.set_border()
    
    worksheet.write('A1', str(warehouse),bold)
    now = datetime.now()
    worksheet.write('F1', now.strftime("%B %d, %Y %H:%M:%S"),format6)
    cellTitle = 0
    cellTitlerow = 2
    cellThickness = ''
    cellLength = ''
    cellQty = ''
    cellWeight = ''
    # worksheet.write('A1', 'Hello world')

    id_num = 0
    sizes = ['1/2 INCH','3/4 INCH','1 INCH','1 1/4 INCH','1 1/2 INCH','2 INCH','2 1/2 INCH','3 INCH','4 INCH','5 INCH','6 INCH','7 INCH','8 INCH','10 INCH','12 INCH']
    size_id = ['pipe1_2inch','pipe3_4inch','pipe1inch','pipe11_4inch','pipe11_2inch','pipe2inch','pipe21_2inch','pipe3inch','pipe4inch','pipe5inch','pipe6inch','pipe7inch','pipe8inch','pipe10inch','pipe12inch']
    callbackreturn = {}
    for pipe_size in sizes:
        # print(pipe_size)
        i = 0 
        
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT item_code,warehouse,actual_qty FROM _4e363c9bf0b93422.tabBin WHERE item_code LIKE 'Pipe-MS-{0}%' AND actual_qty>0 AND warehouse LIKE "{1}"'''.format(pipe_size,warehouse))
        myresult = mycursor.fetchall()
        if (myresult):
            tempTitle = ascii_uppercase[cellTitle] +str(cellTitlerow)
            worksheet.write(tempTitle, pipe_size,bold)
            mergetitle = ascii_uppercase[cellTitle] +str(cellTitlerow) + ':' + ascii_uppercase[cellTitle+3] +str(cellTitlerow)
            worksheet.merge_range(mergetitle, pipe_size, bold)
            worksheet.write(ascii_uppercase[cellTitle]+str(cellTitlerow+1), 'MM',bold)
            worksheet.write(ascii_uppercase[cellTitle+1]+str(cellTitlerow+1), 'FEET',bold)
            worksheet.write(ascii_uppercase[cellTitle+2]+str(cellTitlerow+1), 'QTY',bold)
            worksheet.write(ascii_uppercase[cellTitle+3]+str(cellTitlerow+1), 'KG',bold)
            
            callbackreturn[size_id[id_num]] = {}
            for x in myresult:
                # sqlstr = """SELECT attribute_value FROM _4e363c9bf0b93422.`tabItem Variant Attribute` 
                #             WHERE parent LIKE '{0}' 
                #             AND attribute LIKE 'Size (inches)'""".format(x[0])
                # mycursor.execute(sqlstr)
                # size = mycursor.fetchone()

                sqlstr = """SELECT attribute_value FROM _4e363c9bf0b93422.`tabItem Variant Attribute` 
                            WHERE parent LIKE '{0}' 
                            AND attribute LIKE 'Thickness (mm)'""".format(x[0])
                mycursor.execute(sqlstr)
                thickness = mycursor.fetchone()

                sqlstr = """SELECT attribute_value FROM _4e363c9bf0b93422.`tabItem Variant Attribute` 
                            WHERE parent LIKE '{0}' 
                            AND attribute LIKE 'Length (feet)'""".format(x[0])
                mycursor.execute(sqlstr)
                length = mycursor.fetchone()
                callbackreturn[size_id[id_num]][i] = {'thickness': str(thickness[0]), 'length': str(length[0]), 'qty': str(round(x[2],2)), 'weight': '---'}
                worksheet.write(ascii_uppercase[cellTitle]+str(cellTitlerow+2 + i), str(thickness[0]),border)
                worksheet.write(ascii_uppercase[cellTitle+1]+str(cellTitlerow+2 + i), str(length[0]),border)
                worksheet.write(ascii_uppercase[cellTitle+2]+str(cellTitlerow+2 + i), str(round(x[2],2)),border)
                worksheet.write(ascii_uppercase[cellTitle+3]+str(cellTitlerow+2 + i), '---',border)
                i += 1
            cellTitle +=4
            if cellTitle == 24:
                cellTitle = 0
                cellTitlerow +=30
        id_num +=1
    callbackreturn = json.dumps(callbackreturn)
    # row 4 till 31
    # row
    # row 34 till 60
    # column 0 till 24 (1,25)
    # border = workbook.add_format()
    # border.set_border()
    # for row in range(4,32,1):
    #     for column in range(0,24,1):
    #         worksheet.write(row,column,None,border)
    # for row in range(34,61,1):
    #     for column in range(0,24,1):
    #         worksheet.write(row,column,None,border)

    workbook.close()
    return callbackreturn

@frappe.whitelist()
def generate_xlsx_item_stock():
    # get_site_name,get_site_info,get_site_base_path,get_site_path,get_files_path,get_bench_path,get_site_url
    # frappe.local.response.filename = "pipstocksheet.xlsx"
    # frappe.local.response.filecontent = read_file_content('/tmp/pipstocksheet.xlsx') # custom function
    # frappe.local.response.type = "download"
    file = io.open('/tmp/pipstocksheet.xlsx', "rb", buffering = 0)
    data = file.read()
    if not data:
        frappe.msgprint(_('No Data'))
        return
    frappe.local.response.filecontent = data
    frappe.local.response.type = "download"
    frappe.local.response.filename = "pipestocksheet.xlsx"