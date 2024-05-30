

import frappe

@frappe.whitelist()
def create_quotation(doctype, name):
    contact_person = ''

    try:
        # Create Prospect & Then After That Create Quotation
        deal = frappe.get_doc(doctype,name)
        # Get Primary Contact From List of Contacts
        for each in deal.contacts:
            if each.is_primary:
                contact_person = each.contact
        # Set Prospect Name 
        prospect_name = deal.lead_name
        if deal.organization:
            prospect_name = deal.organization 

        # Get Company
        address = frappe.db.get_list("Address",filters = {
                "address_title": deal.custom_company,
                "is_your_company_address": 1,
                "is_primary_address": 1,
                "disabled": 0
        })
        if address[0].name:
            prospect = frappe.db.get_list("Prospect",filters={
                "company_name": prospect_name
            })

            if prospect:
                prospect = prospect[0]

            if not prospect:
                # Crerate Prospect
                prospect = frappe.new_doc("Prospect")
                prospect.company_name = prospect_name
                prospect.deal_owner = deal.deal_owner
                prospect.website = deal.website
                # prospect.custom_deal = deal.name
                prospect.insert()
            
            # Create Quotation
            quotation = frappe.new_doc("Quotation")
            quotation.quotation_to = "Prospect"
            quotation.party_name = prospect.name        
            quotation.customer_name = prospect.name
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
            quotation.custom_deal = deal.name
            quotation.grand_total = 1 
            quotation.base_grand_total = 1 
            quotation.base_rounded_total = 1 
            quotation.rounded_total = 1
            quotation.company_address = address[0].name

            quotation.save()

            # Return Succes Message
            return {"success" : True,
            'Mesage': "Created Succesfully"}
        
        return {"success" : False,
        'Mesage': "No Company Address Found"}

    except Exception as err:
        return {"success": False, "err":err}

