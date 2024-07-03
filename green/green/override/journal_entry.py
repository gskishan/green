
import frappe
from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry
from green.utils.naming import set_naming_counter


class CustomJournalEntry(JournalEntry):
    def before_save(self):
        set_naming_counter(self)