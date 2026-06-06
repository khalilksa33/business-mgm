import frappe

def run():
    frappe.init(site="26i.uk", sites_path="sites")
    frappe.connect()
    
    # Regenerate API keys for info@itt.sa
    user = frappe.get_doc("User", "info@itt.sa")
    api_secret = user.generate_keys()
    user.save(ignore_permissions=True)
    frappe.db.commit()
    
    print(f"API_KEY: {user.api_key}")
    print(f"API_SECRET: {api_secret}")

if __name__ == "__main__":
    run()
