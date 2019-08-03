frappe.ui.form.on("Sales Order Item",{
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
                    var rate_temp          = item_code.rate_um*item_code.weight_um;
                    var amount_temp       = rate_temp*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "amount", amount_temp);
                    
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
                            var amount_temp       = rate_temp*item_code.qty;
                            frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                            frappe.model.set_value(cdt, cdn, "amount", amount_temp);

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
                    var rate_temp          = item_code.rate_um*item_code.weight_um;
                    var amount_temp        = rate_temp*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp); 
                    
                }
                else{
                    var rate_temp          = item_code.rate_um*item_code.length_um;
                    var amount_temp        = rate_temp*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    
                }
            }
            else{
                frappe.model.set_value(cdt, cdn, "rate", item_code.rate_um)
            }
        }
    },

    qty: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        var total_weight_um_temp    = item_code.qty*item_code.weight_um;
        var total_length_um_temp    = item_code.qty*item_code.length_um;
        frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
        frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
        
    },
    rate: function (frm,cdt,cdn){
            var item_code   = frappe.model.get_doc(cdt, cdn);
            var rate_temp = 0;
            
            if (item_code.um == "Kg"){
                rate_temp   = item_code.rate_um*item_code.weight_um; 
            }
            else{
                rate_temp   = item_code.rate_um*item_code.length_um;
            }

            if (item_code.item_code){
                if(item_code.item_code.includes("Pipe-MS",0)){
                    item_code.rate = rate_temp;
                    refresh_field("rate");
                }
            }
    }
})