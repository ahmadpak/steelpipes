frappe.pages['pipe-stock-summary'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Pipe Stock Summary',
        single_column: true
	});
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
        page.remove_inner_button('Download');
        $('.pipeStockSummary').fadeOut(400,function(){
          $('.noWareHouseHTML').fadeIn();
        });
			}
			else{
        // $("h5").css('color','blue');
        page.add_inner_button('Download', () => download_stock(field1.get_value()));
        $('.noWareHouseHTML').fadeOut(400,function(){
          $('.pipeStockSummary').fadeIn();
            frappe.call({
              method:'steelpipes.utils.get_pipe_stock',
              args: {
                warehouse: field1.get_value()
              },
              callback: function(r){
                if (r.message){
                  var itemstemp = JSON.parse(r.message);
                  // console.log(itemstemp)
                  if (itemstemp.pipe1_2inch){
                    //$('#pipe1_2inch').fadeOut(400,function(){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                      '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                      '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                      '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                      '<td class="col-sm-4" style="border:1px solid">KG</td>'
                    + '</tr>';
                    for (var i in itemstemp.pipe1_2inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1_2inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1_2inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1_2inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1_2inch[i].weight+'</td></tr>';
                    }
                    //});
                    $('#pipe1_2inch').css('background',"none");
                    $('#pipe1_2inch').html(newhtml);
                    $('#pipe1_2inch').fadeOut(400,function(){
                      $('#pipe1_2inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe1_2inch').html(update_null_html());
                    $('#pipe1_2inch').fadeOut(400,function(){
                      $('#pipe1_2inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe3_4inch){
                    //$('#pipe3_4inch').fadeOut(400,function(){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                      '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                      '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                      '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                      '<td class="col-sm-4" style="border:1px solid">KG</td>'
                    + '</tr>';
                    for (var i in itemstemp.pipe3_4inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3_4inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3_4inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3_4inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3_4inch[i].weight+'</td></tr>';
                    }
                    //});
                    $('#pipe3_4inch').css('background',"none");
                    $('#pipe3_4inch').html(newhtml);
                    $('#pipe3_4inch').fadeOut(400,function(){
                      $('#pipe3_4inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe3_4inch').html(update_null_html());
                    $('#pipe3_4inch').fadeOut(400,function(){
                      $('#pipe3_4inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe1inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                      '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                      '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                      '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                      '<td class="col-sm-4" style="border:1px solid">KG</td>'
                    + '</tr>';
                    for (var i in itemstemp.pipe1inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe1inch[i].weight+'</td></tr>';
                    }
                    $('#pipe1inch').css('background',"none");
                    $('#pipe1inch').html(newhtml);
                    $('#pipe1inch').fadeOut(400,function(){
                      $('#pipe1inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe1inch').html(update_null_html());
                    $('#pipe1inch').fadeOut(400,function(){
                      $('#pipe1inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe11_4inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>'
                  + '</tr>';
                    for (var i in itemstemp.pipe11_4inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_4inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_4inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_4inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_4inch[i].weight+'</td></tr>';
                    }
                    $('#pipe11_4inch').css('background',"none");
                    $('#pipe11_4inch').html(newhtml);
                    $('#pipe11_4inch').fadeOut(400,function(){
                      $('#pipe11_4inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe11_4inch').html(update_null_html());
                    $('#pipe11_4inch').fadeOut(400,function(){
                      $('#pipe11_4inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe11_2inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                  '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                  '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                  '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                  '<td class="col-sm-4" style="border:1px solid">KG</td>'
                + '</tr>';
                    for (var i in itemstemp.pipe11_2inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_2inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_2inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_2inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe11_2inch[i].weight+'</td></tr>';
                    }
                    $('#pipe11_2inch').css('background',"none");
                    $('#pipe11_2inch').html(newhtml);
                    $('#pipe11_2inch').fadeOut(400,function(){
                      $('#pipe11_2inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe11_2inch').html(update_null_html());
                    $('#pipe11_2inch').fadeOut(400,function(){
                      $('#pipe11_2inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe2inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>'
                  + '</tr>';
                    for (var i in itemstemp.pipe2inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe2inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe2inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe2inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe2inch[i].weight+'</td></tr>';
                    }
                    $('#pipe2inch').css('background',"none");
                    $('#pipe2inch').html(newhtml);
                    $('#pipe2inch').fadeOut(400,function(){
                      $('#pipe2inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe2inch').html(update_null_html());
                    $('#pipe2inch').fadeOut(400,function(){
                      $('#pipe2inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe21_2inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>'
                  + '</tr>';
                    for (var i in itemstemp.pipe21_2inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe21_2inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe21_2inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe21_2inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe21_2inch[i].weight+'</td></tr>';
                    }
                    $('#pipe21_2inch').css('background',"none");
                    $('#pipe21_2inch').html(newhtml);
                    $('#pipe21_2inch').fadeOut(400,function(){
                      $('#pipe21_2inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe21_2inch').html(update_null_html());
                    $('#pipe21_2inch').fadeOut(400,function(){
                      $('#pipe21_2inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe3inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe3inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe3inch[i].weight+'</td></tr>';
                    }
                    $('#pipe3inch').css('background',"none");
                    $('#pipe3inch').html(newhtml);
                    $('#pipe3inch').fadeOut(400,function(){
                      $('#pipe3inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe3inch').html(update_null_html());
                    $('#pipe3inch').fadeOut(400,function(){
                      $('#pipe3inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe4inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe4inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe4inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe4inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe4inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe4inch[i].weight+'</td></tr>';
                    }
                    $('#pipe4inch').css('background',"none");
                    $('#pipe4inch').html(newhtml);
                    $('#pipe4inch').fadeOut(400,function(){
                      $('#pipe4inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe4inch').html(update_null_html());
                    $('#pipe4inch').fadeOut(400,function(){
                      $('#pipe4inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe5inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe5inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe5inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe5inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe5inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe5inch[i].weight+'</td></tr>';
                    }
                    $('#pipe5inch').css('background',"none");
                    $('#pipe5inch').html(newhtml);
                    $('#pipe5inch').fadeOut(400,function(){
                      $('#pipe5inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe5inch').html(update_null_html());
                    $('#pipe5inch').fadeOut(400,function(){
                      $('#pipe5inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe6inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe6inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe6inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe6inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe6inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe6inch[i].weight+'</td></tr>';
                    }
                    $('#pipe6inch').css('background',"none");
                    $('#pipe6inch').html(newhtml);
                    $('#pipe6inch').fadeOut(400,function(){
                      $('#pipe6inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe6inch').html(update_null_html());
                    $('#pipe6inch').fadeOut(400,function(){
                      $('#pipe6inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe7inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe7inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe7inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe7inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe7inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe7inch[i].weight+'</td></tr>';
                    }
                    $('#pipe7inch').css('background',"none");
                    $('#pipe7inch').html(newhtml);
                    $('#pipe7inch').fadeOut(400,function(){
                      $('#pipe7inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe7inch').html(update_null_html());
                    $('#pipe7inch').fadeOut(400,function(){
                      $('#pipe7inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe8inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe8inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe8inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe8inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe8inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe8inch[i].weight+'</td></tr>';
                    }
                    $('#pipe8inch').css('background',"none");
                    $('#pipe8inch').html(newhtml);
                    $('#pipe8inch').fadeOut(400,function(){
                      $('#pipe8inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe8inch').html(update_null_html());
                    $('#pipe8inch').fadeOut(400,function(){
                      $('#pipe8inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe10inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe10inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe10inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe10inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe10inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe10inch[i].weight+'</td></tr>';
                    }
                    $('#pipe10inch').css('background',"none");
                    $('#pipe10inch').html(newhtml);
                    $('#pipe10inch').fadeOut(400,function(){
                      $('#pipe10inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe10inch').html(update_null_html());
                    $('#pipe10inch').fadeOut(400,function(){
                      $('#pipe10inch').fadeIn();
                    });
                  }
                  if (itemstemp.pipe12inch){
                    var newhtml = '<tr style="background-color:lightgrey">' +
                    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
                    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
                    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
                    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
                    '</tr>';
                    for (var i in itemstemp.pipe12inch){
                      newhtml += '<tr><td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe12inch[i].thickness+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe12inch[i].length+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe12inch[i].qty+'</td>';
                      newhtml += '<td class="col-sm-4" style="border:1px solid">'+itemstemp.pipe12inch[i].weight+'</td></tr>';
                    }
                    $('#pipe12inch').css('background',"none");
                    $('#pipe12inch').html(newhtml);
                    $('#pipe12inch').fadeOut(400,function(){
                      $('#pipe12inch').fadeIn();
                    });
                  }
                  else{
                    $('#pipe12inch').html(update_null_html());
                    $('#pipe12inch').fadeOut(400,function(){
                      $('#pipe12inch').fadeIn();
                    });
                  }
                }
              }
            });
        });

      }
		}
	});
    $(frappe.render_template("pipe_stock_summary")).appendTo(page.main);
    $('.pipeStockSummary').css('display','none');
};

function download_stock(warehouse){
  // console.log('Download stock');
  // frappe.call({
  //   method:'steelpipes.utils.generate_xlsx_item_stock',
  //   args: {
  //     warehouse: warehouse
  //   },
  //   callback: function(r){
  //     console.log(r.message);
  //   }
  // })

  var w = window.open(
    frappe.urllib.get_full_url(
      "/api/method/steelpipes.utils.generate_xlsx_item_stock?"
      ));
  if(!w) {
    frappe.msgprint(__("Please enable pop-ups")); return;
  }
}
function update_null_html(){
  var null_html = '<tr style="background-color:lightgrey">' +
    '<td class="col-sm-4" style="border:1px solid">MM</td>' +
    '<td class="col-sm-4" style="border:1px solid">FEET</td>' +
    '<td class="col-sm-4" style="border:1px solid">QTY</td>' +
    '<td class="col-sm-4" style="border:1px solid">KG</td>' +
  '</tr>' +
  '<tr style="background:#e84545">'+
    '<td class="col-sm-4" style="border:1px solid">---</td>'+
    '<td class="col-sm-4" style="border:1px solid">---</td>' +
    '<td class="col-sm-4" style="border:1px solid">---</td>' +
    '<td class="col-sm-4" style="border:1px solid">---</td>' +
  '</tr>'
  return null_html
}
