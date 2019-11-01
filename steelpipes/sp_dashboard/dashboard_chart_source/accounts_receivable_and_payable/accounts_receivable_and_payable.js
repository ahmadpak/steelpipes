frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["Accounts receivable and payable"] = {
	method: "steelpipes.sp_dashboard.dashboard_chart_source.accounts_receivable_and_payable.accounts_receivable_and_payable.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
	]
};