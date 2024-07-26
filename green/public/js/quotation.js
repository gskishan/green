

frappe.ui.form.on("Quotation", {
	refresh: function (frm) {
		if (frm.is_new()) {
			frm.set_value(
				"valid_till",
				""
			)
		}
	}
})

