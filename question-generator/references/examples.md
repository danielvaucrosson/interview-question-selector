# Calibration Examples

These examples demonstrate the expected quality, format, and depth at each difficulty level. Use them to calibrate new questions.

## Difficulty 1 — Foundational

### Good Example

```
question_id: DE-GEN-001
question: "What is the difference between ETL and ELT? When would you choose one over the other in a cloud environment?"
question_type: definition
answer:
  • ETL transforms data externally before loading; ELT loads raw then transforms in-warehouse
  • ELT leverages elastic cloud compute; preferred when warehouse has scalable resources
  • ETL still appropriate for sensitive data requiring pre-load masking or filtering
  • ELT preserves raw source data for reprocessing and auditing
domain: Data Engineering
sub_domain: ETL / ELT Design
technology: GEN
difficulty: 1
tags: ETL, ELT, cloud transformation, data loading patterns
```

**Why it works:** Tests a fundamental concept. Answer bullets are concise and cover the key distinction, when to use each, and a practical trade-off.

### Bad Example (don't do this)

```
question: "What is ETL?"
answer:
  • Extract, Transform, Load
```

**Why it fails:** Too simple (one-word recall), single bullet, no depth, no trade-offs.

---

## Difficulty 2 — Applied

### Good Example

```
question_id: DV-PBI-002
question: "A client has 500 users across 12 offices needing different data access levels. How would you design row-level security in Power BI?"
question_type: scenario
answer:
  • Dynamic RLS with security mapping table joined to model, using USERPRINCIPALNAME()
  • Single role handles office, regional, and executive access via mapping rows
  • Assign membership via Entra security groups, not individual users
  • Test edge cases: multi-role users, missing users, cross-filter propagation
  • Embedded scenarios require EffectiveIdentity in embed token API calls
domain: Data Visualization
sub_domain: Governance & Standards
technology: PBI
other_skills: SD
difficulty: 2
tags: RLS, dynamic RLS, USERPRINCIPALNAME, Entra, security mapping
```

**Why it works:** Presents a realistic consulting scenario. Tests whether the candidate can design a solution (not just define RLS). Answer covers architecture, implementation detail, operational concerns, and an advanced consideration.

### Bad Example (don't do this)

```
question: "What is row-level security in Power BI?"
answer:
  • RLS restricts data access at the row level
  • You create roles in Power BI Desktop
  • You assign users to roles in the Service
```

**Why it fails:** This is a difficulty 1 definition question mislabeled as difficulty 2. No scenario, no design challenge, no trade-offs.

---

## Difficulty 3 — Architectural

### Good Example

```
question_id: DV-QLK-003
question: "An enterprise has 200+ QlikView apps with macros, triggers, and document security. Design a migration strategy to Qlik Sense on Qlik Cloud."
question_type: scenario
answer:
  • Audit and rationalize: retire unused apps, consolidate duplicates before migrating
  • Phase in waves by complexity; maintain parallel operation during transition
  • Macros/triggers have no Sense equivalent — redesign using button actions and automation
  • Security overhaul: document-based permissions become space-based governance model
  • Reuse QVD data layer; expect 30-40% manual rework on UI elements
domain: Data Visualization
sub_domain: Governance & Standards
technology: QLK
other_skills: SD, PM
difficulty: 3
tags: QlikView migration, Qlik Cloud, macros, section access, managed spaces
```

**Why it works:** Requires designing a solution across multiple dimensions (technical, organizational, security). Tests architectural thinking, migration experience, and awareness of platform differences. The candidate must navigate ambiguity and defend prioritization decisions.

### Bad Example (don't do this)

```
question: "How do you migrate QlikView to Qlik Sense?"
answer:
  • Use the QlikView Converter tool
  • Convert scripts and objects
  • Test the converted apps
  • Deploy to production
```

**Why it fails:** Answer is a generic checklist, not an architectural design. Doesn't address the real challenges (macros, security, organizational change). No trade-offs or decision points.

---

## Question Type Calibration

### Definition — Tests recall and understanding
- Should be answerable by someone who has worked with the technology
- Answers explain WHAT something is and WHY it matters
- Even at difficulty 1, avoid pure trivia — include practical significance

### Explanation — Tests reasoning and comparison
- Requires the candidate to compare, contrast, or articulate a process
- Answers include trade-offs, not just descriptions
- "Walk me through" and "What is the difference" are strong patterns

### Scenario — Tests applied judgment
- Presents a realistic situation with constraints
- The best scenarios have multiple valid approaches (tests decision-making, not recall)
- Consulting scenarios should include client dynamics, not just technical requirements
- Answer bullets describe the approach framework, not a rigid script

## Difficulty Progression Within a Domain

When generating a set of 10 questions for a domain:

1. **Questions 1-3 (Difficulty 1):** Cover foundational concepts the role requires. Mix of definition and explanation types. Technology-specific basics (e.g., "What is X in Snowflake?") and technology-agnostic fundamentals (e.g., "What is a star schema?").

2. **Questions 4-7 (Difficulty 2):** Test whether the candidate can apply knowledge to solve problems. Comparison questions ("X vs Y, when would you use each?"), troubleshooting scenarios, and design decisions with defined constraints. Mix of explanation and scenario types.

3. **Questions 8-10 (Difficulty 3):** Test architectural thinking and leadership. Open-ended scenarios with ambiguity, multi-stakeholder dynamics, cross-platform decisions, migration/transformation projects. Primarily scenario type. Should assess whether the candidate can own outcomes, not just execute tasks.
