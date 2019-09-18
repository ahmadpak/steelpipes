frappe.pages['pipe-stock-summary'].on_page_load = function(wrapper) {
	new mypage(wrapper);	
}

mypage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Pipe Stock Summary',
			single_column: true
		});
		//this.no_data = '1';
		var todays_date = frappe.datetime.get_today();
		var page_subtitle = 'Stock as of ' + todays_date;
		this.page.set_title_sub(page_subtitle);
		var field1 = this.page.add_field({
			label: 'Warehouse',
			fieldtype: 'Link',
			fieldname: 'warehouse',
			options: 'Warehouse',
			change() {
				if (field1.get_value()== ''){
					this.no_data = '1';
					console.log(field1.get_value());
					this.make();
				}
				else{
					this.no_data = '0';  
					this.make();
				}
			}
		});
		//this.make();
	},
	make: function(){
		$(frappe.render_template('pipe_stock_summary',this)).appendTo(this.page.main);
	}
})