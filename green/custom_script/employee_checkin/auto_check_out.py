import frappe
from frappe.utils import now_datetime, getdate, get_datetime_str

def auto_checkout_employees():
    """
    Automatically check out employees who checked in but did not check out  time of this fuction  to get excuted in day end 11:50.
    calling it vai sheduler 
    """
    today_date = getdate(now_datetime())

    checkins = frappe.db.sql("""
        SELECT 
            ec.name AS checkin_name, 
            ec.employee, 
            ec.time, 
            e.shift_type, 
            e.company
        FROM 
            `tabEmployee Checkin` ec
        INNER JOIN 
            `tabEmployee` e ON e.name = ec.employee
        WHERE 
            ec.log_type = 'IN'
            AND DATE(ec.time) = CURDATE()
            AND NOT EXISTS (
                SELECT 
                    1
                FROM 
                    `tabEmployee Checkin` ec_out
                WHERE 
                    ec_out.log_type = 'OUT'
                    AND ec_out.employee = ec.employee
                    AND DATE(ec_out.time) = CURDATE()
            )
    """, as_dict=True)

    for checkin in checkins:
        shift_end_time = frappe.db.get_value(
            "Shift Type", checkin["shift_type"], "end_time"
        )

        if not shift_end_time:
           
            continue

        checkout_time = f"{today_date} {shift_end_time}"

        checkout_doc = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": checkin["employee"],
            "log_type": "OUT",
            "is_auto_created":1,
            "time": checkout_time,
        })
        checkout_doc.insert(ignore_permissions=True)

    frappe.db.commit()

   
