import frappe
from frappe.utils import flt

def calculate_pipe_weight_um(itemcode,um):
    
    #Calculating Pipe Weight using Attributes 
    
    delivery_note_item_um = frappe.get_doc("Item", itemcode)
    item_thickness_um = item_width_um = item_length_um = 0
    if str(delivery_note_item_um.variant_of) in ['Pipe']:
        for item_attribute_um in delivery_note_item_um.attributes:
            attribute_name = str(item_attribute_um.attribute)
            if 'Thickness' in attribute_name:
                item_thickness_um = float(item_attribute_um.attribute_value)
            if 'Width'     in attribute_name:
                item_width_um     = float(item_attribute_um.attribute_value)    
            if 'Length'    in attribute_name:
                item_length_um    = float(item_attribute_um.attribute_value)

        item_weight_um = (1.2 * item_thickness_um * item_width_um * item_length_um) / 508
        if um == 'Meter':
            item_length_um = item_length_um * 0.3048
        return {"item_weight_um":round(item_weight_um,2),"item_length_um":round(item_length_um,2)}



def update_estimate_weight(self,cdt):
    estimate_weight_um_temp = 0
    has_pipe = 0

    for d in self.items:
        if 'Pipe-MS' in str(d.item_code):    
            estimate_weight_um_temp     += d.total_weight_um
            has_pipe = 1
    if has_pipe ==1:
        self.estimate_weight_um                 = estimate_weight_um_temp