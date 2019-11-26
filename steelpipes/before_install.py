import frappe

def pipe_barcode(item):
    if "Pipe-MS" in str(item.item_code):
        # item_code_temp = "Pipe-MS"
        barcode = ''
        for d in item.attributes:
            attribute_name = str(d.attribute)
            
            if 'Size' in attribute_name:
                item_size_um = str(d.attribute_value)
                temp_size = ''
                for character in item_size_um:
                    if character != '/' and character!=' ':
                        temp_size += character
                # item_code_temp += '-{0} INCH'.format(item_size_um)
                barcode += temp_size
            elif 'Thickness' in attribute_name:
                item_thickness_um = str(d.attribute_value)
                temp_thickness = ''
                for character in item_thickness_um:
                    if character != ' ':
                        temp_thickness += character
                if len(temp_thickness)!=4:
                    temp_thickness +='0'
                # item_code_temp += "-{0} MM".format(temp_thickness)
                barcode += temp_thickness

            elif 'Length' in attribute_name:
                item_length_um = str(d.attribute_value)
                temp_length = ''
                for character in item_length_um:
                    if character != ' ':
                        temp_length += character
                # item_code_temp += "-{0} FT".format(temp_length)
                barcode += temp_length
        if item.barcodes:
            has_barcode = 0
            for d in item.barcodes:
                if d.barcode == barcode:
                    has_barcode = 1
            if has_barcode == 0:
                item.append('barcodes',{
                        'barcode':barcode
                    })
        else:                    
            item.append('barcodes',{
                'barcode':barcode
            })
        item.save()
        # item.description = item.item_code = item.item_name = item_code_temp

def create_strip_width(attribute,thickness,step,width):
    while (thickness< 8.04):
                if step == 0:
                    attribute.append('item_attribute_values', {
                        'attribute_value': str(width),
                        'abbr': str(width) + ' MM' 
                    })
                step +=1
                if step == 10:
                    width -=1
                    step = 0
                thickness += 0.05
                    

def create_strip_width_for_item_attribute(OD,strip_size_reduction):
    if OD == '26.7':
        width = 81 - strip_size_reduction
    elif OD == '33.5':
        width = 102 - strip_size_reduction
    elif OD == '42':
        width = 129 - strip_size_reduction
    elif OD == '48':
        width = 148 - strip_size_reduction
    elif OD == '60.3':
        width = 186 - strip_size_reduction
    elif OD == '76':
        width = 236 - strip_size_reduction
    elif OD == '88':
        width = 273 - strip_size_reduction
    elif OD == '113':
        width = 352 - strip_size_reduction
    elif OD == '140':
        width = 437 - strip_size_reduction
    elif OD == '165':
        width = 515 - strip_size_reduction
    elif OD == '190':
        width = 594 - strip_size_reduction
    elif OD == '216':
        width = 676 - strip_size_reduction
    elif OD == '266.5':
        width = 834 - strip_size_reduction
    elif OD == '324':
        width = 1015 - strip_size_reduction
    return str(width)

