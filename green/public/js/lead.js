

frappe.ui.form.on("Lead", {
    status: function(frm) {
        if (frm.doc.status != "Interested") {
            frm.remove_custom_button('Opportunity', 'Create');
        } else {
            frm.add_custom_button(
				__("Opportunity"),
				function () {
					me.frm.trigger("make_opportunity");
				},
				__("Create")
			);
        }   
    },
    custom_capacity: function (frm) {
        if (!frm.doc.custom_capacity.endsWith(frm.doc.custom_uom)) {
            frm.set_value("custom_capacity", frm.doc.custom_capacity + frm.doc.custom_uom)
        }
    },
    custom_customer_category: function (frm) {
        if (frm.doc.custom_customer_category == "Individual") {
            frm.set_df_property(
                "organization_section",
                "hidden",
                1
            );
            frm.set_df_property(
                "custom_poc",
                "hidden",
                1
            );
            frm.refresh()
        } else {
            frm.set_df_property(
                "organization_section",
                "hidden",
                0
            );
            frm.set_df_property(
                "custom_poc",
                "hidden",
                0
            );
            frm.refresh()
        }
    }
})