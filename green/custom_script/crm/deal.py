

import frappe

@frappe.whitelist()
def create_quotation(doctype, name):
    contact_person = ''

    try:
        deal = frappe.get_doc(doctype,name)
        for each in deal.contacts:
            if each.is_primary:
                contact_person = each.contact

        quotation = frappe.new_doc("CRM Quotation")
        quotation.organization = deal.organization
        quotation.customer_name = deal.organization
        quotation.website = deal.website
        quotation.territory = deal.territory
        quotation.annual_revenue = deal.annual_revenue
        quotation.close_date = deal.close_date
        quotation.probability = deal.probability
        quotation.lead = deal.lead
        quotation.lead_source = deal.source
        quotation.lead_name = deal.lead_name
        quotation.deal_owner = deal.deal_owner
        quotation.mobile_no = deal.mobile_no
        quotation.email = deal.email
        quotation.deal = deal.name
        quotation.contact_person = contact_person
        quotation.insert()
        # Update Deal Status
        deal.status = "Quotation Created"
        deal.save()
        # Return Succes Message
        return {"success" : True,
        'Mesage': "Created Succesfully"}

    except Exception as err:
        return {"success": False, "err":err}

