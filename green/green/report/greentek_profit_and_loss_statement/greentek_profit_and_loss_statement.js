// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// frappe.require("assets/erpnext/js/financial_statements.js", function () {
// 	frappe.query_reports["G Profit and Loss Statement"] = $.extend({}, erpnext.financial_statements);

	// erpnext.utils.add_dimensions("Profit and Loss Statement", 10);

	// frappe.query_reports["G Profit and Loss Statement"]["filters"].push({
	// 	fieldname: "selected_view",
	// 	label: __("Select View"),
	// 	fieldtype: "Select",
	// 	options: [
	// 		{ value: "Report", label: __("Report View") },
	// 		{ value: "Growth", label: __("Growth View") },
	// 		{ value: "Margin", label: __("Margin View") },
	// 	],
	// 	default: "Report",
	// 	reqd: 1,
	// });

	// frappe.query_reports["G Profit and Loss Statement"]["filters"].push({
	// 	fieldname: "include_default_book_entries",
	// 	label: __("Include Default Book Entries"),
	// 	fieldtype: "Check",
	// 	default: 1,
	// });
// });
frappe.query_reports["Greentek Profit and Loss Statement"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": "Quality Specialized Health Food Co. Ltd.",
            "reqd": 1,
            "placeholder": __("Company"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "finance_book",
            "label": __("Finance Book"),
            "fieldtype": "Link",
            "options": "Finance Book",
            "placeholder": __("Finance Book"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "filter_based_on",
            "label": __("Filter Based On"),
            "fieldtype": "Select",
            "options": [
                "Fiscal Year",
                "Date Range"
            ],
            "default": "Fiscal Year",
            "reqd": 1,
            "placeholder": __("Filter Based On"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "period_start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "depends_on": "eval:doc.filter_based_on == 'Date Range'",
            "placeholder": __("Start Date"),
            "input_class": "input-xs",
            "hidden_due_to_dependency": true
        },
        {
            "fieldname": "period_end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "depends_on": "eval:doc.filter_based_on == 'Date Range'",
            "placeholder": __("End Date"),
            "input_class": "input-xs",
            "hidden_due_to_dependency": true
        },
        {
            "fieldname": "from_fiscal_year",
            "label": __("Start Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "default": "2023",
            "reqd": 1,
            "depends_on": "eval:doc.filter_based_on == 'Fiscal Year'",
            "placeholder": __("Start Year"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "to_fiscal_year",
            "label": __("End Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "default": "2023",
            "reqd": 1,
            "depends_on": "eval:doc.filter_based_on == 'Fiscal Year'",
            "placeholder": __("End Year"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "periodicity",
            "label": __("Periodicity"),
            "fieldtype": "Select",
            "options": [
                { "value": "Monthly", "label": __("Monthly") },
                { "value": "Quarterly", "label": __("Quarterly") },
                { "value": "Half-Yearly", "label": __("Half-Yearly") },
                { "value": "Yearly", "label": __("Yearly") }
            ],
            "default": "Yearly",
            "reqd": 1,
            "placeholder": __("Periodicity"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "presentation_currency",
            "label": __("Currency"),
            "fieldtype": "Select",
            "options": [
                "", "AED", "AUD", "CHF", "CNY", "EUR", "GBP", "INR", "JPY", "SAR", "USD"
            ],
            "placeholder": __("Currency"),
            "input_class": "input-xs"
        },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "MultiSelectList",
            "placeholder": __("Cost Center"),
            "input_class": "input-xs"
        }
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


