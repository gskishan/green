

frappe.ui.form.on("Quotation", {
	onload_post_render: function (frm) {
		if (frm.is_new() && frm.doc.__islocal) {
			frm.set_value(
				"valid_till",
				""
			)
			frm.refresh_field("valid_till")
		}
	}
})

