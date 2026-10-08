---
name: launch-readiness
description: Review a project's readiness for real users, infer its app type and surface commonly forgotten product, UX and operational basics. Use for app-readiness reviews, pre-launch checks or next-step recommendations about missing product basics; suggest prioritized follow-ups and a TODO.md when useful.
---

# Launch readiness

Find the overlooked basics that matter for this product and its next milestone.
Review by default; implement fixes or write a tracking file when requested. This
is an original toolkit workflow; see [UPSTREAM.md](UPSTREAM.md) for its inspiration.

## Understand the product first

Follow project instructions and preserve existing work. Inspect the README,
manifests, routes/entrypoints, configuration, deployment files, tests and existing
backlog. Identify the product's audience, primary user journey, stage and intended
release surface. Infer its type from those signals, not a framework dependency
alone: a React site can be a marketing page, authenticated SaaS or internal tool.

For mixed projects, identify surfaces separately: a SaaS may have public pages,
private application routes, an API and background workers. Review the requested
app in a monorepo without expanding to unrelated packages. State the inferred type
and supporting evidence. Resolve missing facts that materially change advice;
continue independent checks while those facts are unknown.

Read the applicable sections of [references/checklists.md](references/checklists.md):
start with shared basics, then select app surfaces and capability checks that match
the project. Use it as a prompt for investigation, not a requirement to add every
feature. Prefer the user's constraints and milestone over a generic launch list.

## Check and gather evidence

Inspect actual implementations and configuration. Use safe existing checks, a
permitted local preview or supplied screenshots when they help verify behavior.
Review commands before executing them; do not trigger live purchases, emails,
migrations, deployments or destructive operations to test readiness.

Classify relevant items as:

- **Verified:** observed behavior or a completed check supports the result; state
  what was checked. Source configuration alone verifies configuration, not runtime.
- **Gap:** a concrete missing/broken behavior is supported by evidence. Explain
  the user scenario and consequence, with a file/route reference where available.
- **Needs verification:** evidence is insufficient, the environment is unavailable
  or a product/provider decision is missing. Give a specific way to resolve it.
- **Not applicable:** the capability or audience doesn't need this item; briefly
  explain important exclusions without flooding the report with skipped checks.

Don't declare an item missing from a filename search alone. Frameworks, hosting
providers and generated builds may supply metadata, robots, routing or assets.
Likewise, a file's presence does not prove that it serves the correct content.
Keep secrets, private customer data and internal URLs out of reports. Use current
official documentation when a finding depends on changing platform or policy rules.

## Recommend the next work

Rank actionable gaps and important verification tasks by impact on the primary
journey, release risk and effort. Use **Blocker** for demonstrated failures that
prevent the intended release or expose serious harm, **Before launch** for material
basics needed at this milestone, and **Later** for optional improvements. Tie priority
to this product; a missing favicon is not equivalent to broken account isolation.

Give a short ordered next-step list. Each task needs evidence or a stated unknown,
a concrete action and a way to tell it is done. Identify dependencies where useful.
Don't prescribe analytics, cookie banners, payments or SEO to every app. Surface
legal/privacy decisions for the applicable audience and data use without claiming
that a checklist establishes compliance. Route a demonstrated concern to a deeper
review only when the user requests it or the concern needs that work.

## Report and offer tracking

Lead with the inferred app type, scope, milestone and the most important next action.
Summarize verified basics, list prioritized gaps/verification tasks and state checks
run and remaining limits. Avoid a readiness score or a claim of production safety
based on partial inspection.

When there are actionable follow-ups, suggest tracking them in `TODO.md` at the
reviewed app's root. If an existing backlog serves that purpose, recommend updating
it instead of duplicating it. The suggestion alone does not create a file. If tracking
is requested, read [references/follow-up.md](references/follow-up.md), then create
or merge tasks while preserving existing content, completed work and project style.
