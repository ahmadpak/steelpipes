import frappe

@frappe.whitelist()
def get_charges_account(steel_pipes_charges_settings):
    charges_doc = frappe.get_doc(steel_pipes_charges_settings)
    return {'loading_head': charges_doc.loading_account_head, 'cutting_labor_head': charges_doc.cutting_labor_account_head, 'transport_head': charges_doc.transport_account_head}

@ frappe.whitelist()
def get_pipe_stock(warehouse):
    innerhtml = '''<td class="col-sm-4" style="border:1px solid">5</td>
          <td class="col-sm-4" style="border:1px solid">20</td> 
          <td class="col-sm-4" style="border:1px solid">2115</td> 
          <td class="col-sm-4" style="border:1px solid">30</td>'''
    return innerhtml