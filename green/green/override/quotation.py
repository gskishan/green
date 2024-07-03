
import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
from green.utils.naming import set_naming_counter


class CustomQuotation(Quotation):
    def before_save(self):
        set_naming_counter(self)