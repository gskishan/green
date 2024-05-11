

frappe.ui.form.on("Lead", {
    refresh(frm) {
        
        setTimeout(() => {
            if (frm.doc.status == "Interested") {
                    frm.clear_custom_buttons();
                    frm.add_custom_button(
                        __("Opportunity"),
                        function () {
                            frm.trigger("make_opportunity");
                        },
                        __("Create")
                    );
            } else {
                frm.remove_custom_button("Opportunity","Create")
            }
        }, 10);
    
    },
    custom_capacity: function (frm) {
        setcapacity_with_uom(frm)
    },
    custom_uom: function (frm) {
        setcapacity_with_uom(frm)
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

function setcapacity_with_uom(frm) {
    
    if (!frm.doc.custom_capacity.endsWith(frm.doc.custom_uom) ) {
        if (frm.doc.custom_capacity.includes(frm.doc.custom_uom)) {
            frm.set_value("custom_capacity", frm.doc.custom_capacity.split(frm.doc.custom_uom).toString().replaceAll(",",""))
        } else {
            let d = frm.doc.custom_capacity.replace("KW", "")
            if (frm.doc.custom_capacity.endsWith("LPD")) {
                d = frm.doc.custom_capacity.replaceAll("LPD", "")
            }
            frm.set_value("custom_capacity", d + frm.doc.custom_uom)
        }
    }
}