# Copyright (c) 2024, kushdhallod@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _

import frappe
from frappe.utils import money_in_words

@frappe.whitelist()
def get_money_in_words(amount, currency):
    return money_in_words(amount, currency)

def execute(filters=None):
	# columns, data = [], []
	data=get_data(filters)
	columns=get_columns()
	
	return columns, data



def get_data(filters):
	cond=get_cond(filters)
	sql=""" select employee,employee_name,custom_ifsc_code,bank_name,bank_account_no,net_pay from `tabSalary Slip` {0} """.format(cond)
	frappe.errprint(sql)
	return frappe.db.sql(sql,as_dict=1)



def get_columns():
	columns = [
		{"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Link","options":"Employee", "width": 160},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data" ,"width": 200},
		{"label": _("Bank Name"), "fieldname": "bank_name", "fieldtype": "Data", "width": 200},
		{"label": _("Bank Account"), "fieldname": "bank_account_no",  "fieldtype": "Data","width": 200},
		{"label": _("IFSC Code"), "fieldname": "custom_ifsc_code", "fieldtype": "Data", "width": 120},
		# {"label": _("Gross Pay"), "fieldname": "gross_pay", "fieldtype": "Float", "width": 80},
		{"label": _("Net Pay"), "fieldname": "net_pay", "fieldtype": "Float", "width": 100},

		
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
