
import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from green.utils.naming import set_naming_counter


class CustomPaymentEntry(PaymentEntry):
    def before_save(self):
        set_naming_counter(self)