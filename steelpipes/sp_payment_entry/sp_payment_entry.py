import frappe
from frappe import _

@frappe.whitelist()
def set_phone(contact):
    doc = frappe.get_doc('Contact', contact)

    phone = []
    if doc.phone:
        return doc.phone
    elif doc.mobile_no:
        return doc.mobile_no
    elif len(doc.phone_nos) == 0:
        return False
    else:
        phone = [phone.phone for phone in doc.phone_nos]
        if phone[0]:
            return phone[0]
        else:
            return False
    return False

@frappe.whitelist()
def get_contract(party_type, party):
    contract = frappe.db.get_all('Dynamic Link', {
        'link_doctype': party_type,
        'link_name': party,
        'parenttype': 'Contact'
    }, 'parent')
    if contract:
        return contract[0].parent
    else:
        return False