
import frappe
from hrms.hr.doctype.expense_claim.expense_claim import ExpenseClaim
from green.utils.naming import set_naming_counter


class CustomExpenseClaim(ExpenseClaim):
    def before_save(self):
        set_naming_counter(self)