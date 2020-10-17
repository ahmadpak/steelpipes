frappe.ui.form.on('Payment Entry', {
    contact_person: function(frm) {
        if (frm.doc.contact_person) {
            frappe.call('steelpipes.sp_payment_entry.sp_payment_entry.set_phone',
            {contact: frm.doc.contact_person})
            .then (r => {
                if (r.message) {
                    frm.set_value('contact_phone', r.message)
                    frm.refresh_fields('contact_phone')
                }
            })
        }
    }
});