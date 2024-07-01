# Copyright (c) 2024, kushdhallod@gmail.com and contributors
# For license information, please see license.txt

import frappe

from frappe import _, _dict
import json


def execute(filters=None):
	columns, data = get_columns(), []
	data.append({
		"customer":"Test",
		"project_name":"Test",
		"sales_person":"Test",
		"sales_order":"SO-9877",
		"sales_order_value": 34567,
		"payment_recieved": 4356,
		"balance": 7890
	})
	company = ''
	customer = '' 
	from_date = ''
	to_date = ''

	if "company" in filters:
		company = filters["company"]
	
	if "customer" in filters:
		customer = filters["customer"]

	
	if "from_date" in filters:
		from_date = filters["from_date"]


	if "to_date" in filters:
		to_date = filters["to_date"]
	# print('ALL FILTERS ARE ASSIGNED PRoperly \n\n\n\n\n', filters)
	customers = get_all_customer(company, customer)
	for each_customer in customers:
		print(each_customer["name"], 'Each Customer \n')
		sales_team = frappe.get_list("Sales Team", {"parent": each_customer["name"]},fields=["*"])
		print(sales_team['sales_person'], "Sales Team \n\n\n\n\n")
		# Get All Sales Order of this Customer
		# sales_orders = get_sales_order(company, customer, from_date, to_date)
		# for each_sales_order in sales_orders:
		# 	print(each_sales_order, 'Each Sales ORder \n\n\n\n')

	return columns, data

def get_all_customer(company, customer):
	filters={}
	if company:
		filters['custom_company'] = company
	# print(customer, 'CUSTOMER Filter \n\n\n\n\nn\n')
	if customer:
		filters['name'] = customer
	# print(filters, 'LOCAL FILTER')
	# Get Customer
	customers = frappe.db.get_list('Customer',
		filters=filters,
		fields=['*'],
	)
	# print(customers[0], 'CUSTOMERS \n\n')
	return customers

def get_sales_order(company, customer, from_date, to_date):
	filters={}
	if company:
		filters['company'] = company
	
	if customer:
		filters['customer'] = customer
	
	if from_date and to_date:
		filters["creation"] = ["between", [from_date, to_date]]

	# Get Sales Order
	sales_orders = frappe.db.get_all('Sales Order',
		filters=filters,
		fields=['*'],
	)
	return sales_orders


def get_columns():
	return [
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options":"Customer",
			"width": 180,
		},
		{
			"label": _("Project Name"),
			"fieldname": "project_name",
			"fieldtype": "Data",
			# "options":"Project",
			"width": 260,
		},
		{
			"label": _("Sales Person"),
			"fieldname": "sales_person",
			"fieldtype": "Link",
			"options":"Sales Person",
			"width": 150,
		},
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options":"Sales Order",
			"width": 180,
		},
		{
			"label": _("Sales Order Value"),
			"fieldname": "sales_order_value",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Paymet Received"),
			"fieldname": "payment_recieved",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"width": 150,
		},
	]