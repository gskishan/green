# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from calendar import monthrange
from itertools import groupby
from typing import Dict, List, Optional, Tuple

import frappe
from frappe import _
from frappe.query_builder.functions import Count, Extract, Sum
from frappe.utils import cint, cstr, getdate
from frappe.utils import formatdate

Filters = frappe._dict

status_map = {
	"Present": "P",
	"Absent": "A",
	"Half Day": "HD",
	"Work From Home": "WFH",
	"On Leave": "L",
	"Holiday": "H",
	"Weekly Off": "WO",
}

day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def execute(filters: Optional[Filters] = None) -> Tuple:
	filters = frappe._dict(filters or {})


	# if not (filters.month and filters.year):
	# 	frappe.throw(_("Please select month and year."))
	if get_year(filters.from_date)!=get_year(filters.to_date):
		frappe.throw("Please Select one year range ")

	attendance_map = get_attendance_map(filters)
	if not attendance_map:
		frappe.msgprint(_("No attendance records found."), alert=True, indicator="orange")
		return [], [], None, None

	columns = get_columns(filters)
	data = get_data(filters, attendance_map)

	if not data:
		frappe.msgprint(
			_("No attendance records found for this criteria."), alert=True, indicator="orange"
		)
		return columns, [], None, None

	message = get_message() if not filters.summarized_view else ""
	chart = get_chart_data(attendance_map, filters)
	


	return columns, data,message,chart


def get_message() -> str:
	message = ""
	colors = ["green", "red", "orange", "green", "#318AD8", "", ""]

	count = 0
	for status, abbr in status_map.items():
		message += f"""
			<span style='border-left: 2px solid {colors[count]}; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
				{status} - {abbr}
			</span>
		"""
		count += 1

	return message


