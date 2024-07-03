
import frappe
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt
from green.utils.naming import set_naming_counter


class CustomPurchaseReceipt(PurchaseReceipt):
    def before_save(self):
        set_naming_counter(self)