function pipe_weight(frm,i,itemcode,um,qty){
    if (itemcode.includes("Pipe-MS",0)){
        frm.call({
            method: "steelpipes.sp_delivery_note.sp_delivery_note_item.calculate_pipe_weight_um",
            args: {itemcode: itemcode, um: um},
            callback:function(r){
                var weight_um_temp         = r.message.item_weight_um;
                var length_um_temp         = r.message.item_length_um;
                if (qty == undefined || qty == 0 ){
                    var total_weight_um_temp   = weight_um_temp * 1;
                    var total_length_um_temp   = length_um_temp * 1;
                }
                else{
                    var total_weight_um_temp   = weight_um_temp * qty;
                    var total_length_um_temp   = length_um_temp * qty;
                }
                cur_frm.doc.items[i].weight_um = weight_um_temp;
                cur_frm.doc.items[i].total_weight_um = total_weight_um_temp;
                cur_frm.doc.items[i].length_um = length_um_temp;
                cur_frm.doc.items[i].total_length_um = total_length_um_temp;
                cur_frm.refresh_field("items");
                cur_frm.doc.estimate_weight_um += total_weight_um_temp;
                cur_frm.refresh_field("estimate_weight_um");
            }
        })
    }
}

frappe.ui.form.on("Sales Order Item",{
    items_remove: function (frm,cdt,cdn){
        var estimate_weight_tmp = 0;
        for (var i in cur_frm.doc.items){
            if (cur_frm.doc.items[i].item_code.includes("Pipe-MS",0)){
                estimate_weight_tmp += cur_frm.doc.items[i].total_weight_um;
            }    
        }
        cur_frm.doc.estimate_weight_um = estimate_weight_tmp;
        cur_frm.refresh_field("estimate_weight_um");
    },

    item_code: function(frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                frm.call({
                    method: "steelpipes.sp_delivery_note.sp_delivery_note_item.calculate_pipe_weight_um",
                    args: {itemcode: item_code.item_code, um: item_code.um},
                    callback:function(r){
                        var weight_um_temp         = r.message.item_weight_um;
                        var length_um_temp         = r.message.item_length_um;
                        if (item_code.qty == undefined || item_code.qty == 0 ){
                            var total_weight_um_temp   = weight_um_temp * 1;
                            var total_length_um_temp   = length_um_temp * 1;
                        }
                        else{
                            var total_weight_um_temp   = weight_um_temp * item_code.qty;
                            var total_length_um_temp   = length_um_temp * item_code.qty;
                        }
                        frappe.model.set_value(cdt, cdn, "weight_um", weight_um_temp);
                        frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
                        frappe.model.set_value(cdt, cdn, "length_um", length_um_temp);
                        frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                        cur_frm.doc.estimate_weight_um = 0;
                        for (var i in cur_frm.doc.items){
                            if(cur_frm.doc.items[i].item_code){
                                pipe_weight(frm,i,cur_frm.doc.items[i].item_code,cur_frm.doc.items[i].um,cur_frm.doc.items[i].qty );
                            }
                        }
                    } 
                })
            }
        }
        else{
            frappe.model.set_value(cdt,cdn, "item_name", null);
        }
    },

    um: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt, cdn);  
        if(item_code.um == "Kg"){
            if (item_code.item_code){
                if(item_code.item_code.includes("Pipe-MS",0)){
                    var rate_temp = item_code.rate_um*item_code.weight_um;
                    var amount_temp = rate_temp*item_code.qty
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
                    frm.call({
                        method: "steelpipes.sp_delivery_note.sp_delivery_note_item.calculate_pipe_weight_um",
                        args: {itemcode: item_code.item_code, um: item_code.um},
                        callback:function(r){
                            var length_um_temp         = r.message.item_length_um;
                            var total_length_um_temp   = length_um_temp * item_code.qty;             
                            frappe.model.set_value(cdt, cdn, "length_um", length_um_temp);
                            frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                        }
                    })
                }
            } 
        }
        else{
            if (item_code.item_code){
                if(item_code.item_code.includes("Pipe-MS",0)){
                    frm.call({
                        method: "steelpipes.sp_delivery_note.sp_delivery_note_item.calculate_pipe_weight_um",
                        args: {itemcode: item_code.item_code, um: item_code.um},
                        callback:function(r){
                            var length_um_temp         = r.message.item_length_um;
                            var total_length_um_temp   = length_um_temp * item_code.qty;                                       
                            frappe.model.set_value(cdt, cdn, "length_um", length_um_temp);
                            frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                            var rate_temp          = item_code.rate_um*item_code.length_um;
                            var amount_temp = rate_temp*item_code.qty
                            frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                            frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);
                            frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);

                        }
                    })
                }
            }
            
        }
        
    },

    rate_um: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                if(item_code.um == "Kg"){
                    var rate_temp = item_code.rate_um*item_code.weight_um;
                    var amount_temp = rate_temp*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);    
                }
                else{
                    var rate_temp = item_code.rate_um*item_code.length_um;
                    var amount_temp = rate_temp*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp);  
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);             
                }
            }
            else{
                var amount_temp = item_code.rate_um*item_code.qty;
                frappe.model.set_value(cdt, cdn, "rate", item_code.rate_um)
                frappe.model.set_value(cdt, cdn, "rate_um_per_qty", item_code.rate_um);
                frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
            }
        }
    },

    qty: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                var amount_temp = item_code.rate_um_per_qty*item_code.qty;
                var total_weight_um_temp    = item_code.qty*item_code.weight_um;
                var total_length_um_temp    = item_code.qty*item_code.length_um;
                frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
                frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
                var estimate_weight_tmp = 0;
                for (var i in cur_frm.doc.items){
                    estimate_weight_tmp += cur_frm.doc.items[i].total_weight_um;
                }
                cur_frm.doc.estimate_weight_um = estimate_weight_tmp;
                cur_frm.refresh_field("esitimate_weight_um");
            }
            else{
                var amount_temp = item_code.rate_um*item_code.qty;
                frappe.model.set_value(cdt, cdn, "amount_um", amount_temp);
            }
        }
    },

    price_list_rate: function(frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            if (item_code.price_list_rate!=undefined){
                var rate_temp = 0;
                rate_temp = item_code.price_list_rate;
                if(item_code.item_code.includes("Pipe-MS",0)){                
                    if (item_code.um == "Kg"){
                        rate_temp   = rate_temp/item_code.weight_um; 
                    }
                    else{
                        rate_temp   = rate/item_code.length_um;
                    }
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
                else{
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
            }
        }
    },

    discount_percentage: function(frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            var rate_temp = 0;
            if(item_code.item_code.includes("Pipe-MS",0)){
                rate_temp = item_code.price_list_rate - item_code.price_list_rate*item_code.discount_percentage/100;
                if (item_code.um == "Kg"){
                        rate_temp   = rate_temp/item_code.weight_um; 
                    }
                    else{
                        rate_temp   = rate/item_code.length_um;
                    }
                frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
            }
            else{
                rate_temp = item_code.price_list_rate - item_code.price_list_rate*item_code.discount_percentage/100;
                frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
            }
        }
    },

    discount_amount: function(frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            var rate_temp = 0;
            if(item_code.item_code.includes("Pipe-MS",0)){
                rate_temp = item_code.price_list_rate - item_code.discount_amount;
                if (item_code.um == "Kg"){
                    rate_temp   = rate_temp/item_code.weight_um; 
                }
                else{
                    rate_temp   = rate/item_code.length_um;
                }
                frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
            }
            else{
                rate_temp = item_code.price_list_rate - item_code.discount_amount;
                frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
            }
        }
    },

    margin_rate_or_amount: function(frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                var rate_temp = 0;
                if (item_code.margin_type == "Percentage"){
                    rate_temp = item_code.price_list_rate + item_code.price_list_rate*item_code.margin_rate_or_amount/100;
                    if (item_code.um == "Kg"){
                        rate_temp   = rate_temp/item_code.weight_um; 
                    }
                    else{
                        rate_temp   = rate/item_code.length_um;
                    }
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
                else if (item_code.margin_type == "Amount"){
                    rate_temp = item_code.price_list_rate + item_code.margin_rate_or_amount;
                    if (item_code.um == "Kg"){
                        rate_temp   = rate_temp/item_code.weight_um; 
                    }
                    else{
                        rate_temp   = rate/item_code.length_um;
                    }
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
            }
            else{
                if (item_code.margin_type == "Percentage"){
                    rate_temp = item_code.price_list_rate + item_code.price_list_rate*item_code.margin_rate_or_amount/100;
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
                else if (item_code.margin_type == "Amount"){
                    rate_temp = item_code.price_list_rate + item_code.margin_rate_or_amount;
                    frappe.model.set_value(cdt, cdn, "rate_um", rate_temp);
                }
            }
        }
    },

    rate: function (frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                var rate_temp = 0;
                if (item_code.um == "Kg"){
                    rate_temp   = item_code.rate_um*item_code.weight_um; 
                }
                else{
                    rate_temp   = item_code.rate_um*item_code.length_um;
                }
                item_code.rate = rate_temp;
                refresh_field("rate");
            }
            else{
                item_code.rate = item_code.rate_um;
                refresh_field("rate"); 
            }
        }
    }
})