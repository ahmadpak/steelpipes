function pipe_weight(i,itemcode){
    if (itemcode.includes("Pipe-MS",0)){
        cur_frm.doc.estimate_weight_um += cur_frm.doc.items[i].total_weight_um;
        cur_frm.doc.total_scale_weight_um += cur_frm.doc.items[i].total_scale_weight_um;
        cur_frm.doc.total_um += cur_frm.doc.items[i].amount_um;
        cur_frm.refresh_field("estimate_weight_um");
        cur_frm.refresh_field("total_scale_weight_um");
        cur_frm.refresh_field("total_um");
    }
}

frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm){
        if (cur_frm.doc.__islocal  && (cur_frm.doc.set_posting_time == undefined || cur_frm.doc.set_posting_time == 0)){
            var todays_date = frappe.datetime.get_today();
            var newdate     = frappe.datetime.add_days(todays_date,-1);
            cur_frm.doc.posting_date = newdate;
            cur_frm.refresh_field("posting_date");
        }
    }
})


frappe.ui.form.on("Sales Invoice Item", {
    items_remove: function(frm){
        cur_frm.doc.estimate_weight_um = 0;
        cur_frm.doc.total_scale_weight_um = 0;
        cur_frm.doc.total_um = 0;
        for (var i in cur_frm.doc.items){
            if(cur_frm.doc.items[i].item_code){
                pipe_weight(i,cur_frm.doc.items[i].item_code);
            }
        }
        cur_frm.doc.weight_difference_um = cur_frm.doc.total_weight_um - cur_frm.doc.estimate_weight_um;
        cur_frm.doc.weight_difference_percentage_um = (cur_frm.doc.weight_difference_um/cur_frm.doc.estimate_weight_um)*100;
        cur_frm.refresh_field("weight_difference_um");
        cur_frm.refresh_field("weight_difference_percentage_um");
    },

    qty: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                var qty_temp = 0;
                if (item_code.qty <0){
                    qty_temp = item_code.qty*-1;
                }
                else{
                    qty_temp = item_code.qty;
                    } 
                var total_scale_weight_um_temp  = qty_temp*item_code.scale_weight_um;
                var total_weight_um_temp        = qty_temp*item_code.weight_um;
                var total_length_um_temp        = qty_temp*item_code.length_um;
                var amount_um_temp              = item_code.rate_um_per_qty*item_code.qty;
                frappe.model.set_value(cdt, cdn, "total_scale_weight_um", total_scale_weight_um_temp);
                frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
                frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
                cur_frm.doc.estimate_weight_um = 0;
                cur_frm.doc.total_scale_weight_um = 0;
                cur_frm.doc.total_um = 0;
                for (var i in cur_frm.doc.items){
                    if(cur_frm.doc.items[i].item_code){
                        pipe_weight(i,cur_frm.doc.items[i].item_code);
                    }
                }
                cur_frm.doc.weight_difference_um = cur_frm.doc.total_weight_um - cur_frm.doc.estimate_weight_um;
                cur_frm.doc.weight_difference_percentage_um = (cur_frm.doc.weight_difference_um/cur_frm.doc.estimate_weight_um)*100;
                cur_frm.refresh_field("weight_difference_um");
                cur_frm.refresh_field("weight_difference_percentage_um");
            }
            else{
                var amount_temp = item_code.rate_um*item_code.qty;
                frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
            }
        }
    },

    rate: function (frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);    
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                if(item_code.um == "Kg"){
                    var rate_temp = item_code.rate*item_code.scale_weight_um;
                    var amount_temp = rate_temp*item_code.qty;
                    item_code.rate = item_code.rate*item_code.weight_um;
                    refresh_field("rate");
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);    
                }
                else{
                    var rate_temp = item_code.rate*item_code.length_um;
                    var amount_temp = rate_temp*item_code.qty;
                    item_code.rate = rate_temp;
                    refresh_field("rate");
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);  
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);             
                }
            }
            else{
                var amount_temp = item_code.rate*item_code.qty;
                frappe.model.set_value(cdt, cdn, "rate_um", item_code.rate)
                frappe.model.set_value(cdt, cdn, "rate_um_per_qty", item_code.rate);
                frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
            }
        }
    }
})

frappe.ui.form.on('Sales Taxes and Charges', {
	tax_amount(frm,cdt,cdn) {
        var doc = cur_frm.doc;
	    var charges = frappe.model.get_doc(cdt, cdn);
        frm.call({
            method:'steelpipes.utils.get_charges_account',
            args: {
                steel_pipes_charges_settings: 'Steel Pipes Charges Settings'
            },
            callback: function(r){
                if (charges.account_head == r.message.loading_head){
                    var pipe_charges_amount = charges.tax_amount;
                    doc.loading = pipe_charges_amount;
                    cur_frm.refresh_field('loading');
                }
                else if (charges.account_head == r.message.cutting_labor_head){
                    var pipe_charges_amount = charges.tax_amount;
                    doc.cutting_labor = pipe_charges_amount;
                    cur_frm.refresh_field('cutting_labor');
                }
                else if (charges.account_head == r.message.transport_head){
                    var pipe_charges_amount = charges.tax_amount;
                    doc.transport = pipe_charges_amount;
                    cur_frm.refresh_field('transport');
                }
            }
        })
    },
    taxes_remove: function(frm){
        var doc = cur_frm.doc;
        frm.call({
            method:'steelpipes.utils.get_charges_account',
            args: {
                steel_pipes_charges_settings: 'Steel Pipes Charges Settings'
            },
            callback: function(r){
                var has_loading = 0;
                var has_cutting_labor = 0;
                var has_transport = 0;
                for (var i in doc.taxes){
                    console.log(doc.taxes[i].account_head)
                    if (doc.taxes[i].account_head == r.message.loading_head){
                        has_loading =1;
                    }
                    else if (doc.taxes[i].account_head == r.message.cutting_labor_head){
                        has_cutting_labor = 1;  
                    }
                    else if (doc.taxes[i].account_head == r.message.transport_head){
                        has_transport =1;
                    }
                }
                if ( has_loading == 0){
                    doc.loading = 0;
                    cur_frm.refresh_field('loading');
                }
                if (has_cutting_labor == 0){
                    doc.cutting_labor = 0;
                    cur_frm.refresh_field('cutting_labor');
                }
                if (has_transport == 0){
                    doc.transport = 0;
                    cur_frm.refresh_field('transport');
                }
            }
        })
    }
})