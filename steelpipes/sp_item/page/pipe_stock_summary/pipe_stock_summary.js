frappe.pages['pipe-stock-summary'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Pipe Stock Summary',
        single_column: true
	});
	var no_data = '1';
	var todays_date = frappe.datetime.get_today();
	var page_subtitle = 'Stock as of ' + todays_date;
	page.set_title_sub(page_subtitle);
	var field1 = page.add_field({
		label: 'Warehouse',
		fieldtype: 'Link',
		fieldname: 'warehouse',
		options: 'Warehouse',
		change() {
			if (field1.get_value()== ''){
				no_data = '1';
				console.log(field1.get_value());
				console.log(no_data);
				$(frappe.render_template("pipe_stock_summary", {"no_data": "1"} )).append(page.main);
			}
			else{
				no_data = '0';  
				console.log(field1.get_value());
				console.log(no_data);
				$(frappe.render_template("pipe_stock_summary", {"no_data": "0"} )).appendTo(page.main);
			}
		}
	});

    $(frappe.render_template("pipe_stock_summary", {"no_data": "1"} )).appendTo(page.main);
    //wrapper.pos = new erpnext.stock.SteelStockBalance(wrapper);

};