def get_columns(filters: Filters) -> List[Dict]:
	columns = []

	if filters.group_by:
		columns.append(
			{
				"label": _(filters.group_by),
				"fieldname": frappe.scrub(filters.group_by),
				"fieldtype": "Link",
				"options": "Branch",
				"width": 120,
			}
		)

	columns.extend(
		[
			{
				"label": _("Employee"),
				"fieldname": "employee",
				"fieldtype": "Link",
				"options": "Employee",
				"width": 135,
			},
			{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
		]
	)

	if filters.summarized_view:
		columns.extend(
			[
				{
					"label": _("Total Present"),
					"fieldname": "total_present",
					"fieldtype": "Float",
					"width": 110,
				},
				{"label": _("Total Leaves"), "fieldname": "total_leaves", "fieldtype": "Float", "width": 110},
				{"label": _("Total Absent"), "fieldname": "total_absent", "fieldtype": "Float", "width": 110},
				{
					"label": _("Total Holidays"),
					"fieldname": "total_holidays",
					"fieldtype": "Float",
					"width": 120,
				},
				{
					"label": _("Unmarked Days"),
					"fieldname": "unmarked_days",
					"fieldtype": "Float",
					"width": 130,
				},
			]
		)
		columns.extend(get_columns_for_leave_types())
		columns.extend(
			[
				{
					"label": _("Total Late Entries"),
					"fieldname": "total_late_entries",
					"fieldtype": "Float",
					"width": 140,
				},
				{
					"label": _("Total Early Exits"),
					"fieldname": "total_early_exits",
					"fieldtype": "Float",
					"width": 140,
				},
			]
		)
	else:
		columns.append({"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 120})
		for d in get_columns_for_days(filters):
			columns.append({"label": d.get("label"), "fieldname": d.get("fieldname"), "fieldtype": "Data", "width": 120})


	return columns


def get_columns_for_leave_types() -> List[Dict]:
	leave_types = frappe.db.get_all("Leave Type", pluck="name")
	types = []
	for entry in leave_types:
		types.append(
			{"label": entry, "fieldname": frappe.scrub(entry), "fieldtype": "Float", "width": 120}
		)

	return types


from datetime import datetime, timedelta
import calendar

def get_columns_for_days(filters):
	columns = []
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')

	# Convert from_date and to_date to datetime objects
	start_date = datetime.strptime(from_date, '%Y-%m-%d')
	end_date = datetime.strptime(to_date, '%Y-%m-%d')

	# Iterate over each day in the range
	current_date = start_date
	while current_date <= end_date:
		day = str(current_date.day).zfill(2)
		month_abbr = current_date.strftime('%b').lower()  # Get abbreviated month name in lowercase
		year_abbr = current_date.strftime('%y')  # Get abbreviated year
		weekday_abbr = calendar.day_abbr[current_date.weekday()].lower()  # Get abbreviated weekday name in lowercase

		# Format column name as "apr_24_wed"
		column_name = f"{month_abbr}_{day}_{weekday_abbr}"
		
		# Append dictionary with column name and field type to columns list
		columns.append({
			"label": f"{month_abbr.capitalize()} {day} ({weekday_abbr.capitalize()})",  # Display label with capitalized month and weekday
			"fieldname": column_name,  # Field name in lowercase
			"fieldtype": "Data"  # Field type as Data
		})

		# Move to the next day
		current_date += timedelta(days=1)

	return columns


from datetime import datetime
from calendar import monthrange

def get_total_days_in_month(filters: Filters) -> int:
	# Extract from_date and to_date from filters
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	
	if not from_date or not to_date:
		raise ValueError("Both from_date and to_date must be provided.")

	# Parse from_date and to_date
	try:
		from_date = datetime.strptime(from_date, "%Y-%m-%d")
		to_date = datetime.strptime(to_date, "%Y-%m-%d")
	except ValueError as e:
		raise ValueError(f"Date format should be YYYY-MM-DD. Error: {e}")

	if from_date > to_date:
		raise ValueError("from_date cannot be later than to_date.")

	# Initialize total days counter
	total_days = 0

	# Iterate over each month in the range
	current_date = from_date
	while current_date <= to_date:
		# Get the last day of the current month
		_, last_day = monthrange(current_date.year, current_date.month)
		# Calculate the number of days in the current month to consider
		days_in_month = min(last_day, (to_date - current_date).days + 1)
		total_days += days_in_month

		# Move to the next month
		if current_date.month == 12:
			current_date = datetime(current_date.year + 1, 1, 1)
		else:
			current_date = datetime(current_date.year, current_date.month + 1, 1)

	return total_days




def get_data(filters: Filters, attendance_map: Dict) -> List[Dict]:
	employee_details, group_by_param_values = get_employee_related_details(filters)
	holiday_map = get_holiday_map(filters)
	data = []

	if filters.group_by:
		group_by_column = frappe.scrub(filters.group_by)

		for value in group_by_param_values:
			if not value:
				continue

			records = get_rows(employee_details[value], filters, holiday_map, attendance_map)

			if records:
				data.append({group_by_column: frappe.bold(value)})
				data.extend(records)
	else:
		data = get_rows(employee_details, filters, holiday_map, attendance_map)

	return data


def get_attendance_map(filters: Filters) -> Dict:
	"""Returns a dictionary of employee wise attendance map as per shifts for all the days of the month like
	{
		'employee1': {
				'Morning Shift': {1: 'Present', 2: 'Absent', ...}
				'Evening Shift': {1: 'Absent', 2: 'Present', ...}
		},
		'employee2': {
				'Afternoon Shift': {1: 'Present', 2: 'Absent', ...}
				'Night Shift': {1: 'Absent', 2: 'Absent', ...}
		},
		'employee3': {
				None: {1: 'On Leave'}
		}
	}
	"""
	attendance_list = get_attendance_records(filters)
	attendance_map = {}
	leave_map = {}

	for d in attendance_list:
		if d.status == "On Leave":
			leave_map.setdefault(d.employee, []).append(d.attendance_date)
			continue

		if d.shift is None:
			d.shift = ""

		attendance_map.setdefault(d.employee, {}).setdefault(d.shift, {})
		attendance_map[d.employee][d.shift][d.attendance_date] = d.status

	# leave is applicable for the entire day so all shifts should show the leave entry
	for employee, leave_days in leave_map.items():
		# no attendance records exist except leaves
		if employee not in attendance_map:
			attendance_map.setdefault(employee, {}).setdefault(None, {})

		for day in leave_days:
			for shift in attendance_map[employee].keys():
				attendance_map[employee][shift][day] = "On Leave"
	return attendance_map


import frappe
from frappe import _
from datetime import datetime

def get_attendance_records(filters: Filters) -> List[Dict]:
	Attendance = frappe.qb.DocType("Attendance")
	query = (
		frappe.qb.from_(Attendance)
		.select(
			Attendance.employee,
			Attendance.attendance_date,
			Attendance.status,
			Attendance.shift,
		)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.company == filters.company)
			& (Attendance.attendance_date.between(filters.from_date, filters.to_date))
		)
	)

	if filters.employee:
		query = query.where(Attendance.employee == filters.employee)
	query = query.orderby(Attendance.employee, Attendance.attendance_date)

	records = query.run(as_dict=1)

	# Format date fields
	formatted_records = []
	for record in records:
			date_obj = record['attendance_date']
			date_obj.strftime('%b_%d_%a').lower()  
			formatted_date = date_obj.strftime('%b_%d_%a').lower()  
			record['attendance_date'] = formatted_date
			record[formatted_date] = record['status']
			formatted_records.append(record)

	return formatted_records




def get_employee_related_details(filters: Filters) -> Tuple[Dict, List]:
	"""Returns
	1. nested dict for employee details
	2. list of values for the group by filter
	"""
	Employee = frappe.qb.DocType("Employee")
	query = (
		frappe.qb.from_(Employee)
		.select(
			Employee.name,
			Employee.employee_name,
			Employee.designation,
			Employee.grade,
			Employee.department,
			Employee.branch,
			Employee.company,
			Employee.holiday_list,
		)
		.where(Employee.company == filters.company)
	)

	if filters.employee:
		query = query.where(Employee.name == filters.employee)

	group_by = filters.group_by
	if group_by:
		group_by = group_by.lower()
		query = query.orderby(group_by)

	employee_details = query.run(as_dict=True)

	group_by_param_values = []
	emp_map = {}

	if group_by:
		for parameter, employees in groupby(employee_details, key=lambda d: d[group_by]):
			group_by_param_values.append(parameter)
			emp_map.setdefault(parameter, frappe._dict())

			for emp in employees:
				emp_map[parameter][emp.name] = emp
	else:
		for emp in employee_details:
			emp_map[emp.name] = emp

	return emp_map, group_by_param_values


def get_holiday_map(filters: Filters) -> Dict[str, List[Dict]]:
    """
    Returns a dict of holidays falling in the filter month and year
    with list name as key and list of holidays as values like
    {
        'Holiday List 1': [
            {'day_of_month': '0' , 'weekly_off': 1, 'holiday_date': 'YYYY-MM-DD'},
            {'day_of_month': '1', 'weekly_off': 0, 'holiday_date': 'YYYY-MM-DD'}
        ],
        'Holiday List 2': [
            {'day_of_month': '0' , 'weekly_off': 1, 'holiday_date': 'YYYY-MM-DD'},
            {'day_of_month': '1', 'weekly_off': 0, 'holiday_date': 'YYYY-MM-DD'}
        ]
    }
    """
    # add default holiday list too
    holiday_lists = frappe.db.get_all("Holiday List", pluck="name")
    default_holiday_list = frappe.get_cached_value("Company", filters.company, "default_holiday_list")
    holiday_lists.append(default_holiday_list)

    holiday_map = frappe._dict()
    Holiday = frappe.qb.DocType("Holiday")

    for d in holiday_lists:
        if not d:
            continue

        holidays = (
            frappe.qb.from_(Holiday)
            .select(
                Extract("day", Holiday.holiday_date).as_("day_of_month"), 
                Holiday.weekly_off, 
                Holiday.holiday_date  # Added holiday_date column
            )
            .where(
                (Holiday.parent == d)
                & (Holiday.holiday_date.between(filters.from_date, filters.to_date))
            )
        ).run(as_dict=True)

        holiday_map.setdefault(d, holidays)

    return holiday_map


def get_rows(
	employee_details: Dict, filters: Filters, holiday_map: Dict, attendance_map: Dict
) -> List[Dict]:
	records = []
	default_holiday_list = frappe.get_cached_value("Company", filters.company, "default_holiday_list")

	for employee, details in employee_details.items():
		emp_holiday_list = details.holiday_list or default_holiday_list
		holidays = holiday_map.get(emp_holiday_list)


		if filters.summarized_view:
			attendance = get_attendance_status_for_summarized_view(employee, filters, holidays)
			if not attendance:
				continue

			leave_summary = get_leave_summary(employee, filters)
			entry_exits_summary = get_entry_exits_summary(employee, filters)

			row = {"employee": employee, "employee_name": details.employee_name}
			set_defaults_for_summarized_view(filters, row)
			row.update(attendance)
			row.update(leave_summary)
			row.update(entry_exits_summary)

			records.append(row)
		else:
			employee_attendance = attendance_map.get(employee)
			if not employee_attendance:
				continue

			attendance_for_employee = get_attendance_status_for_detailed_view(
				employee, filters, employee_attendance, holidays
			)

			# set employee details in the first row
			attendance_for_employee[0].update(
				{"employee": employee, "employee_name": details.employee_name}
			)

			records.extend(attendance_for_employee)

	return records


def set_defaults_for_summarized_view(filters, row):
	for entry in get_columns(filters):
		if entry.get("fieldtype") == "Float":
			row[entry.get("fieldname")] = 0.0


def get_attendance_status_for_summarized_view(
	employee: str, filters: Filters, holidays: List
) -> Dict:
	"""Returns dict of attendance status for employee like
	{'total_present': 1.5, 'total_leaves': 0.5, 'total_absent': 13.5, 'total_holidays': 8, 'unmarked_days': 5}
	"""
	summary, attendance_days = get_attendance_summary_and_days(employee, filters)
	if not any(summary.values()):
		return {}
	

	total_days = get_date_range(filters)
	total_holidays = total_unmarked_days = 0
	
	for day in total_days:
		


		if day.day in attendance_days:
			continue
		

		status = get_holiday_status(day.day, holidays)
		if status in ["Weekly Off", "Holiday"]:
			total_holidays += 1
		elif not status:
			total_unmarked_days += 1

	return {
		"total_present": summary.total_present + summary.total_half_days,
		"total_leaves": summary.total_leaves + summary.total_half_days,
		"total_absent": summary.total_absent,
		"total_holidays": total_holidays,
		"unmarked_days": total_unmarked_days,
	}
def get_date_range(filters):
    sql="""select  date_list day from 
(select adddate('2022-01-01',t4.i*10000 + t3.i*1000 + t2.i*100 + t1.i*10 + t0.i) date_list from
 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t0,
 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t1,
 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t2,
 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t3,
 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t4) v
where date_list  BETWEEN '{0}' AND '{1}';  
""".format(filters.from_date, filters.to_date)
    return frappe.db.sql(sql,as_dict=1)

def get_attendance_summary_and_days(employee: str, filters: Filters) -> Tuple[Dict, List]:
	Attendance = frappe.qb.DocType("Attendance")

	present_case = (
		frappe.qb.terms.Case()
		.when(((Attendance.status == "Present") | (Attendance.status == "Work From Home")), 1)
		.else_(0)
	)
	sum_present = Sum(present_case).as_("total_present")

	absent_case = frappe.qb.terms.Case().when(Attendance.status == "Absent", 1).else_(0)
	sum_absent = Sum(absent_case).as_("total_absent")

	leave_case = frappe.qb.terms.Case().when(Attendance.status == "On Leave", 1).else_(0)
	sum_leave = Sum(leave_case).as_("total_leaves")

	half_day_case = frappe.qb.terms.Case().when(Attendance.status == "Half Day", 0.5).else_(0)
	sum_half_day = Sum(half_day_case).as_("total_half_days")

	summary = (
		frappe.qb.from_(Attendance)
		.select(
			sum_present,
			sum_absent,
			sum_leave,
			sum_half_day,
		)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.employee == employee)
			& (Attendance.company == filters.company)
			  & (Attendance.attendance_date.between(filters.from_date, filters.to_date))
		)
	).run(as_dict=True)

	days = (
    frappe.qb.from_(Attendance)
    .select(Attendance.attendance_date)
    .distinct()
    .where(
        (Attendance.docstatus == 1)
        & (Attendance.employee == employee)
        & (Attendance.company == filters.company)
        & (Attendance.attendance_date.between(filters.from_date, filters.to_date))
    )
	).run(pluck=True)

	
	days = [formatdate(day, "yyyy-MM-dd") for day in days]
	return summary[0], days


