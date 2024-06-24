
import frappe



# Create Project Automatically
def create_project_automatically( doc, method= None):
    project = frappe.new_doc("Project")
    project.project_name = doc.name
    project.custom_company = doc.company
    project.sales_order = doc.name
    project.customer = doc.customer
    project.estimated_costing = doc.grand_total
    project.insert()
