---
name: gtm-resume-tailor
version: 1.0.0
description: Tailors a resume to one GTM job posting across eight position types, mapping your real evidence to the requirements, flagging gaps, and never inventing achievements. Use with a resume and a posting.
metadata:
  author: Stefanos Karakasis
  context: claude
  derived_from: pmm-resume 3.0.0
  quality_gate: false
last_updated: 2026-10-19
---

# GTM Resume Tailor

Takes a candidate's resume and one verified job posting, and returns a resume rebuilt for that role. It generalizes `pmm-resume` from one position type to the eight tracked by GTM Job Finder. Position-type specifics live in `references/position-types.md`; this file holds the protocol shared by all eight.

**Tone:** a senior hiring manager in the target discipline. Direct, specific, outcome-oriented. No generic advice.

---

## Trigger

- **When:** a candidate resume and a specific posting are both available and the goal is to tailor the resume to that posting.
- **Not for:** see Do Not Use For.
- **Example prompts:** "Tailor my resume to this posting", "Rebuild my resume for this GTM Engineer role", "Which of my bullets should I lead with for this FDE job?"

---

## Inputs

- **Candidate profile card** (from agent onboarding): skills, seniority, location, salary band. Used for level calibration only. Salary never appears on the resume.
- **Resume**: PDF, DOCX or markdown, or pasted profile text.
- **Posting**: URL and full text of one verified-live posting. If only a URL is given, fetch the text before starting.
- **Bullet bank**: optional, at `profiles/<user>/bullet-bank.md`.
- **Defaults:** inside the agent the goal is already TAILOR, so do not re-ask it. Used standalone, confirm the goal in one sentence before starting. Confirm any inferred seniority or position type with the user before building on it.

---

## Pre-flight

- Resume missing → ask for it. Posting text missing → fetch it or ask. Do not tailor against a guessed JD.
- Check the posting is for one of the eight position types. If it fits none, use the generic rules in Do Not Use For and say so.

---

## Steps

### Step 1: Classify the posting

Assign one position type and one track, using the signal words in `references/position-types.md` and the track test:
- Builds AI systems or agents → AI GTM
- Uses AI tools but owns a classic GTM function → Bridge
- AI incidental or unstated → Traditional GTM

State the result with confidence:
```
Position type: Forward-Deployed Engineer (High) | Track: AI GTM | Level: Senior
```
When GTM Engineering and FDE are both plausible, apply the distinguishing test: does the role build and own systems generally (GTM Engineering), or deploy and configure the product inside individual customer environments, usually after the sale (FDE)? If confidence is Medium or Low, ask the user which type they are targeting.

### Step 2: Load the type profile

Read only the matching section of `references/position-types.md`. It supplies the hiring lens, lead metrics, evidence to surface, red flags, skills order and level calibration for that type.

### Step 3: Dissect the posting

Output a four-layer table:
1. **Must-haves**: 6-10 non-negotiables. Mark each one the resume does not currently prove.
2. **Cultural signals**: what kind of person the language implies ("ship fast" → execution-first; "own the stack" → systems builder).
3. **Nice-to-haves**: differentiators.
4. **Red flags**: places where the resume as written would disqualify the candidate.

Also classify company stage and type (AI-native, PLG, enterprise, fintech, early-stage) because it shifts which bullet categories to lead with.

### Step 4: Map evidence and rank bullets

For each must-have, find the candidate's strongest real evidence and label its level:
- **Shipped**: built it, it ran in production, there is an outcome
- **Led**: owned it end to end or led the people who built it
- **Contributed**: a defined part of something larger
- **Exposed**: worked near it, no ownership

Rank bullets by (1) must-have match, (2) keyword and language match with the posting, (3) type-specific lead metric present, (4) seniority fit. Keep the top 3-4 per role. Show the ranking with reasons:
```
RECOMMENDED: 1. [bullet] → Must-have "workflow automation" (Shipped), metric present, mirrors posting term "enrichment"
CUTS: [bullet] → duty description, no outcome
GAPS: [must-have with no evidence]
```
With a bullet bank, rank from it. Without one, work from the resume.

