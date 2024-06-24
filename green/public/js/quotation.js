


frappe.ui.form.on("Quotation Item", "item_code", function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    if (row.item_code == "CONS 89" && frm.doc.business_unit == "Project") {
        setTimeout(() =>
            frappe.model.set_value(
                cdt,
                cdn,
                "rate",
                flt(frm.doc.items[0].base_amount * 0.3)
            )
        , 100)
    }
});
