import re
import frappe


def validate(self, method=None):
    doc_list=["Purchase Order","Sales Order","Purchase Invoice","Sales Invoice","Journal Entry","Payment Entry","Stock Entry"]
    if self.doctype in doc_list:
        if self.is_new():
            try:
                sql = """SELECT MAX(custom_sequence) sequence
                        FROM `tabSales Invoice`
                        WHERE company=%s AND custom_sequence IS NOT NULL and  YEAR(creation) =%s
                        ORDER BY creation DESC
                        LIMIT 1""".format(self.doctype)
                last_count = frappe.db.sql(sql, (self.company,get_year(self.posting_date)), as_dict=False)
                last_count = last_count[0][0] if last_count else None
                if last_count is not None:
                    self.custom_sequence = last_count + 1
                else:
                    self.custom_sequence = 1	
            except Exception as e:
                frappe.log_error(f"Error setting  custom_sequence: {str(e)}")


def get_year(posting_date):
    import datetime
    date_string = str(posting_date)
    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    year = date_object.year
    return year



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

        sql = """SELECT MAX(custom_sequence)
                            FROM `tab{0}`
                            WHERE company=%s AND custom_sequence IS NOT NULL""".format(doc.doctype)
        max_icv = frappe.db.sql(sql, (doc.company,), as_dict=False)[0][0]
        if max_icv is not None:
            sequence = max_icv + 1
        else:
            sequence = 1
        last_number='{:05d}'.format(sequence)
    
        if last_number == 0:
            last_number = '{:05d}'.format(sequence)
        sequence_formatted = '{:05d}'.format(sequence)
        doc.name = "{0}/{1}/{2}/{3}".format(doc_prefix, month, p_year[-2:], sequence_formatted)
