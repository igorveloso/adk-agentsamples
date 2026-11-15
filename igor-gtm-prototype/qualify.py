"""Deterministic, synthetic-data GTM lead qualification prototype."""
from __future__ import annotations

import json
from typing import Any


def normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def qualify_leads(
    leads: list[dict[str, Any]],
    existing_emails: set[str] | None = None,
    blocked_domains: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Return an auditable decision for every lead; never silently drop rows."""
    existing = {normalize(x) for x in (existing_emails or set())}
    blocked = {normalize(x).removeprefix("www.") for x in (blocked_domains or set())}
    seen: set[str] = set()
    decisions: list[dict[str, Any]] = []

    for lead in leads:
        email = normalize(lead.get("email"))
        domain = normalize(lead.get("company_domain")).removeprefix("www.")
        reasons: list[str] = []
        status = "qualified"

        if not email or "@" not in email or not domain:
            status, reasons = "review", ["Missing or malformed email or company domain"]
        elif domain in blocked:
            status, reasons = "excluded", ["Company domain is on the blocklist"]
        elif email in existing:
            status, reasons = "excluded", ["Contact already exists in CRM"]
        elif email in seen:
            status, reasons = "excluded", ["Duplicate contact in this batch"]

        if email:
            seen.add(email)

        score = 0
        if status == "qualified":
            if normalize(lead.get("segment")) == "enterprise":
                score += 30
                reasons.append("Enterprise segment (+30)")
            elif normalize(lead.get("segment")) == "smb":
                score += 15
                reasons.append("SMB segment (+15)")
            if lead.get("recent_buying_signal") is True:
                score += 40
                reasons.append("Recent buying signal (+40)")
            if lead.get("verified_work_email") is True:
                score += 30
                reasons.append("Verified work email (+30)")
            if not reasons:
                reasons.append("No positive scoring signals")

        decisions.append({
            "email": email,
            "company_domain": domain,
            "status": status,
            "score": score,
            "reasons": reasons,
        })
    return decisions


if __name__ == "__main__":
    sample = [
        {"email": "alex@example.com", "company_domain": "example.com",
         "segment": "enterprise", "recent_buying_signal": True,
         "verified_work_email": True},
        {"email": "ALEX@example.com", "company_domain": "example.com",
         "segment": "smb"},
        {"email": "pat@blocked.test", "company_domain": "blocked.test",
         "segment": "enterprise"},
    ]
    print(json.dumps(
        qualify_leads(sample, blocked_domains={"blocked.test"}),
        indent=2,
    ))
