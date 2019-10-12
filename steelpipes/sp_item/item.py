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
                item_code_temp += '-{0} INCH'.format(item_size_um)
                for character in item_size_um:
                    if character != '/':
                        barcode += character
            elif 'Thickness' in attribute_name:
                item_thickness_um = str(d.attribute_value)
                if len(item_thickness_um)!=4:
                    item_thickness_um +='0'
                item_code_temp += "-{0} MM".format(item_thickness_um)
                barcode += item_thickness_um

            elif 'Length' in attribute_name:
                item_length_um = str(d.attribute_value)
                item_code_temp += "-{0} FT".format(item_length_um)
                barcode += item_length_um
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