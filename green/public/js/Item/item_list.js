frappe.listview_settings['Item'] = {
    onload(listview) {
        frappe.route_options = {
				"disabled": ["=", 0]
        };
        
    }
}