def get_attendance_status_for_detailed_view(
	employee: str, filters: Filters, employee_attendance: Dict, holidays: List
) -> List[Dict]:
	"""Returns list of shift-wise attendance status for employee
	[
			{'shift': 'Morning Shift', jun_01_sat: 'A', jun_02_sat: 'P', jun_03_sat: 'A'....},
			{'shift': 'Evening Shift', jun_01_sat: 'P', jun_02_sat: 'A', jun_03_sat: 'P'....}
	]
	"""
	total_days = get_total_days_in_month(filters)
	attendance_values = []
	a=([d.get("fieldname") for d in get_columns_for_days(filters)])
	key = next(iter(employee_attendance))

	for date in a:
		if date not in employee_attendance[key] and date:
			employee_attendance[key][date] = None

	year=get_year(filters.to_date)
	for shift, status_dict in employee_attendance.items():
		row = {"shift": shift}
		for key, status in status_dict.items():
			status = status_dict.get(key)
			if status is None and holidays:
				day=convert_to_date_format(key, year)
				status = get_holiday_status(day, holidays)

			# Map the status to its abbreviation
			abbr = status_map.get(status, "")
			row[key] = abbr

		attendance_values.append(row)


	return attendance_values



def get_holiday_status(day: int, holidays: List) -> str:
	status = None
	if holidays:
		for holiday in holidays:
			if day == formatdate(holiday.get("holiday_date"), "yyyy-MM-dd"):
				if holiday.get("weekly_off"):
					status = "Weekly Off"
				else:
					status = "Holiday"
				break
	return status


