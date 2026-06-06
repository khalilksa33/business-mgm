import frappe
import json

def main():
    packages = frappe.db.get_all("Umrah Package", fields=["name", "package_code", "package_name", "makkah_hotel", "makkah_nights", "madinah_hotel", "madinah_nights", "price_sharing", "price_quad", "price_triple", "price_double", "status"])
    print(json.dumps(packages, indent=2))
