# Copyright (c) 2024, kushdhallod@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	# columns, data = [], []
	data=get_data(filters)
	columns=get_columns()
	
	return columns, data



def get_data(filters):
	cond=get_cond(filters)
	sql=""" select employee,employee_name,custom_ifsc_code,bank_name,bank_account_no,net_pay,gross_pay from `tabSalary Slip` {0} """.format(cond)



def get_columns():
	columns = [
		{"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Data", "width": 180},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Link","options":"Supplier" ,"width": 180},
		{"label": _("IFSC Code"), "fieldname": "custom_ifsc_code", "fieldtype": "Data", "width": 140},
		{"label": _("Bank Name"), "fieldname": "bank_name", "fieldtype": "Float", "width": 120},
		{"label": _("Bank Account"), "fieldname": "bank_account_no",  "fieldtype": "Float","width": 120},
		{"label": _("Net Pay"), "fieldname": "net_pay", "fieldtype": "Float", "width": 120},
		{"label": _("Gross Pay"), "fieldname": "gross_pay", "fieldtype": "Data", "width": 140},

		
	]

	return columns

def get_cond(filters):
	cond=""
	if filters.get("company"):
		cond=cond+' where company="{0}" '.format(filters.get("company"))
	if filters.get("from_date"):
		cond=cond+' and start_date="{0}" '.format(filters.get("from_date"))
	if filters.get("to_date"):
		cond=cond+' and end_date="{0}" '.format(filters.get("to_date"))
	return cond
