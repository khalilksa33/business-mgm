import frappe

def main():
    # 1. Deactivate duplicate hotel packages
    duplicates = ["DAT-2909", "DT-2909", "DT-2512", "SI-2909", "SI-2512"]
    for code in duplicates:
        if frappe.db.exists("Umrah Package", code):
            doc = frappe.get_doc("Umrah Package", code)
            doc.status = "Inactive"
            doc.save(ignore_permissions=True)
            print(f"Deactivated repeating package: {code}")
            
    # 2. Update remaining active hotel packages by multiplying prices by 74 (SAR to PKR)
    active_hotel_packages = ["DAT-2809", "DT-2809", "DT-2412", "SI-2809", "SI-2412"]
    for code in active_hotel_packages:
        if frappe.db.exists("Umrah Package", code):
            doc = frappe.get_doc("Umrah Package", code)
            # Check if prices are already converted (i.e. > 20000) to prevent double conversion
            if doc.price_sharing < 20000:
                doc.price_sharing = round(doc.price_sharing * 74)
                doc.price_quad = round(doc.price_quad * 74)
                doc.price_triple = round(doc.price_triple * 74)
                doc.price_double = round(doc.price_double * 74)
                if doc.price_single > 0:
                    doc.price_single = round(doc.price_single * 74)
                doc.save(ignore_permissions=True)
                print(f"Converted SAR to PKR for active package: {code} (SH={doc.price_sharing})")
            else:
                print(f"Package {code} already has converted PKR prices: {doc.price_sharing}")

    # 3. Create missing Hotels as Suppliers in ERPNext if they don't exist
    makkah_hotels = ["Dyar Matar", "Land Premium", "Fawad Nasa", "Nawarat Shams 3"]
    madinah_hotels = ["Warda Sultana", "Rose Ward", "Ansar Plus", "Manazil Widyar", "Rou Tiba"]
    
    for hotel in makkah_hotels + madinah_hotels:
        if not frappe.db.exists("Supplier", hotel):
            doc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": hotel,
                "supplier_type": "Company",
                "supplier_group": "Hotel"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Supplier (Hotel): {hotel}")
        else:
            print(f"Supplier {hotel} already exists")

    # 4. Create historical packages from package-hh-1446.jpg
    historical_data = [
        {
            "package_code": "PKG-HH-1446-1",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 1",
            "makkah_hotel": "Dyar Matar",
            "makkah_nights": 10,
            "madinah_hotel": "Warda Sultana",
            "madinah_nights": 10,
            "price_sharing": 192000,
            "price_quad": 195000,
            "price_triple": 199000,
            "price_double": 208000,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        },
        {
            "package_code": "PKG-HH-1446-2",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 2",
            "makkah_hotel": "Land Premium",
            "makkah_nights": 10,
            "madinah_hotel": "Rose Ward",
            "madinah_nights": 10,
            "price_sharing": 201000,
            "price_quad": 207000,
            "price_triple": 214000,
            "price_double": 231500,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        },
        {
            "package_code": "PKG-HH-1446-3",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 3",
            "makkah_hotel": "Fawad Nasa",
            "makkah_nights": 10,
            "madinah_hotel": "Ansar Plus",
            "madinah_nights": 10,
            "price_sharing": 214000,
            "price_quad": 222000,
            "price_triple": 235000,
            "price_double": 263000,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        },
        {
            "package_code": "PKG-HH-1446-4",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 4",
            "makkah_hotel": "Fawad Nasa",
            "makkah_nights": 10,
            "madinah_hotel": "Manazil Widyar",
            "madinah_nights": 10,
            "price_sharing": 223000,
            "price_quad": 233500,
            "price_triple": 250500,
            "price_double": 285500,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        },
        {
            "package_code": "PKG-HH-1446-5",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 5",
            "makkah_hotel": "Fawad Nasa",
            "makkah_nights": 10,
            "madinah_hotel": "Rou Tiba",
            "madinah_nights": 10,
            "price_sharing": 229500,
            "price_quad": 240500,
            "price_triple": 259500,
            "price_double": 299500,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        },
        {
            "package_code": "PKG-HH-1446-6",
            "package_name": "Hijrat-ul-Haram Rabi-ul-Awwal - Pkg 6",
            "makkah_hotel": "Nawarat Shams 3",
            "makkah_nights": 10,
            "madinah_hotel": "Rou Tiba",
            "madinah_nights": 10,
            "price_sharing": 0,
            "price_quad": 258500,
            "price_triple": 283500,
            "price_double": 335000,
            "description": "Historical JV Package - Rabi-ul-Awwal Season 1446"
        }
    ]

    for data in historical_data:
        code = data["package_code"]
        if not frappe.db.exists("Umrah Package", code):
            doc = frappe.get_doc({
                "doctype": "Umrah Package",
                "package_code": code,
                "package_name": data["package_name"],
                "makkah_hotel": data["makkah_hotel"],
                "makkah_nights": data["makkah_nights"],
                "madinah_hotel": data["madinah_hotel"],
                "madinah_nights": data["madinah_nights"],
                "price_sharing": data["price_sharing"],
                "price_quad": data["price_quad"],
                "price_triple": data["price_triple"],
                "price_double": data["price_double"],
                "status": "Active",
                "description": data["description"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Created historical package: {code}")
        else:
            doc = frappe.get_doc("Umrah Package", code)
            doc.status = "Active"
            doc.save(ignore_permissions=True)
            print(f"Historical package {code} already exists, marked as Active")
            
    frappe.db.commit()
    print("Database transaction committed successfully!")

if __name__ == '__main__':
    main()
