

frappe.ui.form.on("Opportunity", {
    opportunity_amount:function(frm) {
      frm.trigger("calculate_probability_amnt")  
    },
    probability: function(frm) {
        frm.trigger("calculate_probability_amnt")
    },
    calculate_probability_amnt: function (frm) {
        if (frm.doc.probability && frm.doc.opportunity_amount) {
            let percentage_amnt = Number(Number(frm.doc.probability / 100) * frm.doc.opportunity_amount).toPrecision(2)
            frm.set_value("custom_percentage_amount",percentage_amnt)
        }
    }
})