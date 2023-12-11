// frappe.ui.form.on("Stock Entry", {
// 	validate: function(frm) {
//         frappe.call({
//             method: "green.green.custom.stock_entry.update_stock_entry_address",
//             args: {
//               stock_name:frm.doc.name
//             },
//             callback: function(response) {
//                 console.log(response)
//                 if (!response.exc) {
//                     console.log(response.message)
//                     var address = response.message
//                     console.log(address['custom_customer_address'])
//                     frm.set_value("custom_customer_address", address['custom_customer_address']);
//                     frm.set_value("custom_address", address['custom_address']);
//                     frm.set_value("custom_billing_address_gstin", address['custom_billing_address_gstin']);
//                     frm.set_value("custom_shipping_address_name", address['custom_shipping_address_name']);
//                     frm.set_value("custom_shipping_address_brief", address['custom_shipping_address_brief']);

//                 }
//             }
//         })	
//     }
// });