def get_leave_summary(employee: str, filters: Filters) -> Dict[str, float]:
	"""Returns a dict of leave type and corresponding leaves taken by employee like:
	{'leave_without_pay': 1.0, 'sick_leave': 2.0}
	"""
	Attendance = frappe.qb.DocType("Attendance")
	day_case = frappe.qb.terms.Case().when(Attendance.status == "Half Day", 0.5).else_(1)
	sum_leave_days = Sum(day_case).as_("leave_days")

	leave_details = (
		frappe.qb.from_(Attendance)
		.select(Attendance.leave_type, sum_leave_days)
		.where(
			(Attendance.employee == employee)
			& (Attendance.docstatus == 1)
			& (Attendance.company == filters.company)
			& ((Attendance.leave_type.isnotnull()) | (Attendance.leave_type != ""))
		  & (Attendance.attendance_date.between(filters.from_date, filters.to_date))
		)
		.groupby(Attendance.leave_type)
	).run(as_dict=True)

	leaves = {}
	for d in leave_details:
		leave_type = frappe.scrub(d.leave_type)
		leaves[leave_type] = d.leave_days

	return leaves


def get_entry_exits_summary(employee: str, filters: Filters) -> Dict[str, float]:
	"""Returns total late entries and total early exits for employee like:
	{'total_late_entries': 5, 'total_early_exits': 2}
	"""
	Attendance = frappe.qb.DocType("Attendance")

	late_entry_case = frappe.qb.terms.Case().when(Attendance.late_entry == "1", "1")
	count_late_entries = Count(late_entry_case).as_("total_late_entries")

	early_exit_case = frappe.qb.terms.Case().when(Attendance.early_exit == "1", "1")
	count_early_exits = Count(early_exit_case).as_("total_early_exits")

	entry_exits = (
		frappe.qb.from_(Attendance)
		.select(count_late_entries, count_early_exits)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.employee == employee)
			& (Attendance.company == filters.company)
		  & (Attendance.attendance_date.between(filters.from_date, filters.to_date))
		)
	).run(as_dict=True)

	return entry_exits[0]


