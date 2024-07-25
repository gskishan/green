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
	refresh(frm){
		if(frm.doc.payment_days && frm.doc.payment_days > 1 && frm.doc.custom_late_entry_days >= 3){
			frm.set_value("payment_days", Number(frm.doc.payment_days - Math.floor(frm.doc.custom_late_entry_days / 3)))
			frm.refresh_field("payment_days")
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