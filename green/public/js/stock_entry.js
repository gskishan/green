frappe.ui.form.on("Stock Entry", { 
    custom_customer: function (frm) {
        if (frm.doc.custom_customer) {
            frappe.call({
                method:"green.green.custom.stock_entry.get_address_display",
                args: {
                    party: frm.doc.custom_customer
                },
                callback: function(response) {
                    var address = response.message
                    console.log(address)
                    if (!response.exc) {

                        frm.set_value("custom_customer_address", address.customer_address);
                        frm.set_value("custom_address_display", address.address_display);
                        frm.set_value("custom_shipping_address_name", address.shipping_address_name);
                        frm.set_value("custom_shipping_address", address.shipping_address);
            
                    }
                }
            })
        }
        if (frm.doc.custom_customer) {
            frm.fields_dict.custom_customer_address.get_query = function (doc, cdt, cdn) {
                var d = locals[cdt][cdn];
                    console.log(d)
                return {
                    filters: {
                        "link_doctype": "Customer",
                        "link_name": d.custom_customer
                    }
                };
            };
        }

        if (frm.doc.custom_customer) {
            frm.fields_dict.custom_shipping_address_name.get_query = function (doc, cdt, cdn) {
                var d = locals[cdt][cdn];
                return {
                    filters: {
                        "link_doctype": "Customer",
                        "link_name": d.custom_customer
                    }
                };
            };
        }
        
    
    },
    custom_customer_address:function(frm){
        if (frm.doc.custom_customer_address){
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Address",
                    name: frm.doc.custom_customer_address,
                },
                callback: function(response) {
                    if (response.message){
                        var address = response.message;
                        console.log(address)
                        var custom_address_display = '';
                        if (address.address_line1) custom_address_display += address.address_line1 + '\n';
                        if (address.address_line2) custom_address_display += address.address_line2 + '\n';
                        if (address.city) custom_address_display += address.city + '\n';
                        if (address.state) custom_address_display += address.state + '\n';
                        if (address.pincode) custom_address_display += address.pincode + '\n';
                        if (address.country) custom_address_display += address.country + '\n';
                        if (address.email_id) custom_address_display += address.email_id + '\n';
                        if (address.phone) custom_address_display += address.phone;

                        // Use cur_frm.set_value to update the field
                        frm.set_value('custom_address_display', custom_address_display);
                    }
                    console.log(response)
                }
            })

        }

    },
    custom_shipping_address_name:function(frm){
        if (frm.doc.custom_shipping_address_name){
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Address",
                    name: frm.doc.custom_shipping_address_name,
                },
                callback: function(response) {
                    if (response.message){
                        var address = response.message;
                        console.log(address)
                        var custom_shipping_address = '';
                        if (address.address_line1) custom_shipping_address += address.address_line1 + '\n';
                        if (address.address_line2) custom_shipping_address += address.address_line2 + '\n';
                        if (address.city) custom_shipping_address += address.city + '\n';
                        if (address.state) custom_shipping_address += address.state + '\n';
                        if (address.pincode) custom_shipping_address += address.pincode + '\n';
                        if (address.country) custom_shipping_address += address.country + '\n';
                        if (address.email_id) custom_shipping_address += address.email_id + '\n';
                        if (address.phone) custom_shipping_address += address.phone;

                        // Use cur_frm.set_value to update the field
                        frm.set_value('custom_shipping_address', custom_shipping_address);
                    }
                    console.log(response)
                }
            })

        }

    },
    custom_dispatch_address_name:function(frm){
        if (frm.doc.custom_dispatch_address_name){
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Address",
                    name: frm.doc.custom_dispatch_address_name,
                },
                callback: function(response) {
                    if (response.message){
                        var address = response.message;
                        console.log(address)
                        var custom_dispatch_address = '';
                        if (address.address_line1) custom_dispatch_address += address.address_line1 + '\n';
                        if (address.address_line2) custom_dispatch_address += address.address_line2 + '\n';
                        if (address.city) custom_dispatch_address += address.city + '\n';
                        if (address.state) custom_dispatch_address += address.state + '\n';
                        if (address.pincode) custom_dispatch_address += address.pincode + '\n';
                        if (address.country) custom_dispatch_address += address.country + '\n';
                        if (address.email_id) custom_dispatch_address += address.email_id + '\n';
                        if (address.phone) custom_dispatch_address += address.phone;

                        // Use cur_frm.set_value to update the field
                        frm.set_value('custom_dispatch_address', custom_dispatch_address);
                    }
                    console.log(response)
                }
            })

        }

    },
   
    company: function(frm){
        if (frm.doc.company){
            frm.fields_dict.custom_dispatch_address_name.get_query = function (doc, cdt, cdn) {
                var d = locals[cdt][cdn];
                    console.log(d)
                return {
                    filters: {
                        "link_doctype": "Company",
                        "link_name": d.company
                    }
                };
            };
        }
    },
})