@frappe.whitelist()
def get_attendance_years() -> str:
	"""Returns all the years for which attendance records exist"""
	Attendance = frappe.qb.DocType("Attendance")
	year_list = (
		frappe.qb.from_(Attendance)
		.select(Extract("year", Attendance.attendance_date).as_("year"))
		.distinct()
	).run(as_dict=True)

	if year_list:
		year_list.sort(key=lambda d: d.year, reverse=True)
	else:
		year_list = [frappe._dict({"year": getdate().year})]

	return "\n".join(cstr(entry.year) for entry in year_list)


def get_chart_data(attendance_map: Dict, filters: Filters) -> Dict:
	days = get_columns_for_days(filters)
	labels = []
	absent = []
	present = []
	leave = []

	for day in days:
		labels.append(day["label"])
		fieldname = day["fieldname"]
		total_absent_on_day = total_leaves_on_day = total_present_on_day = 0

		for employee, attendance_dict in attendance_map.items():
			for shift, attendance in attendance_dict.items():
				attendance_on_day = attendance.get(fieldname)

				if attendance_on_day == "On Leave":
					# leave should be counted only once for the entire day
					total_leaves_on_day += 1
					break
				elif attendance_on_day == "Absent":
					total_absent_on_day += 1
				elif attendance_on_day in ["Present", "Work From Home"]:
					total_present_on_day += 1
				elif attendance_on_day == "Half Day":
					total_present_on_day += 0.5
					total_leaves_on_day += 0.5

		absent.append(total_absent_on_day)
		present.append(total_present_on_day)
		leave.append(total_leaves_on_day)

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Absent", "values": absent},
				{"name": "Present", "values": present},
				{"name": "Leave", "values": leave},
			],
		},
		"type": "line",
		"colors": ["red", "green", "blue"],
	}


def extract_day(date_str):
	# Split the string by underscores
	parts = date_str.split('_')
	# The day is the second part (index 1), so extract it and convert to integer
	day = int(parts[1])
	return day

def get_year(date):
	from datetime import datetime

	date_str = date

	date_obj = datetime.strptime(date_str, "%Y-%m-%d")

	year = date_obj.year

	return year


from datetime import datetime

def convert_to_date_format(date_str, year):
    month_mapping = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12"
    }

    parts = date_str.split("_")

    month_str = parts[0]  
    day_str = parts[1]   

    month_num = month_mapping.get(month_str)
    
    if month_num is None:
        raise ValueError("Invalid month abbreviation")


    year=int(year)
    formatted_date = f"{year}-{month_num}-{day_str.zfill(2)}"

    return formatted_date
