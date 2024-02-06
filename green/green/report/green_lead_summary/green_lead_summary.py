# Copyright (c) 2024, Oymom and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	conditions= get_conditions(filters)
	sql="""select * from (
					SELECT
						l.owner,
						l.company,
						l.lead_owner,
						l.name AS lead,
						lead_name,
						l.source,
						DATE(l.creation) date,
						
						d.description AS activity,
						d.date AS follow_up_date,
						n.note comment,
						l.territory,l.state,l.pincode,l.city,l.status,l.custom_sales_person
					FROM
						`tabLead` l
					LEFT JOIN
						(
							SELECT
								reference_name,
								MAX(creation) AS max_creation
							FROM
								`tabToDo`
							GROUP BY
								reference_name
						) latest_todo ON l.name = latest_todo.reference_name
					LEFT JOIN
						`tabToDo` d ON l.name = d.reference_name AND latest_todo.max_creation = d.creation
					LEFT JOIN
						(
							SELECT
								parent,
								note,
								creation
							FROM
								`tabCRM Note`
							WHERE
								parent = "LEAD-206202127"
							ORDER BY
								creation DESC
							LIMIT 1
						) n ON l.name = n.parent
					)x {0}
""".format(conditions)
	frappe.errprint(sql)
	columns = get_columns()
	data=frappe.db.sql(sql,as_dict=1)
	result=[]
	for row in data:
		entry = {
			'owner': row.owner,
			'company': row.company,
			'lead_owner': row.lead_owner,
			'lead': row.lead,
			'lead_name': row.lead_name,
			'source': row.source,
			'date': row.date,
			'activity':remove_html_tags(row.activity) if row.activity else "",
			'follow_up_date': row.follow_up_date,
			'comment': row.comment,
			'territory': row.territory,
			'state': row.state,
			'pincode': row.pincode,
			'city': row.city,
			'status': row.status,
			'custom_sales_person': row.custom_sales_person
		}
		result.append(entry)
	if result:
		return columns, result
	else:
		columns, data = [], []



def get_conditions(filters):

	condition=" where  company='{0}' ".format(filters.get("company"))
	if filters.get("from_date") and filters.get("to_date"):
		condition=condition+"and  date BETWEEN '{0}' AND '{1}' ".format(filters.get("from_date") ,filters.get("to_date"))

	if filters.get("status"):
		condition=condition+' and status="{0}" '.format(filters.get("status"))
	if filters.get("territory"):
		condition=condition+' and territory="{0}" '.format(filters.get("territory"))
	return condition

import re

def remove_html_tags(text=None):
		clean = re.compile('<.*?>')
		return re.sub(clean, '', text)





def get_columns():
	columns=[]

	columns+= [
		{
			'label': _('Owner'),
			'fieldname': "owner",
			'fieldtype': 'Data',
			'width': 140
		},
		{
	 		'fieldname': 'lead_owner',
			'label':('Lead Owner'),
			'fieldtype': 'Link',
			'options': 'User',
			'width': 200
		},
		{
	 		'fieldname': 'custom_sales_person',
			'label':('Sales Person'),
			'fieldtype': 'Link',
			'options': 'Sales Person',
			'width': 200
		},
		{
	 		'fieldname': 'lead',
			'label':('Lead'),
			'fieldtype': 'Link',
			'options': 'Lead',
			'width': 200
		},
		{
	 		'fieldname': 'lead_name',
			'label':('Lead Name'),
			'fieldtype': 'Data',
			'width': 200
		},
		{
			'label': _('State'),
			'fieldname': "state",
			'fieldtype': 'Data',
			'width': 140
		},
		{
			'label': _('City'),
			'fieldname': "city",
			'fieldtype': 'Data',
			'width': 140
		},
		{
			'label': _('Postal code'),
			'fieldname': "pincode",
			'fieldtype': 'Data',
			'width': 140
		},
		{
	 		'fieldname': 'territory',
			'label':('Territory'),
			'fieldtype': 'Link',
			'options': 'Territory',
			'width': 140
		},
			{
			'label': _('Source'),
			'fieldname': "source",
			'fieldtype': 'Data',
			'width': 140
		},
		{
			'label': _('Status'),
			'fieldname': "status",
			'fieldtype': 'Data',
			'width': 140
		},
			{
			'label': _('Activity'),
			'fieldname': "activity",
			'fieldtype': 'Text Editor',
			'width': 320
		},
		
		{
			'fieldname': "follow_up_date",
			'label': ('Follow Up Date'),
			'fieldtype': 'Date',
			'width': 140
		},
		
		{
			'label': _('Comment'),
			'fieldname': "comment",
			'fieldtype': 'Data',
			'width': 220
		},
	  
	]
	return columns

	
