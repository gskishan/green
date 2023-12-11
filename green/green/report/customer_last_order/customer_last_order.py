import frappe
from frappe import _
from frappe.utils import cint

def execute(filters=None):
	if not filters:
		filters = {}
	
	doctype = filters.get("doctype")

	columns = get_columns()
	customers = get_sales_details(doctype,filters)

	data = []
	for cust in customers:
		cust.insert(7, get_last_sales_amt(cust[0], doctype))
		data.append(cust)
	return columns, data

def get_sales_details(doctype,filters):


	cond = """sum(so.base_net_total) as 'total_order_considered',
		max(so.posting_date) as 'last_order_date',
		DATEDIFF(CURRENT_DATE, max(so.posting_date)) as 'days_since_last_order' """

	date_field = "posting_date"  
	if doctype == "Sales Order":
		date_field = "transaction_date"
		cond = """sum(if(so.status = "Stopped",
			so.base_net_total * so.per_delivered/100,
			so.base_net_total)) as 'total_order_considered',
			max(so.transaction_date) as 'last_order_date',
			DATEDIFF(CURRENT_DATE, max(so.transaction_date)) as 'days_since_last_order'"""
	
	date_filter = ""
	company_filter = "" 
	date_params = []

	if filters.get("company"):
		company = filters.get("company")
		company_filter = f"AND so.company = '{company}'"
			
	if filters.get("from_date") and filters.get("to_date"):

		from_date = filters.get("from_date")
		to_date	= filters.get("to_date")
		date_filter = f"AND DATE(so.{date_field}) BETWEEN %s AND %s "
		date_params = (from_date, to_date)

	sql_query = f"""SELECT
		cust.name,
		cust.customer_name,
		cust.territory,
		cust.customer_group,
		COUNT(DISTINCT so.name) AS 'num_of_order',
		SUM(base_net_total) AS 'total_order_value', {cond}
	FROM `tabCustomer` cust, `tab{doctype}` so
	WHERE cust.name = so.customer
	AND so.docstatus = 1
	{company_filter}
	{date_filter}
	GROUP BY cust.name
	ORDER BY 'days_since_last_order' DESC"""

	return frappe.db.sql(sql_query, tuple(date_params), as_list=1)

def get_last_sales_amt(customer, doctype):
	date_field = "posting_date"  # default date field for other doctypes
	if doctype == "Sales Order":
		date_field = "transaction_date"

	res = frappe.db.sql(
		f"""select base_net_total from `tab{doctype}`
		where customer = %s and docstatus = 1 order by {date_field} desc
		limit 1""",
		customer,
	)
	return res and res[0][0] or 0

def get_columns():
	return [
		_("Customer") + ":Link/Customer:120",
		_("Customer Name") + ":Data:120",
		_("Territory") + "::120",
		_("Customer Group") + "::120",
		_("Number of Order") + "::120",
		_("Total Order Value") + ":Currency:120",
		_("Total Order Considered") + ":Currency:160",
		_("Last Order Amount") + ":Currency:160",
		_("Last Order Date") + ":Date:160",
		_("Days Since Last Order") + "::160",
	]
