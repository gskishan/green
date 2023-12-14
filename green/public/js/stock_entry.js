frappe.ui.form.on("Stock Entry", {
    custom_dispatch_address_name: function(frm) {
        if (frm.doc.custom_dispatch_address_name) {
            console.log(frm.doc.custom_dispatch_address_name);

            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Address",
                    name: frm.doc.custom_dispatch_address_name,
                },
                callback: function(r) {
                    if (r.message) {
                        var address = r.message;
                        console.log(address);
                        
                        var custom_dispatch_address = '';
                        if (address.address_line1) custom_dispatch_address += address.address_line1 + '\n';
                        if (address.address_line2) custom_dispatch_address += address.address_line2 + '\n';
                        if (address.city) custom_dispatch_address += address.city + '\n';
                        if (address.state) custom_dispatch_address += address.state + '\n';
                        if (address.pincode) custom_dispatch_address += address.pincode + '\n';
                        if (address.country) custom_dispatch_address += address.country;

    
                        cur_frm.set_value('custom_dispatch_address', custom_dispatch_address);
                    } else {
                        console.log("Address not found for the given name.");
                        
                    }
                }
            });
        } 
    }
});





// frappe.call({
//     method: "green.green.custom.stock_entry.update_stock_entry_address",
//     args: {
//       stock_name:frm.doc.name
//     },
//     callback: function(response) {
//         console.log(response)
//         if (!response.exc) {
//             console.log(response.message)
//             var address = response.message
//             console.log(address['custom_customer_address'])
//             frm.set_value("custom_customer_address", address['custom_customer_address']);
//             frm.set_value("custom_address", address['custom_address']);
//             frm.set_value("custom_billing_address_gstin", address['custom_billing_address_gstin']);
//             frm.set_value("custom_shipping_address_name", address['custom_shipping_address_name']);
//             frm.set_value("custom_shipping_address_brief", address['custom_shipping_address_brief']);

//         }
//     }
// })