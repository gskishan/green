import frappe
from frappe import _, msgprint
from datetime import datetime

def on_update(self, method=None):
    if self.shift:
        shift = frappe.get_doc("Shift Type", self.shift)
        
        date_d = get_date(self)
        
        if not self.shift_start:
            self.db_set("shift_start", str(date_d) + " " + str(shift.start_time))
        
        if not self.shift_end:
            self.db_set("shift_end", str(date_d) + " " + str(shift.end_time))


def get_date(self):
    datetime_value = self.time
    
    if isinstance(datetime_value, str):
        dt = datetime.strptime(datetime_value, '%Y-%m-%d %H:%M:%S')
    elif isinstance(datetime_value, datetime):
        dt = datetime_value
    else:
        raise ValueError("self.time must be a string or a datetime object")
    
    return dt.date()
