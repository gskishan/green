
frappe.ui.form.on("Expense Claim", {
    setup: function(frm) {
		frm.set_query("payable_account", function() {
			return {
				filters: {
					"report_type": "Balance Sheet",
					"company": frm.doc.company,
					"is_group": 0
				}
			};
		});
	},

})

frappe.ui.form.on('Expense Claim Detail', {
	custom_no_of_kms(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		if (row.custom_no_of_kms) {
			row.amount = row.custom_price_per_km * row.custom_no_of_kms
		} else {
			row.amount = 0
		}
		frm.refresh_field("expenses")
    }
})
