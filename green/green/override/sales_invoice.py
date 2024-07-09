
import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from green.utils.naming import set_naming_counter


class CustomSalesInvoice(SalesInvoice):
    def before_save(self):
        set_naming_counter(self)

    def on_cancel(self):
        self.workflow_state = "Cancelled"
        self.db_update()