import re
import frappe

def autoname(doc, method=None):
    set_name(doc)

def set_name(doc):
    doc_list=["Purchase Order","Sales Order","Purchase Invoice","Sales Invoice","Journal Entry","Payment Entry","Stock Entry"]
    if doc.doctype in doc_list:
        year = frappe.defaults.get_global_default('fiscal_year')
        month = re.findall(r'\d+', frappe.utils.today())[1]
        doc_prefix = ""
        posting_dt = ""
        p_year= ""

        if doc.doctype == "Sales Invoice":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            if doc.is_return:
                doc_prefix="SRET"
            else:
                doc_prefix="SI"
        if doc.doctype == "Payment Entry":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            doc_prefix="PI"      
        if doc.doctype == "Sales Order":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            doc_prefix="SO"
        if doc.doctype == "Purchase Invoice":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            doc_prefix="PI"
        if doc.doctype == "Journal Entry":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            doc_prefix="JV"
        if doc.doctype == "Purchase Order":
            posting_dt = "transaction_date"
            p_year = str(doc.transaction_date).split("-")[0]
            doc_prefix="PO"
        if doc.doctype == "Stock Entry":
            posting_dt = "posting_date"
            p_year = str(doc.posting_date).split("-")[0]
            if doc.stock_entry_type=='Material Transfer to Customer':
                doc_prefix="PJDC"
            if doc.stock_entry_type=='Material Issue':
                doc_prefix="MI"  
            if doc.stock_entry_type=='Manufacture':
                doc_prefix="STE"
            if doc.stock_entry_type=='Material Receipt':
                doc_prefix="MR"

        sql = """SELECT COUNT(name) AS seq FROM `tab{0}` WHERE YEAR({1}) = %s AND company = %s;""".format(doc.doctype, posting_dt)
        ct = frappe.db.sql(sql, (p_year, doc.company), as_dict=True)
        sequence = ct[0].seq + 1 if ct and ct[0].seq is not None else 1
        
        sequence_formatted = '{:05d}'.format(sequence)
        doc.name = "{0}/{1}/{2}/{3}".format(doc_prefix, month, p_year[-2:], sequence_formatted)
