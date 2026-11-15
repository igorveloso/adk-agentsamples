# GTM Lead Qualification — Personal Prototype

**Status:** standalone Python prototype (not yet integrated with Google ADK).

This is an **original extension created within a repository containing upstream Google ADK samples**. It uses only fictional lead records and the Python standard library. It is **not** an enterprise lead scoring system or a production-ready agent.

## What it demonstrates

- Normalizes company domains and email addresses
- Deduplicates leads by normalized email
- Excludes records already in the CRM, on blocklists, or missing contact data
- Scores remaining leads using explicit, auditable rules
- Returns structured decisions and human-readable explanations

The rules are intentionally simple and deterministic. A future ADK agent could call this function as a tool, while keeping exclusion logic deterministic and auditable.

## Run

From this directory:

```bash
python3 qualify.py
python3 -m unittest discover -s tests -v
```

No external API keys, services, or customer data are required.

## Boundaries

This demo uses **synthetic** data only. It does not connect to Salesforce, Clay, Salesloft, or other production services. The rules are examples, not a claim about Wellhub's internal qualification processes.

## Roadmap

- Add a proper ADK tool wrapper and sample agent with optional LLM explanations
- Add schema validation and more nuanced account matching
- Add consent and data retention policies before any real CRM integration
- Test ambiguous duplicates, international domains, and scoring fairness
