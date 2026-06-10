# ADR-002: Licensing of tooling and the Assurance Evidence Base

## Status

**proposed — needs Mohamed's decision.** Until accepted, the repo carries **no licence
file**, i.e. all rights reserved by default. Do not add a LICENSE file before this is
decided.

## Context

The strategy is an **open** Assurance Evidence Base with services and (later) SaaS on
top. Open-by-default builds credibility and aligns with the UK AISI ecosystem (Inspect
is MIT-licensed). But two things complicate signing a licence today:

1. **The legal vehicle is not yet incorporated — by design.** A licence names a
   copyright holder; right now that would be Mohamed personally, and copyright would
   need assigning to the Ltd at incorporation.
2. The split between what is open (evidence base, methodology) and what is proprietary
   (client reports, future SaaS) is a commercial decision, not an engineering one.

## Decision (proposed)

- **Code** (`/evals` tasks, `/redteam` configs, `/infra`): **Apache-2.0** — permissive,
  patent grant, the default for credible open tooling.
- **Evidence Base content and methodology docs** (`/docs`, published `/reports`):
  **CC BY 4.0** — open with attribution, which is the point of the Evidence Base.
- **Client-specific reports:** never licensed openly; published only as redacted,
  client-approved versions.
- Copyright held by Mohamed SG Omar personally until incorporation, then assigned to
  the Ltd (record the assignment).

## Consequences

- Easier: contributions, citations, grant-reviewer diligence, AISI-ecosystem alignment.
- Harder: competitors can use the open tooling (acceptable — the moat is independence,
  rigour and the evidence corpus, not the scripts).

## Alternatives considered

- **MIT for code:** fine too; Apache-2.0 preferred for the explicit patent grant.
- **AGPL:** protects against SaaS free-riding but chills enterprise/NHS adoption and
  contribution. Wrong trade for a trust business.
- **Fully proprietary:** contradicts the open Evidence Base strategy that anchors the
  Sovereign AI / DSIT funding narrative.
