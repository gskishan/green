
import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder
from green.utils.naming import set_naming_counter


class CustomPurchaseOrder(PurchaseOrder):
    def before_save(self):
        set_naming_counter(self)