


frappe.query_reports["Profits and Loss Statement Horizontal"] = $.extend({}, erpnext.financial_statements);

erpnext.utils.add_dimensions("Profits and Loss Statement Horizontal", 10);

frappe.query_reports["Profits and Loss Statement Horizontal"]["filters"].push({
	fieldname: "selected_view",
	label: __("Select View"),
	fieldtype: "Select",
	options: [
		{ value: "Report", label: __("Report View") },
		{ value: "Growth", label: __("Growth View") },
		{ value: "Margin", label: __("Margin View") },
	],
	default: "Report",
	reqd: 1,
});

frappe.query_reports["Profits and Loss Statement Horizontal"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
	default: 1,
});

frappe.query_reports["Profits and Loss Statement Horizontal"]["filters"].push({
	fieldname: "include_default_book_entries",
	label: __("Include Default FB Entries"),
	fieldtype: "Check",
	default: 1,
});
