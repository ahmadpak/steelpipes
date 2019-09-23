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
		change(){
			if (field1.get_value()== ''){
				// no_data = '1';
				// console.log(field1.get_value());
				// console.log(no_data);
				// $(frappe.render_template("pipe_stock_summary", {"no_data": "1"} )).append(page.main);
        // $("h5").css('color','black');
        page.remove_inner_button('Download')
        $('.pipeStockSummary').fadeOut(400,function(){
          $('.noWareHouseHTML').fadeIn();
        });
			}
			else{
        // $("h5").css('color','blue');
        page.add_inner_button('Download', () => download_stock())
        $('.noWareHouseHTML').fadeOut(400,function(){
          $('.pipeStockSummary').fadeIn();
          frappe.call({
            method:'steelpipes.utils.get_pipe_stock',
            args: {
              warehouse: field1.get_value(),
            },
            callback: function(r){
              $('#3_4inch').css('background',"none")
              $('#3_4inch').html(r.message);
            }
          });
        });

      }
		}
	});
    $(frappe.render_template("pipe_stock_summary")).appendTo(page.main);
    $('.pipeStockSummary').css('display','none');
};

function download_stock(){
  console.log('Download stock')
}
