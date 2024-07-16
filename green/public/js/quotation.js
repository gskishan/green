

frappe.ui.form.on("Quotation", {
	refresh: function (frm) {
		if (frm.is_new()) {
			frm.set_value(
				"valid_till",
				frappe.datetime.add_days(
						frm.doc.transaction_date,
						frappe.boot.sysdefaults.quotation_valid_till
					)
				)
		}
	}
})

