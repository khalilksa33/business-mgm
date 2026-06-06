import frappe
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

def run():
    # Mock request environment for validation to succeed
    builder = EnvironBuilder(path='/')
    env = builder.get_environ()
    frappe.local.request = Request(env)

    settings = frappe.get_doc("Website Settings")
    updated = False
    for item in settings.top_bar_items:
        if item.url == "https://26i.uk/#ceo":
            item.url = "/packages#ceo"
            updated = True
        elif item.url == "https://26i.uk/#expertise":
            item.url = "/packages#expertise"
            updated = True
        elif item.url == "https://26i.uk/#services":
            item.url = "/packages#services"
            updated = True
        elif item.url == "https://26i.uk/#contact":
            item.url = "/packages#contact"
            updated = True
            
    if updated:
        settings.save(ignore_permissions=True)
        frappe.db.commit()
        print("Updated Website Settings Top Bar Items successfully with request mock!")
    else:
        print("No updates needed for Website Settings Top Bar Items.")
