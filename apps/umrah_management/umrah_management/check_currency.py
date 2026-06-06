import frappe
import json

def main():
    try:
        exchanges = frappe.db.get_all("Currency Exchange", fields=["*"])
        print("EXCHANGES:", json.dumps(exchanges, default=str))
    except Exception as e:
        print("ERROR exchanges:", e)
        
    try:
        # Check standard exchange rate in Currency Exchange or look up company currency
        company = frappe.get_doc("Company", "INSIGHT TRAVEL & TOURISM")
        print("COMPANY CURRENCY:", company.default_currency)
    except Exception as e:
        print("ERROR company:", e)
