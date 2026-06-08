import frappe

def main():
    try:
        # Check if iicc-portal exists and change its route to packages
        if frappe.db.exists("Web Page", "iicc-portal"):
            doc = frappe.get_doc("Web Page", "iicc-portal")
            doc.route = "packages"
            doc.save()
            frappe.db.commit()
            print("Renamed iicc-portal route to 'packages'")
        
        # Directly update the database value for Website Settings to avoid validation errors
        frappe.db.set_value("Website Settings", "Website Settings", "home_page", "index")
        frappe.db.commit()
        print("Directly set Website Settings home_page to 'index' in the database")
    except Exception as e:
        print("ERROR:", e)
