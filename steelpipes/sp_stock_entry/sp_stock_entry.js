function calculate_weight_um(frm){
    var total_weight_um_temp        = frm.doc.loaded_vehicle_weight_um - frm.doc.empty_vehicle_weight_um;
    var estimate_weight_um_temp         = 0;
    var total_scale_weight_um_temp      = 0;
    var weight_difference_um_temp       = 0;
    var weight_difference_percentage_um = 0;

    for (var i in frm.doc.items){
        estimate_weight_um_temp     += frm.doc.items[i].total_weight_um;
        total_scale_weight_um_temp  += frm.doc.items[i].total_scale_weight_um;
    }

    weight_difference_um_temp           = total_weight_um_temp - estimate_weight_um_temp;
    weight_difference_percentage_um     = (weight_difference_um_temp/estimate_weight_um_temp)*100;


    frm.set_value('estimate_weight_um',estimate_weight_um_temp);
    frm.set_value('total_weight_um',total_weight_um_temp);
    frm.set_value('weight_difference_um', weight_difference_um_temp);
    frm.set_value('weight_difference_percentage_um', weight_difference_percentage_um);
    frm.set_value('total_scale_weight_um', total_scale_weight_um_temp);
}

function update_weight_calculations(frm){
    frm.set_value('empty_vehicle_weight_um',0);
    frm.set_value('loaded_vehicle_weight_um',0);
    frm.set_value('total_weight_um',0);
    frm.set_value('weight_difference_um', 0);
    frm.set_value('weight_difference_percentage_um', 0);
    frm.set_value('total_scale_weight_um', 0);
    cur_frm.doc.estimate_weight_um = 0;
    for (var d in cur_frm.doc.items){
        if (cur_frm.doc.items[d].item_code){
            if (cur_frm.doc.items[d].item_code.includes("Pipe-MS",0)){
                cur_frm.doc.items[d].scale_weight_um = 0;
                cur_frm.doc.items[d].total_scale_weight_um = 0;
                cur_frm.doc.items[d].total_weight_um = cur_frm.doc.items[d].weight_um*cur_frm.doc.items[d].qty;
                cur_frm.doc.items[d].total_length_um = cur_frm.doc.items[d].length_um*cur_frm.doc.items[d].qty;
            }
        }
        cur_frm.doc.estimate_weight_um += cur_frm.doc.items[d].total_weight_um;
    }
    cur_frm.refresh_field('estimate_weight_um');
    cur_frm.refresh_field('items');

}

frappe.ui.form.on("Stock Entry", {
    refresh: function(frm){
        if (cur_frm.doc.__islocal && (cur_frm.doc.set_posting_time == undefined || cur_frm.doc.set_posting_time == 0)){
            var todays_date = frappe.datetime.get_today();
            var newdate     = frappe.datetime.add_days(todays_date,-1);
            cur_frm.doc.posting_date = newdate;
            cur_frm.refresh_field("posting_date");
            update_weight_calculations(frm);
        }
    },

    scan_barcode: function(frm){
        var doc = cur_frm.doc;
        var is_empty = 0;
        for (var i in doc.items){
            if(doc.items[i].item_code==undefined){
                is_empty = 1;
            }
        }
        if (is_empty ==0){
            frm.add_child('items');
        }
    },

    empty_vehicle_weight_um: function(frm){
        calculate_weight_um(frm); 
    },

    loaded_vehicle_weight_um: function(frm){
        calculate_weight_um(frm);
    },

    update_weight_calculations_um: function(frm){
        calculate_weight_um(frm);
    }
})