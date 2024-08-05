frappe.ui.form.on("Salary Slip", {
	employee:function(frm){
		set_values(frm)
	},
	start_date:function(frm){
		set_values(frm)
	},
	end_date:function(frm){
		set_values(frm)
	},
	payroll_frequency:function(frm){
		set_values(frm)
	},
	refresh: function(frm) {
		if (frm.doc.payment_days && frm.doc.payment_days > 1 && frm.doc.custom_late_entry_days >= 3) {
			let adjusted_payment_days = Number(frm.doc.payment_days - Math.floor(frm.doc.custom_late_entry_days / 3));
			frm.set_value("payment_days", adjusted_payment_days);
			frm.set_value("absent_days", Math.floor(frm.doc.custom_late_entry_days / 3));
			frm.refresh_field("payment_days");
			frm.refresh_field("absent_days");

			recalculate_earnings_and_deductions(frm);
		}
	}
})

function set_values(frm){
	let {custom_late_entry_days, employee, start_date, end_date, payroll_frequency } = frm.doc
		if (employee && start_date && end_date && payroll_frequency == "Monthly"){
			let date = start_date.split("-")
			frm.call({
				method:"green.custom_script.salary_slip.get_late_entries",
				args:{
					employee: frm.doc.employee, 
					filters:{
						'month': date[1], 
						'year': date[0], 
						'company': frm.doc.company, 
						'summarized_view': 1
					}}})
			.then(r=>{
				if(r.message){
					if(r.message.total_late_entries >0){
						frm.set_value("custom_late_entry_days", r.message.total_late_entries)
						frm.refresh_field("custom_late_entry_days")
					}
				}
			})
		}
}

function recalculate_earnings_and_deductions(frm) {
    frappe.call({
        method: "erpnext.payroll.doctype.salary_slip.salary_slip.calculate_earnings",
        args: { doc: frm.doc },
        callback: function(r) {
            if (r.message) {
                frm.set_value("earnings", r.message.earnings);
                frm.refresh_field("earnings");
            }
        }
    });

    frappe.call({
        method: "erpnext.payroll.doctype.salary_slip.salary_slip.calculate_deductions",
        args: { doc: frm.doc },
        callback: function(r) {
            if (r.message) {
                frm.set_value("deductions", r.message.deductions);
                frm.refresh_field("deductions");
            }
        }
    });
}
