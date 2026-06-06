import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    """Create custom fields on app installation"""
    create_custom_fields({
        "Sales Invoice": [
            {
                "fieldname": "custom_umrah_booking",
                "label": "Umrah Booking",
                "fieldtype": "Link",
                "options": "Umrah Booking",
                "insert_after": "customer",
                "read_only": 1
            }
        ]
    })
