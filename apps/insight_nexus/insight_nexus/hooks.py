"""
Insight Nexus Module Setup
Registers the module and initializes configuration
"""

from . import __version__ as app_version

app_name = "insight_nexus"
app_title = "Insight Nexus"
app_publisher = "IICC"
app_description = "Multi-sector remote employee check-in and attendance system"
app_icon = "octicon octicon-clock"
app_color = "#667eea"
app_email = "dev@iicc.sa"
app_license = "MIT"

# Includes in <head>
# include_js = ["assets/insight_nexus/js/insight_nexus.js"]
# include_css = ["assets/insight_nexus/css/insight_nexus.css"]

# include_js = {"": ["assets/insight_nexus/js/insight_nexus.js"]}
# include_css = {"": ["assets/insight_nexus/css/insight_nexus.css"]}

# Desk Notifications
# desk_notifications = ["insight_nexus.notifications.get_notification_config"]

# Permissions on Document Types can be configured in the Module Def DocType
# permissions = [
#    {
#        "doctype": "Nexus Check-In",
#        "email_by_document_owner": 1
#    }
# ]

# Home Pages
# home_page_template = "templates/generators/home_page.html"

# Website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website route rules
website_route_rules = [
    {"from_route": "/employee-checkin", "to_route": "check-in"},
    {"from_route": "/checkin", "to_route": "check-in"},
    {"from_route": "/check-in-dashboard", "to_route": "dashboard"},
    {"from_route": "/checkin-dashboard", "to_route": "dashboard"},
]

# Generators
# has_web_form = 1

# Jinja
# jinja = {
# 	"methods": "insight_nexus.utils.jinja_methods",
# 	"filters": "insight_nexus.utils.jinja_filters"
# }

# Installation
# setup_wizard_requires = "postcode_managers/setup.py"
# setup_wizard_stages = [
# 	{
# 		"check_setup_wizard_completeness": [
# 			{
# 				"fieldname": "pre_setup_complete",
# 				"fieldtype": "Check",
# 				"label": "Has setup been completed?"
# 			}
# 		]
# 	},
# 	{
# 		"setup_document_types": [
# 			{
# 				"document_type": "Setup Document",
# 				"setup_source_document": "Setup Target Document"
# 			},
# 		]
# 	},
# 	{
# 		"setup_wizard_complete": [
# 			{
# 				"fieldname": "setup_complete",
# 				"fieldtype": "Check",
# 				"label": "Setup Complete?"
# 			}
# 		]
# 	}
# ]

# Scheduled Tasks
# scheduler_events = {
# 	"all": [
# 		"insight_nexus.tasks.all"
# 	],
# 	"daily": [
# 		"insight_nexus.tasks.daily"
# 	],
# 	"hourly": [
# 		"insight_nexus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"insight_nexus.tasks.weekly"
# 	],
# 	"monthly": [
# 		"insight_nexus.tasks.monthly"
# 	],
# }

# Testing
# before_tests = "insight_nexus.install.before_tests"

# Overrides
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_trash": "method",
# 		"before_rename": "method",
# 		"after_rename": "method"
# 	}
# }

# Whitelisted methods
# whitelist = ["insight_nexus.api.check_in.check_in"]

# User Data Protection
# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_field}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_field}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# ]

# Authentication and authorization
# auth_hooks = [
# 	"insight_nexus.auth.validate"
# ]

# Automatically update python files if they have the same exported data structure
# export_python_objects_in_hooks = True

# List of models to sync with
# models_to_sync = ["DocType", "Document"]

fixtures = [
	{"dt": "DocType", "filters": [["name", "in", ["Nexus Check-In", "JV Partner", "Payment Voucher", "Payment Voucher Item"]]]},
]
