frappe.ui.form.on('Payment Entry', {
    party: function(frm) {
        if (frm.doc.party) {
            frappe.db.get_list('Contact', {
            filters : {
                'status': 'Open'
            }})
            .then( r => {
                for (let i in r) {
                    frappe.db.get_doc('Contact', r[i].name)
                    .then ( doc => {
                        if (doc.links) {
                            if (doc.links[0].link_doctype === frm.doc.party_type && 
                                doc.links[0].link_name === frm.doc.party) {
                                    frm.set_value('contact_person', doc.name)
                                }
                            }
                        })
                    }
            })
        }
        // frappe.db.get_value('Dynamic Link', {
        //     'link_doctype': frm.doc.party_type,
        //     'link_name': frm.doc.party,
        //     'parenttype': 'Contact'
        // }, 'parent')
        // .then(r => {
        //     frm.set_value('contact_person', r.parent)
        // })
    },

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