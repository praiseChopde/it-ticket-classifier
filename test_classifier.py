"""
Tests for the IT Ticket Classifier.
Run with: python test_classifier.py
"""

import unittest
from classifier import classify_ticket, classify_category, classify_priority


class TestCategoryClassification(unittest.TestCase):

    def test_hardware_laptop(self):
        result = classify_ticket("My laptop screen is cracked and won't turn on")
        self.assertEqual(result["category"], "Hardware")

    def test_hardware_printer(self):
        result = classify_ticket("The printer in the Finance office is not working")
        self.assertEqual(result["category"], "Hardware")

    def test_network_wifi(self):
        result = classify_ticket("I can't connect to the Wi-Fi network today")
        self.assertEqual(result["category"], "Network")

    def test_network_vpn(self):
        result = classify_ticket("GlobalProtect VPN keeps disconnecting when I work from home")
        self.assertEqual(result["category"], "Network")

    def test_account_password(self):
        result = classify_ticket("My password expired and I can't log in to my workstation")
        self.assertEqual(result["category"], "Account")

    def test_account_locked(self):
        result = classify_ticket("Account is locked out after too many failed login attempts")
        self.assertEqual(result["category"], "Account")

    def test_software_outlook(self):
        result = classify_ticket("Outlook is not receiving emails since this morning")
        self.assertEqual(result["category"], "Software")

    def test_software_crash(self):
        result = classify_ticket("Microsoft Teams keeps crashing when I try to join a meeting")
        self.assertEqual(result["category"], "Software")

    def test_other_empty_keywords(self):
        result = classify_ticket("I need help with something in room 204 on the third floor")
        self.assertEqual(result["category"], "Other")


class TestPriorityClassification(unittest.TestCase):

    def test_high_locked_out(self):
        priority = classify_priority("I am locked out and cannot log in to anything")
        self.assertEqual(priority, "High")

    def test_high_urgent(self):
        priority = classify_priority("Urgent: laptop won't turn on, I have a presentation in an hour")
        self.assertEqual(priority, "High")

    def test_medium_slow(self):
        priority = classify_priority("My computer has been running slow all week")
        self.assertEqual(priority, "Medium")

    def test_low_request(self):
        priority = classify_priority("I would like to request a second monitor for my desk")
        self.assertEqual(priority, "Low")


class TestFullPipeline(unittest.TestCase):

    def test_result_has_all_fields(self):
        result = classify_ticket("My laptop won't connect to Wi-Fi")
        self.assertIn("category", result)
        self.assertIn("priority", result)
        self.assertIn("first_step", result)
        self.assertIn("description", result)
        self.assertIn("scores", result)

    def test_empty_description_raises(self):
        with self.assertRaises(ValueError):
            classify_ticket("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            classify_ticket("   ")

    def test_first_step_not_empty(self):
        result = classify_ticket("I need help with my password reset")
        self.assertTrue(len(result["first_step"]) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
