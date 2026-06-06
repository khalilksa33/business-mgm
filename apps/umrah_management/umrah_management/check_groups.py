import frappe

def main():
    groups = frappe.db.get_all("Umrah Group", fields=["name", "group_name", "package", "departure_date", "status"])
    print("ALL GROUPS:")
    print(frappe.as_json(groups, indent=2))
