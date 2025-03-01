import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_slip.salary_slip import *
from frappe.utils import flt
from hrms.hr.utils import validate_active_employee
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
import json
from frappe.utils import (
	add_days,
	ceil,
	cint,
	cstr,
	date_diff,
	floor,
	flt,
	formatdate,
	get_first_day,
	get_link_to_form,
	getdate,
	money_in_words,
	rounded,
)

class CustomSalarySlip(SalarySlip):

	@frappe.whitelist()
	def pull_sal_struct(self):
		from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
		rt = 0
		if self.salary_slip_based_on_timesheet:
			self.salary_structure = self._salary_structure_doc.name
			self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
			make_salary_slip(self._salary_structure_doc.name, self)

			self.set("earnings", [])
			self.set("deductions", [])
			base = get_base_amount(self.employee)
			frappe.msgprint(_("Base amount retrieved: {0}").format(base))
			rt = (base / self.total_working_days) / 8.0
			frappe.msgprint(_("Base amount retrieved: {0}").format(rt))
			self.hour_rate = rt
			self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
			wages_amount = self.hour_rate * self.total_working_hours
			self.add_earning_for_hourly_wages(
				self, self._salary_structure_doc.salary_component, wages_amount
			)

		make_salary_slip(self._salary_structure_doc.name, self)
		if self.salary_slip_based_on_timesheet:
			self.hour_rate = rt

		self.get_late_record()

	@frappe.whitelist()
	def get_late_record(self):
		if self.start_date:
			if isinstance(self.start_date, str):
				date = self.start_date.split("-")
			else:
				date = self.start_date.strftime("%Y-%m-%d").split("-")
			filters = {
				'month': date[1],
				'year': date[0],
				'company': self.company,
				'summarized_view': 1,
				'companies': [self.company]
			}

			data = get_late_entries(self.employee, filters)
			self.set("custom_late_entry_days", data.total_late_entries)

			# Calculate late leave days based on total late entries without any deduction
			self.set('custom_late_leave_days', (self.custom_late_entry_days // 3))
			self.update_payment_days()
			self.add_late_deduction()

	def after_insert(self):
		self.save()

	@frappe.whitelist()
	def add_late_deduction(self):
		if self.custom_late_leave_days > 0:
			base = get_base_amount(self.employee)
			rt = ((base / self.total_working_days) * self.custom_late_leave_days)
			update = True
			for s in self.deductions:
				if s.salary_component == "Late Attendance":
					s.amount = rt
					update = False

			if update:
				deduct = self.append("deductions", {})
				deduct.salary_component = "Late Attendance"
				deduct.amount = rt

	@frappe.whitelist()
	def update_payment_days(self):
		payment_days = self.get('payment_days')
		custom_late_entry_days = self.get('custom_late_entry_days')

		if payment_days and payment_days > 1 and custom_late_entry_days >= 3:
			new_payment_days = payment_days - (custom_late_entry_days // 3)
			self.set('payment_days', new_payment_days)

def get_base_amount(employee):
    # Fetch CTC from Employee doctype
    base_salary = frappe.db.get_value("Employee", employee, "ctc")

    # If CTC is not found in Employee, fetch from Salary Structure Assignment
    if not base_salary:
        sql = """
            SELECT base FROM `tabSalary Structure Assignment`
            WHERE employee = %s
            ORDER BY from_date DESC
            LIMIT 1
        """
        assignment = frappe.db.sql(sql, (employee,), as_dict=True)
        base_salary = assignment[0].base if assignment else 0

    # Log and return base salary
    frappe.msgprint(_("Base salary (CTC) fetched for Employee {0}: {1}").format(employee, base_salary))

    return base_salary if base_salary else 0

@frappe.whitelist()
def get_late_entries(employee, filters):
	if isinstance(filters, str):
		filters = json.loads(filters)
	if not isinstance(filters, frappe._dict):
		filters = frappe._dict(filters)
	# frappe.log_error(f"Employee: {employee}, Filters: {filters}", "get_late_entries Debug")
	return get_entry_exits_summary(employee, filters)
