import frappe
from frappe.website.serve import get_response

def get_pages():
    try:
        # Render home page
        frappe.local.request = frappe._dict(path="")
        response = get_response()
        print("HOME PAGE STATUS:", response.status_code)
        print("HOME PAGE CONTENT PREVIEW:", response.get_data().decode()[:500] if response.get_data() else "None")
        
        # Render packages page
        frappe.local.request = frappe._dict(path="packages")
        response = get_response()
        print("PACKAGES PAGE STATUS:", response.status_code)
        print("PACKAGES PAGE CONTENT PREVIEW:", response.get_data().decode()[:500] if response.get_data() else "None")
    except Exception as e:
        print("ERROR RENDERING:", e)
