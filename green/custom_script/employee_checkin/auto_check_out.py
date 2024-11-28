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
            ec.shift, 
            e.company
        FROM 
            `tabEmployee Checkin` ec
        INNER JOIN 
            `tabEmployee` e ON e.name = ec.employee
        WHERE 
            ec.log_type = 'IN'
            AND DATE(ec.time) = %(today_date)s
             AND e.company = 'GTK Software Solutions LLP'
            AND NOT EXISTS (
                SELECT 
                    1
                FROM 
                    `tabEmployee Checkin` ec_out
                WHERE 
                    ec_out.log_type = 'OUT'
                    AND ec_out.employee = ec.employee
                    AND DATE(ec_out.time) = %(today_date)s
            )
    """, {"today_date": today_date}, as_dict=True)


    for checkin in checkins:
        shift_end_time = frappe.db.get_value(
            "Shift Type", checkin["shift"], "end_time"
        )

        if not shift_end_time:
           
            continue

        checkout_time = f"{today_date} {shift_end_time}"

        checkout_doc = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": checkin["employee"],
             "shift": checkin["shift"],
            "log_type": "OUT",
            "is_auto_created":1,
            "time": checkout_time,
            "longitude":78.506336717,
            "latitude":17.45166747
            
        })
        checkout_doc.insert(ignore_permissions=True)

    frappe.db.commit()

   
