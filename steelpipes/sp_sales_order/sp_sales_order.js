function calculate_weight_um(frm){
    var estimate_weight_um_temp         = 0;

    for (var i in frm.doc.items){
        estimate_weight_um_temp     += frm.doc.items[i].total_weight_um;  
    }

    frm.set_value('estimate_weight_um',estimate_weight_um_temp);
}

frappe.ui.form.on("Sales Order", {
    //items: function(frm){
    //    calculate_weight_um(frm); 
   // }
})