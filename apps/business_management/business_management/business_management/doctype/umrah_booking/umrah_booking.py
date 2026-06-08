import frappe
from frappe.model.document import Document
from frappe.utils import flt, today


class UmrahBooking(Document):
    def validate(self):
        """Perform validation and auto-calculations"""
        self.fetch_package_rate()
        self.populate_pilgrim_details()
        self.calculate_totals()

    def on_update(self):
        """Sync group capacity after saving"""
        self.update_group_booked_capacity()

    def on_trash(self):
        """Sync group capacity after deleting"""
        self.update_group_booked_capacity()

    def fetch_package_rate(self):
        """Fetch pricing rate from Umrah Package based on sharing type"""
        if not self.package or not self.sharing_type:
            return

        rate_field_map = {
            "Sharing": "price_sharing",
            "Quad": "price_quad",
            "Triple": "price_triple",
            "Double": "price_double",
            "Single": "price_single"
        }

        field_to_fetch = rate_field_map.get(self.sharing_type)
        if field_to_fetch:
            rate = frappe.db.get_value("Umrah Package", self.package, field_to_fetch)
            self.rate = flt(rate)

    def populate_pilgrim_details(self):
        """Populate read-only pilgrim details in the child table"""
        for item in self.get("pilgrims"):
            if item.pilgrim:
                pilgrim_doc = frappe.get_doc("Umrah Pilgrim", item.pilgrim)
                item.first_name = pilgrim_doc.first_name
                item.last_name = pilgrim_doc.last_name
                item.passport_number = pilgrim_doc.passport_number
                item.visa_status = pilgrim_doc.visa_status

    def calculate_totals(self):
        """Calculate total pilgrims and total amount"""
        self.total_pilgrims = len(self.get("pilgrims") or [])
        self.total_amount = flt(self.rate) * self.total_pilgrims

    def update_group_booked_capacity(self):
        """Update total booked pilgrims on the linked Umrah Group"""
        if self.group:
            update_group_capacity(self.group)


def update_group_capacity(group_name):
    """Calculate and set total booked capacity for an Umrah Group"""
    if not group_name:
        return

    # Sum total pilgrims for all confirmed/active bookings in this group
    # Excluding cancelled bookings
    bookings = frappe.get_all(
        "Umrah Booking",
        filters={
            "group": group_name,
            "status": ["in", ["Draft", "Confirmed", "Completed"]]
        },
        fields=["total_pilgrims"]
    )
    total_booked = sum(b.get("total_pilgrims") or 0 for b in bookings)
    frappe.db.set_value("Umrah Group", group_name, "total_booked", total_booked)


@frappe.whitelist()
def create_sales_invoice(booking_name):
    """
    Whitelist method to create an ERPNext Sales Invoice from an Umrah Booking.
    Called via frontend button.
    """
    booking = frappe.get_doc("Umrah Booking", booking_name)

    if booking.sales_invoice:
        frappe.throw(f"Sales Invoice {booking.sales_invoice} already exists for this booking.")

    # Determine Company
    company = booking.get("company") or frappe.db.get_default("company")
    if not company:
        companies = frappe.get_all("Company", limit=1)
        if companies:
            company = companies[0].name
        else:
            frappe.throw("Please configure at least one Company in ERPNext.")

    # Fetch default accounts
    income_account = frappe.db.get_value("Company", company, "default_income_account")
    cost_center = frappe.db.get_value("Company", company, "cost_center")

    # Fallbacks if default company accounts are empty
    if not income_account:
        income_account = frappe.db.get_value("Account", {"company": company, "root_type": "Income", "is_group": 0})
    if not cost_center:
        cost_center = frappe.db.get_value("Cost Center", {"company": company, "is_group": 0})

    # Create Sales Invoice doc
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "company": company,
        "customer": booking.customer,
        "posting_date": today(),
        "due_date": today(),
        "items": [
            {
                "item_name": f"Umrah Package: {booking.package} ({booking.sharing_type} Sharing)",
                "description": f"Umrah Booking {booking.name} for {booking.total_pilgrims} pilgrim(s)",
                "qty": booking.total_pilgrims,
                "rate": booking.rate,
                "uom": "Nos",
                "income_account": income_account,
                "cost_center": cost_center
            }
        ],
        "custom_umrah_booking": booking.name  # To track reference back
    })

    invoice.insert(ignore_permissions=True)

    # Link invoice to booking
    booking.sales_invoice = invoice.name
    booking.save(ignore_permissions=True)

    return invoice.name
