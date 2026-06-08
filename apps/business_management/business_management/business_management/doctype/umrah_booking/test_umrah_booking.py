import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days

from business_management.business_management.doctype.umrah_booking.umrah_booking import create_sales_invoice


class TestUmrahBooking(FrappeTestCase):
    def setUp(self):
        """Set up master data for test cases"""
        # Determine a test company or create one
        company_name = "INSIGHT TRAVEL & TOURISM"
        if not frappe.db.exists("Company", company_name):
            default_company = frappe.db.get_default("company")
            if default_company:
                self.company = default_company
            else:
                companies = frappe.get_all("Company", limit=1)
                if companies:
                    self.company = companies[0].name
                else:
                    self.company = frappe.get_doc({
                        "doctype": "Company",
                        "company_name": "_Test Company",
                        "default_currency": "SAR"
                    }).insert(ignore_permissions=True).name
        else:
            self.company = company_name

        # Create a test customer if not exists
        if not frappe.db.exists("Customer", "_Test Umrah Customer"):
            self.customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "_Test Umrah Customer",
                "customer_group": "All Customer Groups",
                "territory": "All Territories"
            }).insert(ignore_permissions=True)
        else:
            self.customer = frappe.get_doc("Customer", "_Test Umrah Customer")

        # Use an existing country
        if frappe.db.exists("Country", "Saudi Arabia"):
            self.country = frappe.get_doc("Country", "Saudi Arabia")
        elif frappe.db.exists("Country", "India"):
            self.country = frappe.get_doc("Country", "India")
        else:
            self.country = frappe.get_doc({
                "doctype": "Country",
                "country_name": "_Test Country",
                "code": "TC"
            }).insert(ignore_permissions=True)

        # Create a test package
        if frappe.db.exists("Umrah Package", "PKG-TEST-01"):
            frappe.delete_doc("Umrah Package", "PKG-TEST-01", ignore_permissions=True)

        self.package = frappe.get_doc({
            "doctype": "Umrah Package",
            "package_code": "PKG-TEST-01",
            "package_name": "Test Package 15 Days",
            "status": "Active",
            "valid_from": today(),
            "valid_to": add_days(today(), 30),
            "price_sharing": 1500,
            "price_quad": 2000,
            "price_triple": 2500,
            "price_double": 3000,
            "price_single": 4000
        }).insert(ignore_permissions=True)

        # Create a test group
        if frappe.db.exists("Umrah Group", "GRP-TEST-01"):
            frappe.delete_doc("Umrah Group", "GRP-TEST-01", ignore_permissions=True)

        self.group = frappe.get_doc({
            "doctype": "Umrah Group",
            "group_code": "GRP-TEST-01",
            "group_name": "Test Group Caravan",
            "package": self.package.name,
            "departure_date": add_days(today(), 5),
            "return_date": add_days(today(), 20),
            "max_capacity": 45,
            "status": "Planning"
        }).insert(ignore_permissions=True)

        # Create two test pilgrims
        if frappe.db.exists("Umrah Pilgrim", "PPT-TEST-01"):
            frappe.delete_doc("Umrah Pilgrim", "PPT-TEST-01", ignore_permissions=True)
        self.pilgrim1 = frappe.get_doc({
            "doctype": "Umrah Pilgrim",
            "first_name": "Ahmad",
            "last_name": "Ali",
            "gender": "Male",
            "nationality": self.country.name,
            "passport_number": "PPT-TEST-01",
            "passport_expiry": add_days(today(), 365),
            "date_of_birth": "1990-01-01",
            "visa_status": "Issued",
            "visa_number": "VISA-12345"
        }).insert(ignore_permissions=True)

        if frappe.db.exists("Umrah Pilgrim", "PPT-TEST-02"):
            frappe.delete_doc("Umrah Pilgrim", "PPT-TEST-02", ignore_permissions=True)
        self.pilgrim2 = frappe.get_doc({
            "doctype": "Umrah Pilgrim",
            "first_name": "Fatima",
            "last_name": "Ahmad",
            "gender": "Female",
            "nationality": self.country.name,
            "passport_number": "PPT-TEST-02",
            "passport_expiry": add_days(today(), 365),
            "date_of_birth": "1992-05-15",
            "visa_status": "Not Applied"
        }).insert(ignore_permissions=True)

    def tearDown(self):
        """Clean up database after tests"""
        frappe.db.rollback()

    def test_booking_pricing_and_pilgrims(self):
        """Test that rate auto-fetches and total is computed correctly"""
        booking = frappe.get_doc({
            "doctype": "Umrah Booking",
            "customer": self.customer.name,
            "company": self.company,
            "package": self.package.name,
            "group": self.group.name,
            "sharing_type": "Double",
            "booking_date": today(),
            "status": "Draft",
            "pilgrims": [
                {"pilgrim": self.pilgrim1.name},
                {"pilgrim": self.pilgrim2.name}
            ]
        })
        booking.insert(ignore_permissions=True)

        # Assertions
        # 1. Double price is 3000
        self.assertEqual(booking.rate, 3000)
        # 2. Total pilgrims count
        self.assertEqual(booking.total_pilgrims, 2)
        # 3. Total amount is rate * count = 6000
        self.assertEqual(booking.total_amount, 6000)

        # 4. Check that pilgrim child table columns are auto-populated
        self.assertEqual(booking.pilgrims[0].first_name, "Ahmad")
        self.assertEqual(booking.pilgrims[0].passport_number, "PPT-TEST-01")
        self.assertEqual(booking.pilgrims[1].first_name, "Fatima")
        self.assertEqual(booking.pilgrims[1].passport_number, "PPT-TEST-02")

        # 5. Check group booked capacity is updated
        group_booked = frappe.db.get_value("Umrah Group", self.group.name, "total_booked")
        self.assertEqual(group_booked, 2)

    def test_sales_invoice_creation(self):
        """Test creating and submitting a Sales Invoice from booking"""
        booking = frappe.get_doc({
            "doctype": "Umrah Booking",
            "customer": self.customer.name,
            "company": self.company,
            "package": self.package.name,
            "group": self.group.name,
            "sharing_type": "Quad",
            "booking_date": today(),
            "status": "Draft",
            "pilgrims": [
                {"pilgrim": self.pilgrim1.name}
            ]
        })
        booking.insert(ignore_permissions=True)

        # Create invoice
        invoice_name = create_sales_invoice(booking.name)

        # Verify link is saved in booking
        booking.reload()
        self.assertEqual(booking.sales_invoice, invoice_name)

        # Verify invoice document is saved as Draft
        invoice = frappe.get_doc("Sales Invoice", invoice_name)
        self.assertEqual(invoice.docstatus, 0)  # Draft
        self.assertEqual(invoice.customer, self.customer.name)
        self.assertEqual(invoice.items[0].qty, 1)
        self.assertEqual(invoice.items[0].rate, 2000)  # Quad price is 2000
        self.assertEqual(invoice.custom_umrah_booking, booking.name)

    def test_booking_sharing_rate(self):
        """Test that the new Sharing rate fetches correctly"""
        booking = frappe.get_doc({
            "doctype": "Umrah Booking",
            "customer": self.customer.name,
            "company": self.company,
            "package": self.package.name,
            "group": self.group.name,
            "sharing_type": "Sharing",
            "booking_date": today(),
            "status": "Draft",
            "pilgrims": [
                {"pilgrim": self.pilgrim1.name}
            ]
        })
        booking.insert(ignore_permissions=True)
        self.assertEqual(booking.rate, 1500)
        self.assertEqual(booking.total_amount, 1500)


def run_manual_tests():
    """Run tests programmatically to bypass test runner dependencies"""
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(TestUmrahBooking("test_booking_pricing_and_pilgrims"))
    suite.addTest(TestUmrahBooking("test_booking_sharing_rate"))
    suite.addTest(TestUmrahBooking("test_sales_invoice_creation"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
