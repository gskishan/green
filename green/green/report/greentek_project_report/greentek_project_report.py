# Copyright (c) 2023, kushdhallod@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("ID"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Project",
			"width": 150,
		},
		{
			"label": _("Customer Purchase Order Date "),
			"fieldname": "po_date",
			"fieldtype": "Date",
			"width": 150,
		},
		{
			"label": _("Sales Order Date"),
			"fieldname": "so_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"label": _("Project Name"),
			"fieldname": "project_name",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Item Code/Name"),
			"fieldname": "item_code",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Task Stage"),
			"fieldname": "task_stage",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Pending Tasks"),
			"fieldname": "pending_tasks",
			"fieldtype": "Data",
			"width": 200,
		},
	]

def get_conditions(filters):
	conditions = ""

	if filters.get("status"):
		conditions += " and pj.status = %(status)s"
	if filters.get("from_date"):
		conditions += " and date(pj.creation)>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and date(pj.creation)<=%(to_date)s"

	return conditions

def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
        SELECT
            pj.name,
            pj.project_name,
            pj.status,
            so.transaction_date AS 'so_date',
            so.po_date,
            GROUP_CONCAT(DISTINCT sii.item_code) AS 'item_code',
            (
                SELECT GROUP_CONCAT(DISTINCT tk.subject)
                FROM `tabTask` tk
                WHERE tk.project = pj.name
                AND tk.status not in ("Completed", "Cancelled")
            ) AS 'pending_tasks',
            (
                SELECT DISTINCT tk.subject
                FROM `tabTask` tk
                WHERE tk.project = pj.name
                AND tk.status != 'Completed'
                LIMIT 1
            ) AS 'task_stage'
        FROM
            `tabProject` pj
        INNER JOIN
            `tabSales Order` so ON so.name = pj.sales_order
        LEFT JOIN
            `tabSales Order Item` sii ON sii.parent = pj.sales_order
        WHERE 
            pj.docstatus = 0 %s
        GROUP BY
            pj.name, pj.project_name, pj.status, so.transaction_date, so.po_date
        """% conditions,filters,as_dict=1)
	return data