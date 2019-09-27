import mysql.connector
import json

mydb = mysql.connector.connect(
  host="192.168.10.18",
  user="ahmad",
  passwd="LHR736!7331Gr"
)
idx = 0
id_num = 0
sizes = ['1/2 INCH','3/4 INCH','1 INCH','1 1/4 INCH','1 1/2 INCH','2 INCH','2 1/2 INCH','3 INCH','4 INCH','5 INCH','6 INCH','7 INCH','8 INCH','10 INCH','12 INCH']
size_id = ['pipe1_2inch','pipe3_4inch','pipe1inch','pipe11_4inch','pipe11/2inch','pipe2inch','pipe21_2inch','pipe3inch','pipe4inch','pipe5inch','pipe6inch','pipe7inch','pipe8inch','pipe10inch','pipe12inch']
callbackreturn = {}
for pipe_size in sizes:
    # print(pipe_size)
    i = 0
    mycursor = mydb.cursor()
    mycursor.execute('''SELECT item_code,warehouse,actual_qty FROM _4e363c9bf0b93422.tabBin WHERE item_code LIKE 'Pipe-MS-{0}%' AND actual_qty>0'''.format(pipe_size))
    myresult = mycursor.fetchall()
    if (myresult):
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
            callbackreturn[size_id[id_num]][i] = {'thickness': thickness[0], 'length': length[0], 'Qty': str(round(x[2],2))}
            i += 1
            # datastr = "Size: {0} | Thickness: {1} | Length: {2} | warehouse: {3} | Qty: {4}".format(size[0],thickness[0],length[0],x[1],str(round(x[2],2)))
            # print(datastr)
            idx +=1
    id_num +=1


# print(callbackreturn)
# print("***********")
json_return = json.dumps(callbackreturn)
print(idx)
print(json_return)