frappe.query_reports["Profits and Loss Statement Horizontal"] = {
	"filters": [
        {
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
        {
			fieldname: "finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book",
		},
		{
			fieldname: "filter_based_on",
			label: __("Filter Based On"),
			fieldtype: "Select",
			options: ["Fiscal Year", "Date Range"],
			default: "Fiscal Year",
			reqd: 1,
			on_change: function () {
				let filter_based_on = frappe.query_report.get_filter_value("filter_based_on");
				frappe.query_report.toggle_filter_display("from_fiscal_year", filter_based_on === "Fiscal Year");
				frappe.query_report.toggle_filter_display("to_fiscal_year", filter_based_on === "Fiscal Year");
				frappe.query_report.toggle_filter_display("period_start_date", filter_based_on === "Date Range");
				frappe.query_report.toggle_filter_display("period_end_date", filter_based_on === "Date Range");

				frappe.query_report.refresh();
			},
		},
        {
			fieldname: "period_start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			reqd: 1,
			depends_on: "eval: frappe.query_report.get_filter_value('filter_based_on') == 'Date Range'",
		},
		{
			fieldname: "period_end_date",
			label: __("End Date"),
			fieldtype: "Date",
			reqd: 1,
			depends_on: "eval: frappe.query_report.get_filter_value('filter_based_on') == 'Date Range'",
		},
        {
			fieldname: "periodicity",
			label: __("Periodicity"),
			fieldtype: "Select",
			options: [
				{ value: "Monthly", label: __("Monthly") },
				{ value: "Quarterly", label: __("Quarterly") },
				{ value: "Half-Yearly", label: __("Half-Yearly") },
				{ value: "Yearly", label: __("Yearly") },
			],
			default: "Yearly",
			reqd: 1,
		},
        {
			fieldname: "from_fiscal_year",
			label: __("Start Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			reqd: 1,
			depends_on: "eval: frappe.query_report.get_filter_value('filter_based_on') == 'Fiscal Year'",
		},
		{
			fieldname: "to_fiscal_year",
			label: __("End Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			reqd: 1,
			depends_on: "eval: frappe.query_report.get_filter_value('filter_based_on') == 'Fiscal Year'",
		},
		{
			fieldname: "presentation_currency",
			label: __("Currency"),
			fieldtype: "Select",
			options: erpnext.get_presentation_currency_list(),
		},
        {
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Cost Center", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Project", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
		},
    ],

    // "onload": function(report) {
    //     // Code to execute when the report is loaded
    // },

    // "formatter": function(value, row, column, data, default_formatter) {
    //     // Custom formatting of values, if needed
    //     return default_formatter(value, row, column, data);
    // },

    // "get_data": function(filters) {
    //     // Replace this with your actual data fetching logic
    //     return frappe.call({
    //         method: "your_app.report.your_report_method",
    //         args: {
    //             filters: filters
    //         }
    //     }).then(function(response) {
    //         return response.message;
    //     });
    // }
};
