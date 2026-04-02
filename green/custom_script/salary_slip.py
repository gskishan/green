import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import flt, getdate
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
import json


class CustomSalarySlip(SalarySlip):

    @frappe.whitelist()
    def pull_sal_struct(self):
        """Pull salary structure details and calculate hourly wages if applicable."""
        rt = 0
        if self.salary_slip_based_on_timesheet:
            self.salary_structure = self._salary_structure_doc.name
            self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
            make_salary_slip(self._salary_structure_doc.name, self)

            self.set("earnings", [])
            self.set("deductions", [])

            base = get_base_amount(self.employee)
            frappe.msgprint(_("Base amount retrieved: {0}").format(base))

            if self.total_working_days > 0:
                rt = (base / self.total_working_days) / 8.0
                frappe.msgprint(_("Hourly rate calculated: {0}").format(rt))

            self.hour_rate = rt
            self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)

            wages_amount = self.hour_rate * self.total_working_hours
            self.add_earning_for_hourly_wages(
                self, self._salary_structure_doc.salary_component, wages_amount
            )

        self.get_late_record()

    @frappe.whitelist()
    def get_late_record(self):
        """Fetch late entries and calculate deductions."""
        if self.start_date:
            date_parts = str(getdate(self.start_date)).split("-")
            filters = {
                'month': date_parts[1],
                'year': date_parts[0],
                'company': self.company,
                'summarized_view': 1,
                'companies': [self.company]
            }

            data = get_late_entries(self.employee, filters)
            total_late_entries = data.get("total_late_entries", 0)

            self.set("custom_late_entry_days", total_late_entries)
            self.set("custom_late_leave_days", total_late_entries // 3)

            self.update_payment_days()
            self.add_late_deduction()

    def after_insert(self):
        """Ensure the document is saved after insert."""
        self.save()

    @frappe.whitelist()
    def add_late_deduction(self):
        """Apply late entry deduction if applicable."""
        if self.custom_late_leave_days > 0:
            base = get_base_amount(self.employee)
            deduction_amount = (base / self.total_working_days) * self.custom_late_leave_days

            for deduction in self.deductions:
                if deduction.salary_component == "Late Attendance":
                    deduction.amount = deduction_amount
                    break
            else:
                deduct = self.append("deductions", {})
                deduct.salary_component = "Late Attendance"
                deduct.amount = deduction_amount

    @frappe.whitelist()
    def update_payment_days(self):
        """Reduce payment days based on late entries."""
        payment_days = self.get("payment_days", 0)
        custom_late_entry_days = self.get("custom_late_entry_days", 0)

        if payment_days > 1 and custom_late_entry_days >= 3:
            self.set("payment_days", payment_days - (custom_late_entry_days // 3))


@frappe.whitelist()
def get_base_amount(employee):
    """Fetch base salary amount, prioritizing CTC from Employee doctype."""
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
    """Fetch late entry details for an employee."""
    if isinstance(filters, str):
        filters = json.loads(filters)
    if not isinstance(filters, frappe._dict):
        filters = frappe._dict(filters)

    return get_entry_exits_summary(employee, filters)
