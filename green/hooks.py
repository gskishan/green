from . import __version__ as app_version

app_name = "green"
app_title = "Green"
app_publisher = "kushdhallod@gmail.com"
app_description = "Custom App for customization in Greentek"
app_email = "kushdhallod@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/green/css/green.css"
# app_include_js = "/assets/green/js/green.js"

# include js, css files in header of web template
# web_include_css = "/assets/green/css/green.css"
# web_include_js = "/assets/green/js/green.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "green/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"Item" : "public/js/item/item_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {"ToDo" : "public/js/todo.js",
              "Stock Entry": "public/js/stock_entry.js",
             "Employee Checkin":"public/js/employee_checkin.js"
             }

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "green.utils.jinja_methods",
#	"filters": "green.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "green.install.before_install"
# after_install = "green.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "green.uninstall.before_uninstall"
# after_uninstall = "green.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "green.utils.before_app_install"
# after_app_install = "green.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "green.utils.before_app_uninstall"
# after_app_uninstall = "green.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "green.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#     "Stock Entry":{
#         "validate":"green.green.custom.stock_entry.validate",
                        
#     }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"green.tasks.all"
#	],
#	"daily": [
#		"green.tasks.daily"
#	],
#	"hourly": [
#		"green.tasks.hourly"
#	],
#	"weekly": [
#		"green.tasks.weekly"
#	],
#	"monthly": [
#		"green.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "green.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "green.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "green.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["green.utils.before_request"]
# after_request = ["green.utils.after_request"]

# Job Events
# ----------
# before_job = ["green.utils.before_job"]
# after_job = ["green.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"green.auth.validate"
# ]
fixtures=[
     {
        "dt": "Custom Field", 
        "filters": {
            "module": ["in", ["Green"]]
        }
    },
    {
        "dt": "Property Setter", 
        "filters": {
            "module": ["in", ["Green"]]
        }
    }
]