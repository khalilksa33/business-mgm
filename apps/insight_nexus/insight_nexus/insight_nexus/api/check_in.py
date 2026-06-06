"""
Insight Nexus API Endpoints
REST API for check-in/check-out operations
"""

import frappe
from datetime import datetime, timedelta


@frappe.whitelist(methods=["POST"], allow_guest=True)
def check_in(latitude=None, longitude=None, accuracy=None, device_info=None, notes=None):
    """
    Create a check-in record
    Called when employee clicks "Check In"
    """
    try:
        user = frappe.session.user
        employee = frappe.db.get_value("Employee", {"user_id": user})
        
        if not employee:
            return {
                "status": "error",
                "message": "User is not linked to an employee"
            }
        
        emp_doc = frappe.get_doc("Employee", employee)
        
        # Validate GPS accuracy if provided
        if latitude and longitude and accuracy:
            threshold = frappe.conf.get("insight_nexus", {}).get("gps_accuracy_threshold", 50)
            if int(accuracy) > threshold:
                return {
                    "status": "error",
                    "message": f"GPS accuracy too low ({accuracy}m). Threshold: {threshold}m",
                    "accuracy": accuracy,
                    "threshold": threshold
                }
        
        # Prevent active open check-in from being created again
        active_checkin = frappe.db.get_value(
            "Nexus Check-In",
            {"employee": employee, "check_out_time": ["is", "not set"]}
        )
        if active_checkin:
            return {
                "status": "error",
                "message": "An active check-in already exists. Please check out before creating a new check-in.",
                "active_check_in_id": active_checkin
            }

        # Check cooldown after the most recent check-in
        cooldown = frappe.conf.get("insight_nexus", {}).get("check_in_cooldown_minutes", 15)
        last_checkin_time = frappe.db.get_value(
            "Nexus Check-In",
            {"employee": employee},
            "check_in_time",
            order_by="check_in_time desc"
        )
        if last_checkin_time:
            last_checkin_dt = frappe.utils.get_datetime(last_checkin_time)
            if frappe.utils.now_datetime() - last_checkin_dt < timedelta(minutes=cooldown):
                return {
                    "status": "error",
                    "message": f"Please wait {cooldown} minutes between check-ins",
                    "retry_after": cooldown * 60
                }
        
        # Create check-in
        checkin = frappe.get_doc({
            "doctype": "Nexus Check-In",
            "employee": employee,
            "employee_name": emp_doc.employee_name,
            "company": emp_doc.company,
            "sector": emp_doc.department,
            "latitude": latitude,
            "longitude": longitude,
            "accuracy_meters": accuracy,
            "device_info": device_info,
            "notes": notes,
            "sync_status": "Pending"
        })
        checkin.insert()
        
        return {
            "status": "success",
            "check_in_id": checkin.name,
            "timestamp": str(checkin.check_in_time),
            "message": "Check-in successful"
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Nexus Check-In Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(methods=["POST"], allow_guest=True)
def check_out(check_in_id=None, notes=None):
    """
    Update a check-in with check-out time
    Called when employee clicks "Check Out"
    """
    try:
        user = frappe.session.user
        employee = frappe.db.get_value("Employee", {"user_id": user})
        
        if not employee:
            return {
                "status": "error",
                "message": "User is not linked to an employee"
            }
        
        # If no check_in_id provided, find the active check-in
        if not check_in_id:
            check_in_id = frappe.db.get_value(
                "Nexus Check-In",
                {
                    "employee": employee,
                    "check_out_time": ["is", "not set"]
                },
                "name"
            )
            
            if not check_in_id:
                return {
                    "status": "error",
                    "message": "No active check-in found"
                }
        
        # Get and update check-in
        checkin = frappe.get_doc("Nexus Check-In", check_in_id)
        
        # Verify ownership
        if checkin.employee != employee:
            return {
                "status": "error",
                "message": "Unauthorized"
            }
        
        # Check if already checked out
        if checkin.check_out_time:
            return {
                "status": "error",
                "message": "Already checked out"
            }
        
        checkin.check_out_time = datetime.now()
        if notes:
            checkin.notes = notes
        checkin.save()
        
        return {
            "status": "success",
            "check_in_id": checkin.name,
            "check_in_time": str(checkin.check_in_time),
            "check_out_time": str(checkin.check_out_time),
            "duration_minutes": checkin.duration_minutes,
            "message": "Check-out successful"
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Nexus Check-Out Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_check_ins(start_date=None, end_date=None, limit=100):
    """
    Get check-in history for current user
    """
    try:
        user = frappe.session.user
        employee = frappe.db.get_value("Employee", {"user_id": user})
        
        if not employee:
            return {
                "status": "error",
                "message": "User is not linked to an employee"
            }
        
        from insight_nexus.insight_nexus.doctype.nexus_check_in.nexus_check_in import NexusCheckIn
        
        checkins = NexusCheckIn.get_employee_checkins(
            employee,
            start_date=start_date,
            end_date=end_date,
            limit=int(limit)
        )
        
        return {
            "status": "success",
            "check_ins": checkins
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Nexus Get Check-Ins Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_dashboard():
    """
    Get dashboard data for the employee
    """
    try:
        user = frappe.session.user
        employee = frappe.db.get_value("Employee", {"user_id": user})
        
        if not employee:
            return {
                "status": "error",
                "message": "Please login with your ERP account to use check-in portal."
            }
        
        emp_doc = frappe.get_doc("Employee", employee)
        
        # Get today's check-ins
        today = frappe.utils.today()
        today_checkins = frappe.get_list(
            "Nexus Check-In",
            filters={
                "employee": employee,
                "check_in_time": [">=", f"{today} 00:00:00"]
            },
            fields=["name", "check_in_time", "check_out_time", "duration_minutes"],
            order_by="check_in_time desc"
        )
        
        # Get current month history
        month_start = today[:8] + "01"
        month_checkins = frappe.get_list(
            "Nexus Check-In",
            filters={
                "employee": employee,
                "check_in_time": [">=", f"{month_start} 00:00:00"]
            },
            fields=["name", "check_in_time", "check_out_time", "duration_minutes"],
            order_by="check_in_time desc"
        )
        
        # Get current status
        current_checkin = frappe.db.get_value(
            "Nexus Check-In",
            {
                "employee": employee,
                "check_out_time": ["is", "not set"],
                "check_in_time": [">=", f"{today} 00:00:00"]
            },
            "name"
        )
        
        return {
            "status": "success",
            "employee": employee,
            "employee_name": emp_doc.employee_name,
            "company": emp_doc.company,
            "department": emp_doc.department,
            "checked_in": bool(current_checkin),
            "current_check_in_id": current_checkin,
            "today_check_ins": today_checkins,
            "month_check_ins": month_checkins,
            "month_total": len(month_checkins)
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Nexus Dashboard Error")
        return {
            "status": "error",
            "message": str(e)
        }
