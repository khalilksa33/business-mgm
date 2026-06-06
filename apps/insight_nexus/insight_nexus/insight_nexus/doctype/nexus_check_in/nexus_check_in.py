import frappe
from frappe.model.document import Document
from datetime import datetime


class NexusCheckIn(Document):
    """
    Employee Check-In and Check-Out tracking with optional GPS
    Syncs automatically with ERPNext Attendance and Employee Checkin
    """

    def before_insert(self):
        """Set initial values before insert"""
        if not self.check_in_time:
            self.check_in_time = datetime.now()
        
        # Fetch employee name if not set
        if self.employee and not self.employee_name:
            emp = frappe.get_doc("Employee", self.employee)
            self.employee_name = emp.employee_name

    def on_update(self):
        """Calculate duration and trigger ERP sync"""
        # Calculate duration if checked out
        if self.check_out_time and self.check_in_time:
            duration = (self.check_out_time - self.check_in_time).total_seconds() / 60
            self.duration_minutes = int(duration)
        
        # Sync to ERP
        self.sync_to_erp()

    def sync_to_erp(self):
        """
        Sync check-in data to ERPNext
        Creates or updates Attendance and Employee Checkin records
        """
        try:
            # Get employee and attendance date
            employee = frappe.get_doc("Employee", self.employee)
            attendance_date = self.check_in_time.date()
            
            # 1. Update or create Attendance record
            attendance = self._get_or_create_attendance(employee, attendance_date)
            if attendance:
                self.erp_attendance_id = attendance
            
            # 2. Create Employee Checkin record
            checkin_doc = self._create_employee_checkin(employee)
            if checkin_doc:
                self.erp_checkin_id = checkin_doc
            
            self.sync_status = "Synced"
            frappe.db.set_value("Nexus Check-In", self.name, {
                "sync_status": "Synced",
                "erp_attendance_id": self.erp_attendance_id,
                "erp_checkin_id": self.erp_checkin_id
            })
            frappe.msgprint(f"Synced to ERP: {self.name}")
            
        except Exception as e:
            frappe.log_error(f"Failed to sync Nexus Check-In {self.name}: {str(e)}", "Nexus Sync Error")
            self.sync_status = "Failed"
            frappe.db.set_value("Nexus Check-In", self.name, "sync_status", "Failed")

    def _get_or_create_attendance(self, employee, attendance_date):
        """Get or create Attendance record in ERPNext"""
        try:
            # Check if attendance exists
            existing = frappe.db.get_value(
                "Attendance",
                {
                    "employee": employee.name,
                    "attendance_date": attendance_date
                }
            )
            
            if existing:
                return existing
            
            # Create new Attendance record
            attendance = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee.name,
                "employee_name": employee.employee_name,
                "attendance_date": attendance_date,
                "status": "Present",
                "working_hours": self.duration_minutes / 60 if self.duration_minutes else 0,
                "source": "Insight Nexus"
            })
            attendance.insert()
            return attendance.name
            
        except Exception as e:
            frappe.log_error(f"Failed to sync Attendance: {str(e)}", "Nexus Attendance Sync")
            return None

    def _get_existing_employee_checkin(self, employee, log_type, time):
        """Return an existing ERP Employee Checkin if it already exists."""
        return frappe.db.get_value(
            "Employee Checkin",
            {
                "employee": employee.name,
                "log_type": log_type,
                "time": time
            }
        )

    def _create_employee_checkin(self, employee):
        """Create Employee Checkin record in ERPNext"""
        try:
            location = f"{self.latitude}, {self.longitude}" if self.latitude and self.longitude else None
            device_id = self.device_info or "web"

            existing_checkin = self._get_existing_employee_checkin(employee, "IN", self.check_in_time)
            if existing_checkin:
                checkin_name = existing_checkin
            else:
                checkin = frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": employee.name,
                    "employee_name": employee.employee_name,
                    "time": self.check_in_time,
                    "device_id": device_id,
                    "log_type": "IN",
                    "location": location
                })
                checkin.insert()
                checkin_name = checkin.name

            # If checked out, create or find checkout record
            if self.check_out_time:
                existing_checkout = self._get_existing_employee_checkin(employee, "OUT", self.check_out_time)
                if not existing_checkout:
                    checkout = frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": employee.name,
                        "employee_name": employee.employee_name,
                        "time": self.check_out_time,
                        "device_id": device_id,
                        "log_type": "OUT",
                        "location": location
                    })
                    checkout.insert()

            return checkin_name
            
        except Exception as e:
            frappe.log_error(f"Failed to create Employee Checkin: {str(e)}", "Nexus Checkin Sync")
            return None

    @staticmethod
    def get_employee_checkins(employee, start_date=None, end_date=None, limit=100):
        """
        Get check-ins for an employee
        Used by API endpoints
        """
        filters = {"employee": employee}
        
        if start_date:
            filters["check_in_time"] = [">=", start_date]
        if end_date:
            filters["check_in_time"] = ["<=", end_date]
        
        return frappe.get_list(
            "Nexus Check-In",
            filters=filters,
            fields=["name", "check_in_time", "check_out_time", "duration_minutes", 
                    "latitude", "longitude", "accuracy_meters", "sync_status"],
            order_by="check_in_time desc",
            limit_page_length=limit
        )
