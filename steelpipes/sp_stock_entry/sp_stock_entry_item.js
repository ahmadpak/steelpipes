function pipe_weight(frm,i,itemcode){
    if (itemcode.includes("Pipe-MS",0)){
        cur_frm.doc.estimate_weight_um += cur_frm.doc.items[i].total_weight_um;
        cur_frm.doc.total_scale_weight_um += cur_frm.doc.items[i].total_scale_weight_um;
        cur_frm.doc.total_um += cur_frm.doc.items[i].amount_um;
        cur_frm.refresh_field("estimate_weight_um");
        cur_frm.refresh_field("total_scale_weight_um");
        cur_frm.refresh_field("total_um");
    }
}

frappe.ui.form.on("Stock Entry Detail", {    
    items_remove: function(frm){
        cur_frm.doc.estimate_weight_um = 0;
        cur_frm.doc.total_scale_weight_um = 0;
        cur_frm.doc.total_um = 0;
        for (var i in cur_frm.doc.items){
            if(cur_frm.doc.items[i].item_code){
                pipe_weight(frm,i,cur_frm.doc.items[i].item_code);
            }
        }
        cur_frm.doc.weight_difference_um = cur_frm.doc.total_weight_um - cur_frm.doc.estimate_weight_um;
        cur_frm.doc.weight_difference_percentage_um = (cur_frm.doc.weight_difference_um/cur_frm.doc.estimate_weight_um)*100;
        cur_frm.refresh_field("weight_difference_um");
        cur_frm.refresh_field("weight_difference_percentage_um");
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
                        }
                    })
                }
            }
        }
    },
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
                    var rate_um_per_qty_temp= item_code.rate_um*item_code.scale_weight_um;
                    var amount_um_temp      = item_code.rate_um*item_code.scale_weight_um*item_code.qty;
                    frappe.model.set_value(cdt, cdn, "rate_um_per_qty", rate_um_per_qty_temp);
                    frappe.model.set_value(cdt, cdn, "amount_um", amount_um_temp);
                }
                cur_frm.doc.estimate_weight_um = 0;
                cur_frm.doc.total_scale_weight_um = 0;
                cur_frm.doc.total_um = 0;
                for (var i in cur_frm.doc.items){
                    if(cur_frm.doc.items[i].item_code){
                        pipe_weight(frm,i,cur_frm.doc.items[i].item_code);
                    }
                }
                cur_frm.doc.weight_difference_um = cur_frm.doc.total_weight_um - cur_frm.doc.estimate_weight_um;
                cur_frm.doc.weight_difference_percentage_um = (cur_frm.doc.weight_difference_um/cur_frm.doc.estimate_weight_um)*100;
                cur_frm.refresh_field("weight_difference_um");
                cur_frm.refresh_field("weight_difference_percentage_um");
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
                        pipe_weight(frm,i,cur_frm.doc.items[i].item_code);
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
    }
})