// Copyright (c) 2024, kushdhallod@gmail.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("CRM Quotation", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Quotation Item', {
    item_code: async function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        let item = await frappe.db.get_doc("Item", row.item_code);
        // row.base_amount = row.qty *row.rate
        row.item_name = item.item_name
        // row.rate = item.rate
        row.uom = item.stock_uom
        row.conversion_factor = 1
    },
    qty(frm, cdt, cdn) {
        caluclateBaseAmount(frm, cdt, cdn)
    },
    rate(frm, cdt, cdn) {
        caluclateBaseAmount(frm, cdt, cdn)
    }
})
async function caluclateBaseAmount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    console.log(frm.doc.items, 'ITEMS')

    if (row.qty && row.rate) {
        row.amount = row.qty * row.rate
        // 
        let totalQty = 0 
        let totalAmount = 0 
        frm.doc.items.map(d => {
            totalAmount += d.amount
            totalQty +=d.qty
        })
        
        // Set Each Accordingly
        frm.set_value("total_qty", totalQty) 
        frm.set_value("total", totalAmount) 
        frm.set_value("net_total", totalAmount) 
        frm.set_value("grand_total", totalAmount) 
        frm.set_value("rounded_total", totalAmount) 
        frm.set_value("base_total", totalAmount) 
        frm.set_value("base_net_total", totalAmount) 
        frm.set_value("base_grand_total", totalAmount) 
        frm.set_value("base_rounded_total", totalAmount) 
        frm.refresh()
    }
}