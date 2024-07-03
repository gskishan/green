
import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from green.utils.naming import set_naming_counter


class CustomDeliveryNote(DeliveryNote):
    def before_save(self):
        set_naming_counter(self)