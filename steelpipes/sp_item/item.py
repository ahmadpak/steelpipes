import frappe
from frappe.utils import flt

def pipe_custom_name(self,cdt):
    if "Pipe-MS" in str(self.item_code):
        item_code_temp = "Pipe-MS"
        barcode = ''
        for d in self.attributes:
            attribute_name = str(d.attribute)
            
            if 'Size' in attribute_name:
                item_size_um = str(d.attribute_value)
                temp_size = ''
                for character in item_size_um:
                    if character != '/' and character!=' ':
                        temp_size += character
                item_code_temp += '-{0} INCH'.format(temp_size)
                barcode += temp_size
            elif 'Thickness' in attribute_name:
                item_thickness_um = str(d.attribute_value)
                temp_thickness = ''
                for character in item_thickness_um:
                    if character != ' ':
                        temp_thickness += character
                if len(temp_thickness)!=4:
                    temp_thickness +='0'
                item_code_temp += "-{0} MM".format(temp_thickness)
                barcode += temp_thickness

            elif 'Length' in attribute_name:
                item_length_um = str(d.attribute_value)
                temp_length = ''
                for character in item_length_um:
                    if character != ' ':
                        temp_length += character
                item_code_temp += "-{0} FT".format(temp_length)
                barcode += temp_length
        if self.barcodes:
            has_barcode = 0
            for d in self.barcodes:
                if d.barcode == barcode:
                    has_barcode = 1
            if has_barcode == 0:
                self.append('barcodes',{
                        'barcode':barcode
                    })
        else:                    
            self.append('barcodes',{
                'barcode':barcode
            })
        self.description = self.item_code = self.item_name = item_code_temp    