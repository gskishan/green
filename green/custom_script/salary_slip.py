import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_slip.salary_slip import *
from frappe.utils import flt
from hrms.hr.utils import  validate_active_employee
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
		rt=0
		if self.salary_slip_based_on_timesheet:
			self.salary_structure = self._salary_structure_doc.name
			self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
			make_salary_slip(self._salary_structure_doc.name, self)
			# deduct=0
			# for d in self.deductions:
			# 	if d.salary_component=='Provident Fund Employee' or  d.salary_component=='ESIC Employer':
			# 		deduct+=d.amount
			# adding=0
			# for e in self.earnings:
			# 	if e.salary_component == 'Basic' or e.salary_component == 'Conveyance Allowance' or e.salary_component == 'House Rent Allowance' or e.salary_component == 'Medical Allowance':
			# 		adding += e.amount
			
			self.set("earnings", [])
			self.set("deductions", [])
			base=get_base_amount(self.employee)
			frappe.msgprint(_("Base amount retrieved: {0}").format(base))
			rt = ((base / self.total_working_days) / 8.0)
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

	def get_working_days_details(self, lwp=None, for_preview=0):
		payroll_settings = frappe.get_cached_value(
			"Payroll Settings",
			None,
			(
				"payroll_based_on",
				"include_holidays_in_total_working_days",
				"consider_marked_attendance_on_holidays",
				"daily_wages_fraction_for_half_day",
				"consider_unmarked_attendance_as",
			),
			as_dict=1,
		)

		consider_marked_attendance_on_holidays = (
			payroll_settings.include_holidays_in_total_working_days
			and payroll_settings.consider_marked_attendance_on_holidays
		)

		daily_wages_fraction_for_half_day = flt(payroll_settings.daily_wages_fraction_for_half_day) or 0.5

		working_days = date_diff(self.end_date, self.start_date) + 1
		if for_preview:
			self.total_working_days = working_days
			self.payment_days = working_days
			return

		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
		working_days_list = [add_days(getdate(self.start_date), days=day) for day in range(0, working_days)]

		if not cint(payroll_settings.include_holidays_in_total_working_days):
			working_days_list = [i for i in working_days_list if i not in holidays]

			working_days -= len(holidays)
			if working_days < 0:
				frappe.throw(_("There are more holidays than working days this month."))

		if not payroll_settings.payroll_based_on:
			frappe.throw(_("Please set Payroll based on in Payroll settings"))

		if payroll_settings.payroll_based_on == "Attendance":
			actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(
				holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
			)
			self.absent_days = absent
		else:
			actual_lwp = self.calculate_lwp_or_ppl_based_on_leave_application(
				holidays, working_days_list, daily_wages_fraction_for_half_day
			)

		if not lwp:
			lwp = actual_lwp
		elif lwp != actual_lwp:
			frappe.msgprint(
				_("Leave Without Pay does not match with approved {} records").format(
					payroll_settings.payroll_based_on
				)
			)

		self.leave_without_pay = lwp
		self.total_working_days = working_days

		payment_days = self.get_payment_days(payroll_settings.include_holidays_in_total_working_days)

		if flt(payment_days) > flt(lwp):
			self.payment_days = flt(payment_days) - flt(lwp)

			if payroll_settings.payroll_based_on == "Attendance":
				self.payment_days -= flt(absent)

			consider_unmarked_attendance_as = payroll_settings.consider_unmarked_attendance_as or "Present"

			if (
				payroll_settings.payroll_based_on == "Attendance"
				and consider_unmarked_attendance_as == "Absent"
			):
				unmarked_days = self.get_unmarked_days(
					payroll_settings.include_holidays_in_total_working_days, holidays
				)
				self.absent_days += unmarked_days  # will be treated as absent
				self.payment_days -= unmarked_days
		else:
			self.payment_days = 0
		self.payment_days = (self.payment_days or 0) - (self.absent_days or 0)
		
	@frappe.whitelist()
	def get_late_record(self):
		date= self.start_date.split("-")
		filters={
			'month': date[1], 
			'year': date[0], 
			'company': self.company, 
			'summarized_view': 1
			}

		data=get_late_entries(self.employee,filters)
		self.set("custom_late_entry_days",data.total_late_entries)
		self.update_payment_days()
		self.set('custom_late_leave_days', (self.custom_late_entry_days // 3))
		self.add_late_deduction()


	@frappe.whitelist()
	def add_late_deduction(self):
		if self.custom_late_leave_days>0:
			base=get_base_amount(self.employee)
			rt = ((base / self.total_working_days) * self.custom_late_leave_days)
			update=True
			for s in self.deductions:
				if s.salary_component=="Late Attendance":
					s.amount=rt
					update=False
					

					
			if update:	
				deduct=self.append("deductions",{})
				deduct.salary_component="Late Attendance"
				deduct.amount=rt




	@frappe.whitelist()
	def update_payment_days(self):
		self.payment_days = (self.payment_days or 0) - (self.absent_days or 0)
		payment_days = self.get('payment_days')
		custom_late_entry_days = self.get('custom_late_entry_days')
	
		if payment_days and payment_days > 1 and custom_late_entry_days >= 3:
			new_payment_days = payment_days - (custom_late_entry_days // 3)
			self.set('payment_days', new_payment_days)
		
		

def get_base_amount(employee):
	sql="""select base from `tabSalary Structure Assignment` where employee="{0}" """.format(employee)
	base=frappe.db.sql(sql,as_dict=True)
	if base:
		return base[0].base
	else:
		frappe.msgprint("issue in finding salary assigment")
		return 0





@frappe.whitelist()
def get_late_entries(employee, filters):
    if isinstance(filters, str):
        filters = json.loads(filters)
    if not isinstance(filters, frappe._dict):
        filters = frappe._dict(filters)
    return get_entry_exits_summary(employee, filters)
