

frappe.ui.form.on("Quotation", {
	onload_post_render: function (frm) {
		if (frm.is_new()) {
			frm.set_value("valid_till", "");			
		}
	}
})

