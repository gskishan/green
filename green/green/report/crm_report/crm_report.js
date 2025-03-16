// Copyright (c) 2025, kushdhallod@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["CRM Report"] = {
       "filters": [
    {
        "fieldname": "reference_type",
        "label": "Doctype",
        "fieldtype": "Select",
        "options": "\nCustomer\nLead",
        "default": "",
        "on_change": function (query_report) {
            let reference_type = frappe.query_report.get_filter_value("reference_type");
            let reference_name_filter = frappe.query_report.get_filter("reference_name");

            if (reference_type === "Customer") {
                reference_name_filter.df.options = "Customer";
            } else if (reference_type === "Lead") {
                reference_name_filter.df.options = "Lead";
            } else {
                reference_name_filter.df.options = "";
            }
            
            reference_name_filter.set_value("");  // Reset selection
            reference_name_filter.refresh();
        }
    },
    {
        "fieldname": "reference_name",
        "label": "Customer/Lead",
        "fieldtype": "Link",
        "options": "Customer",  // This will be updated dynamically
        "default": ""
    },
    {
        "fieldname": "from_date",
        "label": "From Date",
        "fieldtype": "Date",
        "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30)
    },
    {
        "fieldname": "to_date",
        "label": "To Date",
        "fieldtype": "Date",
        "default": frappe.datetime.get_today()
    }
],

};
