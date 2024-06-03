import re
import frappe

def autoname(doc, method=None):
    set_name(doc)

def set_name(doc):
    year = frappe.defaults.get_global_default('fiscal_year')
    month = re.findall(r'\d+', frappe.utils.today())[1]
    doc_prefix = ""
    posting_dt = ""
    p_year= ""

    if doc.doctype == "Sales Invoice":
        posting_dt = "posting_date"
        p_year = str(doc.posting_date).split("-")[0]
        doc_prefix="SI"

    sql = """SELECT COUNT(name) AS seq FROM `tab{0}` WHERE YEAR({1}) = %s AND company = %s;""".format(doc.doctype, posting_dt)
    ct = frappe.db.sql(sql, (p_year, doc.company), as_dict=True)
    sequence = ct[0].seq + 1 if ct and ct[0].seq is not None else 1
    
    sequence_formatted = '{:05d}'.format(sequence)
    doc.name = "{0}/{1}/{2}/{3}".format(doc_prefix, month, year, sequence_formatted)
    frappe.errprint(doc.name )
