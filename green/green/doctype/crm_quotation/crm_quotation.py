# Copyright (c) 2024, kushdhallod@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMQuotation(Document):
	@frappe.whitelist()
	def update_date(self):
		for d in get_data():
			if d.get('valid_till'):
				doc=frappe.get_doc("Quotation",d.get("quotation"))
				if doc.docstatus==1:
					doc.db_set("valid_till",None)
					doc.db_set("status",'Open')




def get_data():
	return [
  {
    "Sr": 1,
    "ID": "QTN-00974-1",
    "Docstatus": 1,
    "Date": "2024-07-25",
    "Valid Till": "2024-07-25",
    "Party": "Sri Rama Krishna Solar Power System",
    "Title": "Sri Rama Krishna Solar Power System",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 2049264,
    "Grand Total (Company Currency)": 2049264,
    "Company": "Greentek India Limited",
    "Customer Name": "Sri Rama Krishna Solar Power System"
  },
  {
    "Sr": 2,
    "ID": "QTN-00977",
    "Docstatus": 1,
    "Date": "2024-07-26",
    "Valid Till": "2024-07-26",
    "Party": "LEAD-206210887",
    "Title": "Mr AZMADDIN MD",
    "Quotation To": "Lead",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 300000,
    "Grand Total (Company Currency)": 300000,
    "Company": "Greentek India Limited",
    "Customer Name": "Mr AZMADDIN MD"
  },
  {
    "Sr": 3,
    "ID": "QTN-00976",
    "Docstatus": 1,
    "Date": "2024-07-26",
    "Valid Till": "2024-07-26",
    "Party": "LEAD-206211777",
    "Title": "Mr Ravi Kiran",
    "Quotation To": "Lead",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 204000,
    "Grand Total (Company Currency)": 204000,
    "Company": "Greentek India Limited",
    "Customer Name": "Mr Ravi Kiran"
  },
  {
    "Sr": 4,
    "ID": "QTN-00975-1",
    "Docstatus": 1,
    "Date": "2024-07-25",
    "Valid Till": "2024-07-25",
    "Party": "Satya Enterprises",
    "Title": "Satya Enterprises",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 276358.5,
    "Grand Total (Company Currency)": 276358.5,
    "Company": "Greentek India Limited",
    "Customer Name": "Satya Enterprises"
  },
  {
    "Sr": 5,
    "ID": "QTN-00961",
    "Docstatus": 1,
    "Date": "2024-07-17",
    "Valid Till": "2024-07-26",
    "Party": "Adhwaya Energy Solutions",
    "Title": "Adhwaya Energy Solutions",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 510518,
    "Grand Total (Company Currency)": 510518,
    "Company": "Greentek India Limited",
    "Customer Name": "Adhwaya Energy Solutions"
  },
  {
    "Sr": 6,
    "ID": "QTN-00960-1",
    "Docstatus": 1,
    "Date": "2024-07-17",
    "Valid Till": "2024-07-27",
    "Party": "LEAD-206211411",
    "Title": "Ramakrishna Reddy",
    "Quotation To": "Lead",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 694400,
    "Grand Total (Company Currency)": 694400,
    "Company": "Greentek India Limited",
    "Customer Name": "vensa infrastructure limited"
  },
  {
    "Sr": 7,
    "ID": "QTN-00959",
    "Docstatus": 1,
    "Date": "2024-07-17",
    "Valid Till": "2024-07-28",
    "Party": "V-Pro Solar Systems",
    "Title": "V-Pro Solar Systems",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 137894,
    "Grand Total (Company Currency)": 137894,
    "Company": "Greentek India Limited",
    "Customer Name": "V-Pro Solar Systems"
  },
  {
    "Sr": 8,
    "ID": "QTN-00958-1",
    "Docstatus": 1,
    "Date": "2024-07-16",
    "Valid Till": "2024-07-29",
    "Party": "Adhwaya Energy Solutions",
    "Title": "Adhwaya Energy Solutions",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 630509.9,
    "Grand Total (Company Currency)": 630509.9,
    "Company": "Greentek India Limited",
    "Customer Name": "Adhwaya Energy Solutions"
  },
  {
    "Sr": 9,
    "ID": "QTN-00957-1",
    "Docstatus": 1,
    "Date": "2024-07-16",
    "Valid Till": "2024-07-30",
    "Party": "Adhwaya Energy Solutions",
    "Title": "Adhwaya Energy Solutions",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 504529.59,
    "Grand Total (Company Currency)": 504529.59,
    "Company": "Greentek India Limited",
    "Customer Name": "Adhwaya Energy Solutions"
  },
  {
    "Sr": 10,
    "ID": "QTN-00956",
    "Docstatus": 1,
    "Date": "2024-07-16",
    "Valid Till": "2024-07-31",
    "Party": "Adhwaya Energy Solutions",
    "Title": "Adhwaya Energy Solutions",
    "Quotation To": "Customer",
    "Order Type": "Sales",
    "Status": "Expired",
    "Currency": "INR",
    "Grand Total": 219129.27,
    "Grand Total (Company Currency)": 219129.27,
    "Company": "Greentek India Limited",
    "Customer Name": "Adhwaya Energy Solutions"
  }
]
