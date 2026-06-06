from datetime import datetime
from unittest.mock import MagicMock, patch

import frappe
from frappe.tests import UnitTestCase

from insight_nexus.insight_nexus.api import check_in as check_in_module
from insight_nexus.insight_nexus.doctype.nexus_check_in.nexus_check_in import NexusCheckIn


class TestNexusCheckIn(UnitTestCase):

    def test_check_in_blocks_active_open_checkin(self):
        with patch.object(frappe.session, 'user', 'test@example.com'):
            with patch('frappe.db.get_value', side_effect=['EMP-001', 'NEXUS-0001']):
                result = check_in_module.check_in()

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'An active check-in already exists. Please check out before creating a new check-in.')
        self.assertEqual(result['active_check_in_id'], 'NEXUS-0001')

    def test_check_in_respects_cooldown(self):
        with patch.object(frappe.session, 'user', 'test@example.com'):
            with patch('frappe.db.get_value', side_effect=['EMP-001', None, '2026-05-07 10:00:00']):
                with patch('frappe.utils.now_datetime', return_value=datetime(2026, 5, 7, 10, 10)):
                    result = check_in_module.check_in()

        self.assertEqual(result['status'], 'error')
        self.assertIn('retry_after', result)
        self.assertEqual(result['message'], 'Please wait 15 minutes between check-ins')

    def test_create_employee_checkin_reuses_existing_log(self):
        employee_doc = MagicMock(name='EMP-001', employee_name='Test User')
        nexus = NexusCheckIn(
            employee='EMP-001',
            check_in_time=datetime(2026, 5, 7, 9, 0),
            check_out_time=None,
            latitude=24.0,
            longitude=54.0,
            device_info='mobile'
        )

        with patch('frappe.get_doc', return_value=employee_doc):
            with patch('frappe.db.get_value', return_value='CKIN-IN-1'):
                result = nexus._create_employee_checkin(employee_doc)

        self.assertEqual(result, 'CKIN-IN-1')
