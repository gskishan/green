
frappe.ui.form.on("CRM Deal", {
    refresh: function(frm) {
		if (frm.doc.status == "Proposal/Quotation") {
			frm.add_custom_button(__("Create  Quotation"), function () {
				// Get Contact Person from List of Contacts
				let contactPerson = ''
				frm.doc.contacts.map(d => {
					if (d.is_primary) {
						contactPerson = d.contact
					}
				})
				// Redirect with params
				frappe.route_options = {
					"organization": frm.doc.organization,
					"customer_name": frm.doc.organization,
					"website": frm.doc.website,
					"territory": frm.doc.territory,
					"annual_revenue": frm.doc.annual_revenue,
					"close_date": frm.doc.close_date,
					"probability": frm.doc.probability,
					"lead": frm.doc.lead,
					"lead_source": frm.doc.source,
					"lead_name": frm.doc.lead_name,
					"deal_owner": frm.doc.deal_owner,
					"mobile_no": frm.doc.mobile_no,
					"email": frm.doc.email,
					"deal": frm.doc.name,
					"contact_person": contactPerson,
				};
				
				frappe.set_route('Form', 'CRM Quotation', "new-crm-quotation");
			}, __());
		}
	},

})