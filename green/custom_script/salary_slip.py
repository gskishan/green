import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
from frappe.utils import flt, getdate
import json

class CustomSalarySlip(SalarySlip):

    @frappe.whitelist()
    def pull_sal_struct(self):
        from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

        if self.salary_slip_based_on_timesheet:
            self.salary_structure = self._salary_structure_doc.name
            self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
            make_salary_slip(self._salary_structure_doc.name, self)

            self.set("earnings", [])
            self.set("deductions", [])
            base = get_base_amount(self.employee)
            frappe.msgprint(_("Base amount retrieved: {0}").format(base))
            self.hour_rate = (base / self.total_working_days) / 8.0
            frappe.msgprint(_("Hourly rate calculated: {0}").format(self.hour_rate))
            self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
            wages_amount = self.hour_rate * self.total_working_hours
            self.add_earning_for_hourly_wages(
                self, self._salary_structure_doc.salary_component, wages_amount
            )

        else:
            make_salary_slip(self._salary_structure_doc.name, self)

        self.get_late_record()

    @frappe.whitelist()
    def get_late_record(self):
        if self.start_date and self.end_date:
            filters = {
                'from_date': self.start_date,
                'to_date': self.end_date,
                'company': self.company,
                'summarized_view': 1,
                'companies': [self.company]
            }

            data = get_late_entries(self.employee, filters)
            self.custom_late_entry_days = data.get('total_late_entries', 0)
            frappe.msgprint(_("Total late entries: {0}").format(self.custom_late_entry_days))

            # Calculate late leave days based on total late entries
            self.custom_late_leave_days = self.custom_late_entry_days // 3
            frappe.msgprint(_("Total late leave days: {0}").format(self.custom_late_leave_days))

            self.update_payment_days()
            self.add_late_deduction()

    @frappe.whitelist()
    def add_late_deduction(self):
        if self.custom_late_leave_days > 0:
            base = get_base_amount(self.employee)
            deduction_amount = (base / self.total_working_days) * self.custom_late_leave_days
            frappe.msgprint(_("Late attendance deduction amount: {0}").format(deduction_amount))

            late_deduction = next(
                (d for d in self.deductions if d.salary_component == "Late Attendance"), None
            )

            if late_deduction:
                late_deduction.amount = deduction_amount
            else:
                self.append("deductions", {
                    'salary_component': "Late Attendance",
                    'amount': deduction_amount
                })

    @frappe.whitelist()
    def update_payment_days(self):
        if self.payment_days and self.payment_days > 1 and self.custom_late_entry_days >= 3:
            new_payment_days = self.payment_days - (self.custom_late_entry_days // 3)
            frappe.msgprint(_("Updated payment days: {0}").format(new_payment_days))
            self.payment_days = new_payment_days

def get_base_amount(employee):
    # Fetch CTC from Employee doctype
    base_salary = frappe.db.get_value("Employee", employee, "ctc")

    # If CTC is not found in Employee, fetch from Salary Structure Assignment
    if not base_salary:
        assignment = frappe.db.sql("""
            SELECT base FROM `tabSalary Structure Assignment`
            WHERE employee = %s
            ORDER BY from_date DESC
            LIMIT 1
        """, (employee,), as_dict=True)
        base_salary = assignment[0].base if assignment else 0

    frappe.msgprint(_("Base salary (CTC) fetched for Employee {0}: {1}").format(employee, base_salary))
    return base_salary or 0

@frappe.whitelist()
def get_late_entries(employee, filters):
    if isinstance(filters, str):
        filters = json.loads(filters)
    if not isinstance(filters, dict):
        filters = frappe._dict(filters)

    frappe.log_error(f"Fetching late entries for {employee} from {filters.get('from_date')} to {filters.get('to_date')}", "get_late_entries Debug")

    # Fetch late entries based on the salary period
    return get_entry_exits_summary(employee, filters)
