//Pipe calculations 
frappe.ui.form.on("Delivery Note Item", { 
    /*
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
                    var rate_temp           = item_code.rate_um*item_code.weight_um;
                    var qty_sign            = 0;
                    if (item_code.qty<0){
                        qty_sign = -1;
                    }
                    else{
                        qty_sign = 1;
                    }
                    var rate_um_per_qty_temp= item_code.rate_um*item_code.scale_weight_um*qty_sign;
                    var amount_um_temp      = item_code.rate_um*item_code.scale_weight_um*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_um_per_qty_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);

                    
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
                            var qty_sign = 0;
                            if (item_code.qty<0){
                                qty_sign = -1;
                            }
                            else{
                                qty_sign = 1;
                            }
                            frappe.model.set_value(cdt, cdn, "length_um", length_um_temp);
                            frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                            var rate_temp       = item_code.rate_um*item_code.length_um;
                            var amount_um_temp  = item_code.rate_um*item_code.length_um*item_code.qty;
                            frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                            frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_temp*qty_sign);
                            frappe.model.set_value(cdt, cdn, "amount", amount_um_temp);

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
                    var rate_temp           = item_code.rate_um*item_code.weight_um;
                    var rate_um_per_qty_temp= item_code.rate_um*item_code.scale_weight_um;
                    var amount_um_temp      = item_code.rate_um*item_code.scale_weight_um*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp); 
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_um_per_qty_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
                }
                else{
                    var rate_temp           = item_code.rate_um*item_code.length_um;
                    var rate_um_per_qty_temp= item_code.rate_um*item_code.length_um;
                    var amount_um_temp      = item_code.rate_um*item_code.length_um*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_um_per_qty_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
                }  
            }
        }
        else{
            frappe.model.set_value(cdt, cdn, "rate", item_code.rate_um)
        }
    },//*/

    scale_weight_um: function (frm, cdt, cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        var qty_temp = 0;
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                if (item_code.qty <0){
                    qty_temp = item_code.qty*-1;
                }
                else{
                    qty_temp = item_code.qty;
                }
                var total_scale_weight_um_temp = qty_temp*item_code.scale_weight_um;
                frappe.model.set_value(cdt, cdn, "total_scale_weight_um", total_scale_weight_um_temp);
                if(item_code.um == "Kg"){
                    var rate_temp          = item_code.rate_um*item_code.weight_um;
                    var rate_um_per_qty_temp= item_code.rate_um*item_code.scale_weight_um;
                    var amount_um_temp      = item_code.rate_um*item_code.scale_weight_um*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate", rate_temp);
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_um_per_qty_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
                }         
            }
            else{
                item_code.scale_weight_um = 0;
                refresh_field("scale_weight_um");
            }
        }
    },

    qty: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        var qty_temp = 0;
        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                if (item_code.qty <0){
                    qty_temp = item_code.qty*-1;
                }
                else{
                    qty_temp = item_code.qty;
                    } 
                var total_scale_weight_um_temp  = qty_temp*item_code.scale_weight_um;
                var total_weight_um_temp        = qty_temp*item_code.weight_um;
                var total_length_um_temp        = qty_temp*item_code.length_um;
                var amount_um_temp              = item_code.rate_um*item_code.scale_weight_um*item_code.qty;
                var rate_um_per_qty_temp        = item_code.rate_um*item_code.scale_weight_um;
                frappe.model.set_value(cdt, cdn, "total_scale_weight_um", total_scale_weight_um_temp);
                frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
                frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
                frappe.model.set_value(cdt, cdn, "rate_um_per_qty",rate_um_per_qty_temp);
                frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
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