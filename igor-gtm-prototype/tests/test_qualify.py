import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qualify import qualify_leads


class QualificationTests(unittest.TestCase):
    def test_scoring(self):
        leads = [{"email": "a@x.test", "company_domain": "x.test",
                  "segment": "enterprise", "recent_buying_signal": True,
                  "verified_work_email": True}]
        self.assertEqual(qualify_leads(leads)[0]["score"], 100)

    def test_duplicate_normalized_email(self):
        leads = [{"email": "A@x.test", "company_domain": "x.test"},
                 {"email": "a@x.test", "company_domain": "x.test"}]
        self.assertEqual(qualify_leads(leads)[1]["status"], "excluded")

    def test_crm_exclusion(self):
        lead = {"email": "a@x.test", "company_domain": "x.test"}
        self.assertEqual(qualify_leads([lead], existing_emails={"A@X.TEST"})[0]["status"], "excluded")

    def test_blocklist(self):
        lead = {"email": "a@x.test", "company_domain": "www.x.test"}
        self.assertEqual(qualify_leads([lead], blocked_domains={"x.test"})[0]["status"], "excluded")

    def test_missing_email_needs_review(self):
        lead = {"company_domain": "x.test"}
        self.assertEqual(qualify_leads([lead])[0]["status"], "review")


if __name__ == "__main__":
    unittest.main()
