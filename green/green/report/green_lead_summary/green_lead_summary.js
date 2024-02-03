// Copyright (c) 2024, kushdhallod@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Green Lead Summary"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": [
				"",
				"Lead",
				"Open",
				"Replied",
				"Opportunity",
				"Quotation",
				"Lost Quotation",
				"Interested",
				"Converted",
				"Do Not Contact",
			],
		},
		{
			"fieldname": "territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory",
		
		},
	]
};
