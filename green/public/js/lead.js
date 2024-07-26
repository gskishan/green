


frappe.ui.form.on('Lead', {
    refresh(frm){
        let temp_status = ["Open",  "Lead", "Do Not Contact", "Replied"]
        let status_needed =[ 'Intake', "Open", 'Inprogress', 'Qualified', 'Not Interested', "Replied"]
        if (!status_needed.includes(frm.doc.status)){
		    frm.set_df_property("custom_lead_status", "hidden", 1);
            frm.refresh_field("custom_lead_status")
        }
    },
    custom_do_not_contact(frm){
        if(frm.doc.custom_do_not_contact){
            frm.set_value("status", "Do Not Contact")
        }
    },
    custom_lead_status(frm){
        let status_needed =[ 'Intake', 'Open', 'Inprogress', 'Qualified', 'Not Interested', "Replied"]
        if(status_needed.includes(frm.doc.status)){
            frm.set_value("status", frm.doc.custom_lead_status)
            frm.refresh_field("status")
        }
    }
})