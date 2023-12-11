import frappe


@frappe.whitelist()
def validate(doc, method):
    if doc.customer:
        addr_links = frappe.db.get_value("Dynamic Link", {
            "parenttype": "Address",
            "link_doctype": "Customer",
            "link_name": doc.customer
        }, "parent")
        if addr_links:
            addr_doc = frappe.get_doc("Address", addr_links)
            if addr_doc.is_primary_address == 1:
                doc.custom_customer_address = addr_doc.name
                doc.custom_address = construct_address(addr_doc)
            if addr_doc.is_shipping_address == 1:
                doc.custom_shipping_address_name = addr_doc.name
                doc.custom_shipping_address_brief = construct_shipping_address(addr_doc)


def construct_address(addr_doc):
    address_lines = []
    if addr_doc.address_line1:
        address_lines.append(addr_doc.address_line1)
    if addr_doc.address_line2:
        address_lines.append(addr_doc.address_line2)
    if addr_doc.city:
        address_lines.append(addr_doc.city)
    if addr_doc.state:
        address_lines.append(addr_doc.state)
    if addr_doc.pincode:
        address_lines.append(addr_doc.pincode)
    if addr_doc.country:
        address_lines.append(addr_doc.country)
    if addr_doc.email_id:
        address_lines.append(addr_doc.email_id)
    if addr_doc.gstin:
        address_lines.append(addr_doc.gstin)

    return '\n'.join(address_lines)


def construct_shipping_address(addr_doc):
    shipping_address_lines = []
    if addr_doc.address_line1:
        shipping_address_lines.append(addr_doc.address_line1)
    if addr_doc.address_line2:
        shipping_address_lines.append(addr_doc.address_line2)
    if addr_doc.city:
        shipping_address_lines.append(addr_doc.city)
    if addr_doc.state:
        shipping_address_lines.append(addr_doc.state)

    return '\n'.join(shipping_address_lines)
