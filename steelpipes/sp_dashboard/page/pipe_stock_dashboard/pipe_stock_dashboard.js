frappe.pages['pipe-stock-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Pipe Stock Dashboard',
		single_column: true
	});
	$(frappe.render_template("pipe_stock_dashboard")).appendTo(page.main);
}