import requests
import frappe, json
from frappe.utils.data import now,get_datetime,get_datetime_str
from frappe.utils import (
	add_days,
    time_diff,
    now
)
import json
frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("daily", allow_site=True, file_count=500)


def make_missing_checkout():
    logger.info("accessed Make Missing Checkout ")

    # Get All Checkins
    checkins = frappe.db.get_list("Employee Checkin", filters={
        "time":  ['between', ['2024-07-15', '2024-07-15']],
        # "time":  ['between', [get_datetime_str(add_days(now(),-1)), get_datetime_str(now())]],
    }, fields=['name', 'time', 'log_type', 'employee'])
    

    # Get All Shifts
    shift_types = frappe.db.get_list("Shift Type", filters={}, fields=['name', 'end_time'])
    
    # Finding Out Missing Checkouts
    missing_checkouts = {}
    for each_checkin in checkins:
        logger.info(f"Each Checkin {each_checkin}")
        if each_checkin["employee"] in missing_checkouts:
            temp_logs = missing_checkouts[each_checkin["employee"]]["data"]
            temp_logs.append({"log_type": each_checkin["log_type"], "time": each_checkin["time"]})
            missing_checkouts[each_checkin["employee"]]["data"] = temp_logs
        else:
            missing_checkouts[each_checkin["employee"]] = {"data": [{"log_type" : each_checkin["log_type"], "time": each_checkin["time"] }] }

    for each in missing_checkouts:
        no_logout = True

        for each_data in missing_checkouts[each]['data']:
            if each_data['log_type'] == 'OUT':
                no_logout = False

        if no_logout:
            logger.info(f"Create Checkout {each}")
            # Create Checkout
            log = frappe.new_doc("Employee Checkin")
            log.employee = each
            log.log_type = "OUT"
            log.time = str(shift_types[0]['end_time'])
            log.insert()
    logger.info("Completed Make Missing Checkout ")
    
    # print(json.dumps(missing_checkouts, indent=1, sort_keys=True, default=str),' Checkout \n\n\n\n\n\n\n')