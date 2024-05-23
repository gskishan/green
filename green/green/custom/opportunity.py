import frappe
from frappe import _
from erpnext.crm.doctype.opportunity.opportunity import Opportunity
from erpnext.crm.doctype.opportunity.opportunity import *
from erpnext.crm.utils import (
	copy_comments,
	link_communications,
	link_open_tasks,
)
from erpnext.crm.utils import get_open_events

class CustomOpportunity(Opportunity):
	def after_insert(self):
		if self.opportunity_from == "Lead":
			frappe.get_doc("Lead", self.party_name).set_status(update=True)

			link_open_tasks(self.opportunity_from, self.party_name, self)
			custom_link_open_events(self.opportunity_from, self.party_name, self)
			if frappe.db.get_single_value("CRM Settings", "carry_forward_communication_and_comments"):
				copy_comments(self.opportunity_from, self.party_name, self)
				link_communications(self.opportunity_from, self.party_name, self)

def custom_link_open_events(ref_doctype, ref_docname, doc):
	events = get_open_events(ref_doctype, ref_docname)
	for event in events:
		event_doc = frappe.get_doc("Event", event.name)
		event_doc.add_participant(doc.doctype, doc.name)
		event_doc.save()

def get_permission_query_conditions(user=None):
    if not user:
        user = frappe.session.user
    return f"""
    (
        `tabEvent`.`event_type` IN ('Public', 'Private')
        OR `tabEvent`.`owner`={frappe.db.escape(user)}
    )
    """

def has_permission(doc, user):
	typelist=["Public","Private"]
	if doc.event_type == "Public" or doc.owner == user:
		return True

	return False



