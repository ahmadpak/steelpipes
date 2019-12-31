// Copyright (c) 2019, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplier Balance Report Generator", {
  download_report: function(frm) {
    var doc = cur_frm.doc;
    if (doc.balance_less_than == undefined && doc.all_balances == 0) {
      frappe.throw("Please enter value for Balance less than");
    }
    if (
      doc.get_advances == 1 &&
      doc.balance_less_than >= 0 &&
      doc.all_balances == 0
    ) {
      frappe.throw("Balance less than must be negative to get advances");
    }
    if (
      doc.get_advances == 0 &&
      doc.balance_less_than <= 0 &&
      doc.all_balances == 0
    ) {
      frappe.throw("Balance less than must be greater than zero");
    }
    if (!doc.company) {
      frappe.throw("Please select a company");
    }
		frm.save();
		if (!doc.supplier_group){
			doc.supplier_group = ''
		}
    frappe.call({
      method:
        "steelpipes.sp_purchase_invoice.doctype.supplier_balance_report_generator.supplier_balance_report_generator.generate_supplier_balance",
      args: {
        data: {
          company: doc.company,
					supplier_group: doc.supplier_group,
					supplier_type: doc.supplier_type,
          balance_less_than: doc.balance_less_than,
          get_advances: doc.get_advances,
          all_balances: doc.all_balances
        }
      },
      callback: function(r) {
        download_stock();
      }
    });
  }
});

function download_stock() {
  var w = window.open(
    frappe.urllib.get_full_url(
      "/api/method/steelpipes.sp_purchase_invoice.doctype.supplier_balance_report_generator.supplier_balance_report_generator.generate_xlsx_supplier_balance?"
    )
  );
  if (!w) {
    frappe.msgprint(__("Please enable pop-ups"));
    return;
  }
}
