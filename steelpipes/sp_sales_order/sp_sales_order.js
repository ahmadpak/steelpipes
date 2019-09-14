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

frappe.ui.form.on("Sales Order",{
    refresh: function(frm){
        cur_frm.doc.estimate_weight_um = 0;
        for (var i in cur_frm.doc.items){
            if(cur_frm.doc.items[i].item_code){
                pipe_weight(frm,i,cur_frm.doc.items[i].item_code,cur_frm.doc.items[i].um,cur_frm.doc.items[i].qty );
            }
        }
        if (cur_frm.doc.__islocal){
            var todays_date = frappe.datetime.get_today();
            var newdate     = frappe.datetime.add_days(todays_date,-1);
            cur_frm.doc.transaction_date = newdate;
            cur_frm.doc.delivery_date = newdate;
            cur_frm.refresh_field("transaction_date");
            cur_frm.refresh_field("delivery_date");
        }
    }
})