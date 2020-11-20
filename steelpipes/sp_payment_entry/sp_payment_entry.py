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
