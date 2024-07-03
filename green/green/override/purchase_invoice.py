
import frappe
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from green.utils.naming import set_naming_counter


class CustomPurchaseInvoice(PurchaseInvoice):
    def before_save(self):
        set_naming_counter(self)