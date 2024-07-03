
import frappe
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
from green.utils.naming import set_naming_counter


class CustomStockEntry(StockEntry):
    def before_save(self):
        set_naming_counter(self)