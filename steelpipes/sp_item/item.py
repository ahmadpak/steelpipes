import frappe
from frappe.utils import flt

def pipe_custom_name(self,cdt):
    if "Pipe-MS" in str(self.item_code):
        item_code_temp = "Pipe-MS"
        for d in self.attributes:
            attribute_name = str(d.attribute)
            
            if 'Size' in attribute_name:
                item_size_um = str(d.attribute_value)
                item_code_temp += '-{0} INCH'.format(item_size_um)
            
            elif 'Thickness' in attribute_name:
                item_thickness_um = str(d.attribute_value)
                item_code_temp += "-{0} MM".format(item_thickness_um)
            
            elif 'Length' in attribute_name:
                item_length_um = str(d.attribute_value)
                item_code_temp += "-{0} FT".format(item_length_um)
    
        self.description = self.item_code = self.item_name = item_code_temp    