import frappe
from frappe import msgprint, _
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from erpnext.accounts.doctype.payment_entry.payment_entry import *

class CustomPaymentEntry(PaymentEntry):
	def validate_reference_documents(self):
		valid_reference_doctypes = self.get_valid_reference_doctypes()

		if not valid_reference_doctypes:
			return
		frappe.errprint([valid_reference_doctypes,"valid_reference_doctypes"])
		for d in self.get("references"):
			if not d.allocated_amount:
				continue

			if d.reference_doctype not in valid_reference_doctypes:
				frappe.errprint([(d) for d in valid_reference_doctypes])
				frappe.throw(
					_("Reference Doctype must be one of {0}").format(
						comma_or(_(d) for d in valid_reference_doctypes)
					)
				)
			elif d.reference_name:
				if not frappe.db.exists(d.reference_doctype, d.reference_name):
					frappe.throw(_("{0} {1} does not exist").format(d.reference_doctype, d.reference_name))
				else:
					ref_doc = frappe.get_doc(d.reference_doctype, d.reference_name)

					if d.reference_doctype != "Journal Entry":
						if self.party != ref_doc.get(scrub(self.party_type)):
							frappe.throw(
								_("{0} {1} is not associated with {2} {3}").format(
									_(d.reference_doctype), d.reference_name, _(self.party_type), self.party
								)
							)
					else:
						self.validate_journal_entry()

					if d.reference_doctype in frappe.get_hooks("invoice_doctypes"):
						if self.party_type == "Customer":
							ref_party_account = (
								get_party_account_based_on_invoice_discounting(d.reference_name)
								or ref_doc.debit_to
							)
						elif self.party_type == "Supplier":
							ref_party_account = ref_doc.credit_to
						elif self.party_type == "Employee":
							ref_party_account = ref_doc.payable_account

						if (
							ref_party_account != self.party_account
							and not self.book_advance_payments_in_separate_party_account
						):
							frappe.throw(
								_("{0} {1} is associated with {2}, but Party Account is {3}").format(
									_(d.reference_doctype),
									d.reference_name,
									ref_party_account,
									self.party_account,
								)
							)

						if ref_doc.doctype == "Purchase Invoice" and ref_doc.get("on_hold"):
							frappe.throw(
								_("{0} {1} is on hold").format(_(d.reference_doctype), d.reference_name),
								title=_("Invalid Purchase Invoice"),
							)

					if ref_doc.docstatus != 1:
						frappe.throw(
							_("{0} {1} must be submitted").format(_(d.reference_doctype), d.reference_name)
						)

	def get_valid_reference_doctypes(self):
		if self.party_type == "Customer":
			return ("Sales Order", "Sales Invoice", "Journal Entry", "Dunning", "Payment Entry")
		elif self.party_type == "Supplier":
			return ("Purchase Order", "Purchase Invoice", "Journal Entry", "Payment Entry")
		elif self.party_type == "Shareholder":
			return ("Journal Entry",)
		elif self.party_type == "Employee":
			return ("Journal Entry",)
