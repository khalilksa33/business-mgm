import frappe
import json

def main():
    frappe.init(site="26i.uk")
    frappe.connect()
    try:
        pages = frappe.get_all("Web Page", fields=["name", "title", "route", "published"])
        print("WEB PAGES:", json.dumps(pages, default=str))
        
        settings = frappe.db.get_value("Website Settings", "Website Settings", "home_page")
        print("WEBSITE SETTINGS HOME PAGE:", settings)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        frappe.destroy()

if __name__ == "__main__":
    main()
