import frappe


# from frappe.contacts.doctype.address.address import get_address_display

@frappe.whitelist()
def get_address_display(party):
    if party:
        from erpnext.accounts.party import get_party_details
        address_display = get_party_details(party)

        return address_display

@frappe.whitelist()
def add_list_view():
    sql="""select name from `tabDocType` where issingle=0 and istable=0"""
    for d in frappe.db.sql(sql,as_dict=True):
        if d.name!="List View Settings":
            doc=frappe.new_doc("List View Settings")
            doc.__newname=d.name
            doc.disable_count=0
            doc.save()
