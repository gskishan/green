// Copyright (c) 2023, kushdhallod@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Last Order"] = {
	"filters": [

		{
			"fieldname":"doctype",
			"label": __("Doctype"),
			"fieldtype": "Select",
			"default": "Sales Order",
			"options": "Sales Order\nSales Invoice"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		
		}

	]
};



