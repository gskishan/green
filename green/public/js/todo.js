

frappe.ui.form.on("ToDo", {
    onload: function(frm) {
		frm.set_query("reference_type", function() {
			return{
				"filters": {
					"name": ["in", ["Customer", "Lead"]],
				}
			}
		});
	},

})