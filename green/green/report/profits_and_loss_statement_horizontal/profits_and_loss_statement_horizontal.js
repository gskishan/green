frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Profits and Loss Statement Horizontal"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Profits and Loss Statement Horizontal', 10);

	frappe.query_reports["Profits and Loss Statement Horizontal"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
