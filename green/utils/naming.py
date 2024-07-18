
import frappe
from frappe import _
from frappe.model.naming import NamingSeries
from frappe.utils import cint, cstr, now_datetime
from frappe.utils.data import nowdate


@frappe.whitelist()
def get_current_naming_value(prefix):
    current_value = None
    if prefix is not None:
        current_value = NamingSeries(prefix).get_current_value()
    return current_value



def set_naming_counter(self):
    if self.is_new():
        try:
            date = nowdate()
            # yyyy-mm-dd
            year = date[2:4]
            month = date[5:7]
            # Change Naming Format
            name = self.naming_series 
            name = name.replace(".MM.", month)
            name = name.replace(".YY.", year)
            # Change Month to Previous Month 
            prev_name = self.naming_series
            prev_name = prev_name.replace(".MM.", "0"* (2- len(str(int(month)))) + str(int(month) - 1))
            prev_name = prev_name.replace(".YY.", year)
            # Check Is there any Naming Counter for Current Month if not then create it
            count = get_current_naming_value(name)
            prev_count = get_current_naming_value(prev_name)

            Series = frappe.qb.DocType("Series")
            prefix = name
            prev_count += 1
            last_no = "0"* (5 - len(str(prev_count))) + str(prev_count)

            if count == 1 or count == 0:
                # Initialize if not present in DB
                if frappe.db.get_value("Series", prefix, "name", order_by="name") is None:
                    frappe.qb.into(Series).insert(prefix, new_count).columns("name", "current").run()
                else:
                    (frappe.qb.update(Series).set(Series.current, cint(prev_count)).where(Series.name == prefix)).run()
                self.name = prefix + last_no
        except:
            pass