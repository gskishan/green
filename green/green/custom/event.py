import frappe


# from frappe.contacts.doctype.address.address import get_address_display

@frappe.whitelist()
def validate(self,method=None):
    pass
    # self.event_type="Public"
    # frappe.errprint([self.event_type,self.owner])
