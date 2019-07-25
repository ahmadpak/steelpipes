frappe.ui.form.on("Sales Invoice Item", {
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