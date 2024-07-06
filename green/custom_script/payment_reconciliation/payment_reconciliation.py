import frappe, erpnext
from erpnext.accounts.doctype.payment_reconciliation.payment_reconciliation import PaymentReconciliation

class CustomPaymentReconciliation(PaymentReconciliation):
	def get_nonreconciled_payment_entries(self):
		self.check_mandatory_to_fetch()

		payment_entries = self.get_payment_entries() or []
		journal_entries = self.get_jv_entries()

		if self.party_type in ["Customer", "Supplier"]:
			dr_or_cr_notes = self.get_dr_or_cr_notes()
		else:
			dr_or_cr_notes = []

		non_reconciled_payments = payment_entries + journal_entries + dr_or_cr_notes

		if self.payment_limit:
			non_reconciled_payments = non_reconciled_payments[: self.payment_limit]

		non_reconciled_payments = sorted(
			non_reconciled_payments, key=lambda k: k["posting_date"] or getdate(nowdate())
		)

		self.add_payment_entries(non_reconciled_payments)