def create_pipe_ms_items():
    stock_setting = frappe.get_doc('Stock Settings')
    stock_setting.valuation_method = 'FIFO'
    stock_setting.show_barcode_field = 1,
    stock_setting.over_delivery_receipt_allowance = 10
    stock_setting.save()
    print('Valuation method: {0}'.format(stock_setting.valuation_method))
    print('show barcode: {0}'.format(stock_setting.show_barcode_field))
    item_group = frappe.new_doc('Item Group')
    item_group.item_group_name = 'Pipes'
    item_group.show_in_website = 1
    item_group.save()
    # Creating required attributes
    # Size (inches)
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Size (inches)'
    sizes = ['3/4','1','1 1/4','1 1/2','2','2 1/2','3','4','5','6','7','8','10','12']
    for size in sizes:
        attribute.append('item_attribute_values', {
            'attribute_value': size,
            'abbr': size + ' INCH'
        })
    attribute.save()

    # Material Type
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Material Type'
    attribute.append('item_attribute_values', {
        'attribute_value': 'MILD STEEL',
        'abbr': 'MS'
    })
    attribute.save()

    # Thickness (mm)
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Thickness (mm)'
    thickness = 1.05
    while thickness<8.04:
        thickness_str = ''
        if len(str(round(thickness,2)))==1:
            thickness_str = str(round(thickness,2)) + '.00'
        elif len(str(round(thickness,2)))==3:
            thickness_str = str(round(thickness,2)) + '0'
        else:
            thickness_str = str(round(thickness,2)) + ''
        attribute.append('item_attribute_values', {
            'attribute_value': str(round(thickness,2)),
            'abbr': thickness_str + ' MM'
        })
        thickness += 0.05
    attribute.save()

    # Length
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Length (feet)'
    attribute.append('item_attribute_values', {
            'attribute_value': '20',
            'abbr': '20 FT'
        })
    attribute.append('item_attribute_values', {
            'attribute_value': '10',
            'abbr': '10 FT'
        })
    attribute.save()

    # Outer Diameter
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Outer Diameter'
    ODs = ['26.7','33.5','42','48','60.3','76','88','113','140','165','190','216','266.5','324']
    for OD in ODs:
        attribute.append('item_attribute_values', {
            'attribute_value': OD,
            'abbr': 'OD ' + OD 
        })
    attribute.save()

    # Width (mm)
    attribute = frappe.new_doc('Item Attribute')
    attribute.attribute_name = 'Width (mm)'
    for OD in ODs:
        thickness = 1.05
        step = 0
        if OD == '26.7':
            width = 81
            create_strip_width(attribute,thickness,step,width)
        elif OD == '33.5':
            width = 102
            create_strip_width(attribute,thickness,step,width)
        elif OD == '42':
            width = 129
            create_strip_width(attribute,thickness,step,width)
        elif OD == '48':
            width = 148
            create_strip_width(attribute,thickness,step,width)
        elif OD == '60.3':
            width = 186
            create_strip_width(attribute,thickness,step,width)
        elif OD == '76':
            width = 236
            create_strip_width(attribute,thickness,step,width)
        elif OD == '88':
            width = 273
            create_strip_width(attribute,thickness,step,width)
        elif OD == '113':
            width = 352
            create_strip_width(attribute,thickness,step,width)
        elif OD == '140':
            width = 437
            create_strip_width(attribute,thickness,step,width)
        elif OD == '165':
            width = 515
            create_strip_width(attribute,thickness,step,width)
        elif OD == '190':
            width = 594
            create_strip_width(attribute,thickness,step,width)
        elif OD == '216':
            width = 676
            create_strip_width(attribute,thickness,step,width)
        elif OD == '266.5':
            width = 834
            create_strip_width(attribute,thickness,step,width)
        elif OD == '324':
            width = 1015
            create_strip_width(attribute,thickness,step,width)
    attribute.save()

    # Making Pipe Products
    item = frappe.new_doc('Item')
    item.item_code = 'Pipe'
    item.item_name = 'Pipe'
    item.item_group = 'Pipes'
    # item.uom = 'Nos'
    item.has_variants = 1
    item.append('attributes',{
        'attribute': 'Material Type'
    })
    item.append('attributes',{
        'attribute': 'Size (inches)'
    })
    item.append('attributes',{
        'attribute': 'Thickness (mm)'
    })
    item.append('attributes',{
        'attribute': 'Length (feet)'
    })
    item.append('attributes',{
        'attribute': 'Outer Diameter'
    })
    item.append('attributes',{
        'attribute': 'Width (mm)'
    })
    item.save()

    # Creating Pipe Variants for 10 and 20 Feet

    thickness = 1.05
    strip_size_reduction = 0
    step = 0
    while thickness<8.04:
        sr = 0
        for size in sizes:
            for pipe_length in ['10','20']:
                item = frappe.new_doc('Item')
                item.variant_of = 'Pipe'
                item.item_group = 'Pipes'
                item_code_str = 'Pipe-MS-'
                thickness_str = ''
                if len(str(round(thickness,2)))==1:
                    thickness_str = str(round(thickness,2)) + '.00 MM-'
                elif len(str(round(thickness,2)))==3:
                    thickness_str = str(round(thickness,2)) + '0 MM-'
                else:
                    thickness_str = str(round(thickness,2)) + ' MM-'
                item_code_str += size + ' INCH-' + thickness_str + pipe_length + ' FT'
                item.item_code = item_code_str
                item.item_name = item_code_str
                item.append('attributes',{
                    'attribute': 'Material Type',
                    'attribute_value': 'MILD STEEL'
                })
                item.append('attributes',{
                    'attribute': 'Size (inches)',
                    'attribute_value': size
                })
                item.append('attributes',{
                    'attribute': 'Thickness (mm)',
                    'attribute_value': str(round(thickness,2))
                })
                item.append('attributes',{
                    'attribute': 'Length (feet)',
                    'attribute_value': pipe_length
                })
                item.append('attributes',{
                    'attribute': 'Outer Diameter',
                    'attribute_value': ODs[sr]
                })
                item.append('attributes',{
                    'attribute': 'Width (mm)',
                    'attribute_value': create_strip_width_for_item_attribute(ODs[sr],round(strip_size_reduction))
                })
                item.save()
                pipe_barcode(item)
                print('Item created: {0}'.format(item.item_code))
            sr +=1
        step +=1
        if step == 10:
            strip_size_reduction += 1
            step = 0
        thickness += 0.05
        