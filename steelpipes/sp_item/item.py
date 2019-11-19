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
                item_code_temp += '-{0} INCH'.format(item_size_um)
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

def pipe_item_weight_detail(self,cdt):
    for d in self.items:
        if 'Pipe-MS' in str(d.item_code):
                if self.doctype == 'Purchase Receipt':
                    item = frappe.get_doc('Item',d.item_code)
                    has_warehouse = 0
                    for w in item.receiving_details:
                        if w.receiving_warehouse == d.warehouse:
                            has_warehouse = 1
                            w.db_set('qty',d.qty)
                            w.db_set('scale_weight', d.scale_weight_um)
                            w.db_set('estimate_weight',d.weight_um)
                            w.db_set('date',self.posting_date)
                            w.db_set('related_document',self.name)
                    if has_warehouse == 0:
                        item.append('receiving_details',{
                            'receiving_warehouse': d.warehouse,
                            'qty': d.qty,
                            'scale_weight': d.scale_weight_um,
                            'estimate_weight': d.weight_um,
                            'date': self.posting_date,
                            'related_document': self.name
                        })
                    item.save()
                elif self.doctype == 'Delivery Note':
                    item = frappe.get_doc('Item',d.item_code)
                    has_warehouse = 0
                    for w in item.delivery_details:
                        if w.delivery_warehouse == d.warehouse:
                            has_warehouse = 1
                            w.db_set('qty',d.qty)
                            w.db_set('scale_weight', d.scale_weight_um)
                            w.db_set('estimate_weight',d.weight_um)
                            w.db_set('date',self.posting_date)
                            w.db_set('delivery_note',self.name)
                    if has_warehouse == 0:
                        item.append('delivery_details',{
                            'delivery_warehouse': d.warehouse,
                            'qty': d.qty,
                            'scale_weight': d.scale_weight_um,
                            'estimate_weight': d.weight_um,
                            'date': self.posting_date,
                            'delivery_note': self.name
                        })
                    item.save()                    
                elif self.doctype == 'Stock Entry':
                    if self.stock_entry_type == 'Send to Warehouse':
                        item = frappe.get_doc('Item',d.item_code)
                        has_warehouse = 0
                        for w in item.receiving_details:
                            if w.receiving_warehouse == d.s_warehouse:
                                has_warehouse = 1
                                w.db_set('qty',d.qty)
                                w.db_set('scale_weight', d.scale_weight_um)
                                w.db_set('estimate_weight',d.weight_um)
                                w.db_set('date',self.posting_date)
                                w.db_set('related_document',self.name)
                        if has_warehouse == 0:
                            item.append('receiving_details',{
                                'receiving_warehouse': d.s_warehouse,
                                'qty': d.qty,
                                'scale_weight': d.scale_weight_um,
                                'estimate_weight': d.weight_um,
                                'date': self.posting_date,
                                'related_document': self.name
                            })
                        item.save()
                        
                    elif self.stock_entry_type == 'Receive at Warehouse':
                        item = frappe.get_doc('Item',d.item_code)
                        has_warehouse = 0
                        for w in item.receiving_details:
                            if w.receiving_warehouse == d.t_warehouse:
                                has_warehouse = 1
                                w.db_set('qty',d.qty)
                                w.db_set('scale_weight', d.scale_weight_um)
                                w.db_set('estimate_weight',d.weight_um)
                                w.db_set('date',self.posting_date)
                                w.db_set('related_document',self.name)
                        if has_warehouse == 0:
                            item.append('receiving_details',{
                                'receiving_warehouse': d.t_warehouse,
                                'qty': d.qty,
                                'scale_weight': d.scale_weight_um,
                                'estimate_weight': d.weight_um,
                                'date': self.posting_date,
                                'related_document': self.name
                            })
                        item.save()
