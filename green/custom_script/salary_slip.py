import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_slip.salary_slip import *
from frappe.utils import flt
from hrms.hr.utils import  validate_active_employee
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
import json

class CustomSalarySlip(SalarySlip):

	def before_validate(self):
		self.get_late_record()
		
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

	@frappe.whitelist()
	def update_payment_days(self):
		payment_days = self.get('payment_days')
		custom_late_entry_days = self.get('custom_late_entry_days')
	
		if payment_days and payment_days > 1 and custom_late_entry_days >= 3:
			new_payment_days = payment_days - (custom_late_entry_days // 3)
			self.set('payment_days', new_payment_days)


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

