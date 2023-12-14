import frappe


# from frappe.contacts.doctype.address.address import get_address_display

@frappe.whitelist()
def get_address_display(party):
    if party:
        from erpnext.accounts.party import get_party_details
        address_display = get_party_details(party)

        return address_display