### Step 5: Close gaps honestly

For each gap, do both:
1. Ask the user 1-2 targeted questions to surface a real fact they have not written down (see "Gap questions" in the type profile).
2. If they confirm a fact, draft a bullet with XYZ+S, tagged `NEW`.

If they have no real evidence, leave the gap open and say so. Never invent an achievement, a metric, a tool, a tenure or a customer. Reframe only what is real. The newer disciplines (AEO/GEO, AI Product Management, AI Transformation) tempt padding; a short honest history beats an inflated one.

### Step 6: Write the summary

Three sentences:
1. Identity + domain + scale.
2. Three named capabilities from the type profile, not soft skills.
3. "Known for [distinctive differentiator]."

Weave in verbs and environment words from the posting. Delete generic claims (passionate, results-driven, strategic thinker).

### Step 7: Rebuild

- **IC roles:** 3-4 bullets per role, metric-first, impact-ordered.
- **Director and above:** a scope paragraph, then Key Achievements, then Responsibilities (optional).
- **Skills section:** order given by the type profile. Only list tools the candidate genuinely uses.
- **Sections:** contact → summary → experience (most recent first) → education → certifications → skills. Single column, plain headings, no tables or text boxes, so applicant-tracking systems parse it.
- No personal pronouns. Month-Year dates. Standard job titles unless the real title is distinctive and accurate.

Show each rewritten bullet as a before/after block:

| | Content | Changes |
|--|---------|---------|
| ❌ Before | [original] | |
| ✅ After | [rewrite] | [tags] |
| 💡 Why | [one-sentence note] | |

Tags: `metric-first`, `XYZ+S`, `ownership verb`, `scope anchor`, `commercial anchor`, `pronoun removed`, `banned word`, `passive → active`, `type signal` (language or evidence specific to the position type), `NEW`.

**XYZ+S:** X = outcome, Y = metric, Z = action, S = specific context. Apply to about 70% of impact bullets.

### Step 8: Confirm, then build

Show the rebuilt content and ask the user to confirm it. Build the final file only after confirmation, using the `docx` or `pdf` skill. Offer to save new bullets to the bullet bank; save only the entries the user approves.

---

## Level Calibration

Use the level from the candidate's profile card, checked against the resume.
- **PMM roles:** PMM / Senior PMM / PMM Lead / Principal PMM / Director / VP.
- **All other roles:** Entry & mid-level / Senior / Senior++ / Director / VP / SVP-CXO.

Calibrate every rewrite to the target level. Individual-contributor levels are judged on scope of what they built or shipped. Director and above are judged on system ownership, team leadership and commercial accountability. A mismatch signals the candidate does not understand the level.

If the posting is more senior than the resume supports, say so plainly in the dissection, and tailor honestly rather than inflating scope.

---

## Outputs

- **Files written:** the final resume (.docx or .pdf) via the `docx` / `pdf` skill, after confirmation. Bullet bank entries only with user approval.
- **Chat output:** classification line, dissection table, evidence map, gaps and questions, before/after blocks, rebuilt resume.
- **External side effects:** none. Never submits an application.

---

## Verification

- Posting type and level confirmed when confidence was below High.
- Every bullet traces to a real fact in the resume, the bullet bank or a user answer. New facts are tagged `NEW`.
- No invented metrics, tools, customers or tenure.
- Gaps with no real evidence are reported, not filled.
- Final file built only after user confirmation.
- Salary and personal pronouns absent from the resume.

---

## Do Not Use For

- **Cover letters.** This skill is built around resume bullets, not narrative.
- **Postings outside the eight position types** (for example pure demand generation or lifecycle marketing). Apply only the shared rules (XYZ+S, metric-first, honesty, level calibration) and tell the user the type-specific guidance does not apply.
- **Full resume audits and Director+ story-arc work for Product Marketing.** Use a dedicated PMM resume-audit skill (not bundled with this plugin).
- **Submitting applications** or contacting employers.
