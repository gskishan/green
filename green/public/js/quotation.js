

frappe.ui.form.on("Quotation", {
    refresh: function(frm) {
		frm.set_value(
			"valid_till",
			frappe.datetime.add_days(
				doc.transaction_date,
				frappe.boot.sysdefaults.quotation_valid_till
			)
		)
	}
})

