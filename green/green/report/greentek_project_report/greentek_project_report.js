// Copyright (c) 2023, kushdhallod@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Greentek Project Report"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Project Status"),
			"fieldtype": "Select",
			"options":"\nOpen\nCompleted\nCancelled"
		},
	]
};
