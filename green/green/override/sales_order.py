
import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from green.utils.naming import set_naming_counter


class CustomSalesOrder(SalesOrder):
    def before_save(self):
        set_naming_counter(self)