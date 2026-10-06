# Actionable review findings

## Severity

- **P0 — Critical:** a demonstrated issue requiring immediate attention, such as
  unavoidable data loss or a broadly exploitable vulnerability. Reserve this
  for issues whose impact is established, not speculative.
- **P1 — High:** a serious defect in a supported scenario that should be fixed
  before release, such as a broken primary flow or incorrect authorization.
- **P2 — Medium:** a concrete bug in a narrower scenario, incorrect edge-case
  behavior or a maintainability problem with a demonstrated consequence.
- **P3 — Low:** a smaller actionable defect with limited impact. Skip cosmetic
  preferences and issues already covered by formatting tools.

Choose severity from the actual impact and likelihood. Follow the project's
severity scheme when it defines one.

## Finding shape

```text
[P2] Preserve the tenant filter when loading the requested record
Location: src/records.py:42
When a user supplies an ID belonging to a different tenant, this new lookup
queries by ID alone. The route's login check does not constrain record ownership,
so it can return another tenant's data. Apply the tenant constraint before the
lookup, and cover a cross-tenant request with a regression test.
```

This is a hypothetical format example, not a finding about the reviewed project.
Each real finding needs evidence from that project. Explain the triggering
condition and observable consequence; avoid vague statements such as "could be
unsafe" without a supported path. Use absolute workspace paths or platform diff
links when supported by the output environment.

End the report with relevant checks and limitations, for example:

```text
Reviewed the branch diff against the verified target branch and traced the
changed record lookup. Ran the focused request tests. Database integration tests
were not run because the required service was unavailable.
```

Keep findings separate from open questions. If uncertainty prevents establishing
a defect, state what information is missing instead of presenting it as a bug.
