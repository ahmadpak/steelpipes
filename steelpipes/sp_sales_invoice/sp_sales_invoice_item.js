frappe.ui.form.on("Sales Invoice Item", {
    qty: function (frm,cdt,cdn){
        var item_code = frappe.model.get_doc(cdt,cdn);
        console.log("Before Processing");
        console.log(item_code.scale_weight_um);
        console.log(item_code.total_scale_weight_um);

        var qty_temp = 0;
        if (item_code.qty <0){
            qty_temp = item_code.qty*-1;
        }
        else{
            qty_temp = item_code.qty;
        }
        console.log("qty:" + item_code.qty);    
        var total_scale_weight_um_temp = qty_temp*item_code.scale_weight_um;
        var total_weight_um_temp    = qty_temp*item_code.weight_um;
        var total_length_um_temp    = qty_temp*item_code.length_um;
        frappe.model.set_value(cdt, cdn, "total_scale_weight_um", total_scale_weight_um_temp);
        frappe.model.set_value(cdt, cdn, "total_weight_um", total_weight_um_temp);
        frappe.model.set_value(cdt, cdn, "total_length_um", total_length_um_temp);
        console.log("After Processing");
        console.log(item_code.scale_weight_um);
        console.log(item_code.total_scale_weight_um);
        
    },

    rate: function (frm,cdt,cdn){
        var item_code   = frappe.model.get_doc(cdt, cdn);
        var rate_temp = 0;
        
        if (item_code.um == "Kg"){
            rate_temp   = item_code.rate_um*item_code.scale_weight_um; 
        }
        else{
            rate_temp   = item_code.rate_um*item_code.length_um;
        }

        if (item_code.item_code){
            if(item_code.item_code.includes("Pipe-MS",0)){
                frappe.model.set_value(cdt,cdn,'rate', rate_temp);
            }
        }
    }
})