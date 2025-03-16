import frappe
from collections import defaultdict
from frappe.utils import markdown

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"fieldname": "created_by", "label": "Created By", "fieldtype": "Data", "width": 200},
        {"fieldname": "doctype", "label": "Doctype", "fieldtype": "Data", "width": 150},
        {"fieldname": "reference_name", "label": "Customer / Lead", "fieldtype": "Dynamic Link", "options": "doctype", "width": 200},
        {"fieldname": "full_name", "label": "Full Name", "fieldtype": "Data", "width": 200},
    ]    

    for i in range(1, 9):
        columns.append({
            "fieldname": f"day{i}",
            "label": f"Day {i}",
            "fieldtype": "Data",
            "width": 250
        })

    extra_columns = [
        {"fieldname": "oppo_count", "label": "Opp Qty", "fieldtype": "Int", "width": 120},
        {"fieldname": "oppo_amt", "label": "Oppo Amt", "fieldtype": "Currency", "width": 120},
        {"fieldname": "qtn_count", "label": "Qtn Qty", "fieldtype": "Int", "width": 120},
        {"fieldname": "qtn_amt", "label": "Qtn Amt", "fieldtype": "Currency", "width": 120},
        {"fieldname": "so_count", "label": "SO Qty", "fieldtype": "Int", "width": 120},
        {"fieldname": "so_amt", "label": "SO Amt", "fieldtype": "Currency", "width": 120},
        {"fieldname": "si_count", "label": "SI Qty", "fieldtype": "Int", "width": 120},
        {"fieldname": "si_amt", "label": "SI Amt", "fieldtype": "Currency", "width": 120},
    ]

    columns.extend(extra_columns)
    return columns

def get_data(filters):
    from_date = filters.get("from_date", frappe.utils.today())
    to_date = filters.get("to_date", frappe.utils.today())
    reference_type = filters.get("reference_type")
    reference_name = filters.get("reference_name")

    filters_dict = {"creation": ["between", [from_date, to_date]]}
    if reference_name:
        filters_dict["name"] = reference_name

    entities = []
    if not reference_type or reference_type == "Customer":
        entities += frappe.get_all("Customer", fields=["name", "owner", "customer_name"], filters=filters_dict)
    if not reference_type or reference_type == "Lead":
        entities += frappe.get_all("Lead", fields=["name", "owner", "lead_name"], filters=filters_dict)

    result = {
        entity["name"]: {
            "created_by": frappe.get_value("User", entity["owner"], "full_name") or entity["owner"],
            "reference_name": entity["name"],
            "doctype": "Customer" if "customer_name" in entity else "Lead",
            "full_name": entity.get("customer_name") or entity.get("lead_name", ""),
            "oppo_count": 0, "oppo_amt": 0, "qtn_count": 0, "qtn_amt": 0,
            "so_count": 0, "so_amt": 0, "si_count": 0, "si_amt": 0,
        }
        for entity in entities
    }

    process_todos(result, from_date, to_date)
    update_sales_data(result)
    
    return list(result.values())

def process_todos(result, from_date, to_date):
    todos = frappe.get_all(
        "ToDo", 
        fields=["reference_name", "description", "date"], 
        filters={"status": "Open", "date": ["between", [from_date, to_date]]}
    )
    
    todo_data = defaultdict(lambda: defaultdict(list))
    for todo in todos:
        if todo["reference_name"] in result:
            todo_data[todo["reference_name"]][todo["date"]].append(todo["description"] or "No Description")
    
    for ref_name, dates in todo_data.items():
        sorted_dates = sorted(dates.keys())
        for i, date in enumerate(sorted_dates[:8]):
            result[ref_name][f"day{i+1}"] = markdown("<br>".join(dates[date]))

def update_sales_data(result):
    ref_names = list(result.keys())
    
    # Fetch sales data in bulk
    sales_data = {
        "Opportunity": frappe.get_all("Opportunity", filters={"party_name": ["in", ref_names], "docstatus": 0}, fields=["party_name", "opportunity_amount"]),
        "Quotation": frappe.get_all("Quotation", filters={"party_name": ["in", ref_names], "docstatus": 1}, fields=["party_name", "total"]),
        "Sales Order": frappe.get_all("Sales Order", filters={"customer": ["in", ref_names], "docstatus": 1}, fields=["customer", "total"]),
        "Sales Invoice": frappe.get_all("Sales Invoice", filters={"customer": ["in", ref_names], "docstatus": 1}, fields=["customer", "total"])
    }

    # Process fetched sales data
    for doc_type, records in sales_data.items():
        for record in records:
            ref_name = record.get("party_name") or record.get("customer")
            if ref_name in result:
                if doc_type == "Opportunity":
                    result[ref_name]["oppo_count"] += 1
                    result[ref_name]["oppo_amt"] += record.get("opportunity_amount", 0)
                elif doc_type == "Quotation":
                    result[ref_name]["qtn_count"] += 1
                    result[ref_name]["qtn_amt"] += record.get("total", 0)
                elif doc_type == "Sales Order":
                    result[ref_name]["so_count"] += 1
                    result[ref_name]["so_amt"] += record.get("total", 0)
                elif doc_type == "Sales Invoice":
                    result[ref_name]["si_count"] += 1
                    result[ref_name]["si_amt"] += record.get("total", 0)

    # Handle Leads' associated Customers
    lead_to_customer = {
        lead: frappe.get_value("Customer", {"lead_name": lead}, "name") 
        for lead in result if result[lead]["doctype"] == "Lead"
    }

    for lead, customer in lead_to_customer.items():
        if customer:
            # Fetch sales data for the linked customer
            so = frappe.get_all("Sales Order", filters={"customer": customer, "docstatus": 1}, fields=["total"])
            si = frappe.get_all("Sales Invoice", filters={"customer": customer, "docstatus": 1}, fields=["total"])

            # Update the lead's result with the customer's sales data
            result[lead]["so_count"] = len(so)
            result[lead]["so_amt"] = sum(s["total"] for s in so if s["total"])
            result[lead]["si_count"] = len(si)
            result[lead]["si_amt"] = sum(s["total"] for s in si if s["total"])