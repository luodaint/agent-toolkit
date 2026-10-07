---
name: simplify
description: >-
  Simplify a specified change or code area while preserving behavior. Use when
  asked to clean up code, consolidate existing helpers, reduce unnecessary
  complexity or remove demonstrated waste in recently changed code.
---

# Simplify

Improve the requested code with small, justified changes. This is an editing
workflow when cleanup is requested; a request only for observations stays
read-only. See [UPSTREAM.md](UPSTREAM.md) for the origin of the workflow concept.

## Bound the work

Identify the requested files, diff, branch or commit and follow applicable project
instructions. Inspect staged, unstaged and relevant untracked changes so existing
work is preserved. For branch comparisons, use the verified target and merge base.
If the worktree is clean, use the explicit target or a clearly identified change
from the conversation. Do not choose arbitrary recent files to manufacture work.

Read affected callers, tests and project conventions before proposing edits.
Keep externally observable behavior, interfaces, error handling, authorization,
ordering, side effects and data ownership intact unless a change is requested.

## Examine three aspects

- **Reuse:** check for an established helper that already serves the same purpose.
  Verify its contract and dependency direction before adopting it. Similar-looking
  code with different domain meaning may be clearer kept separate.
- **Clarity:** identify avoidable branching, indirect control flow or duplicated
  representation that makes the change difficult to follow. Favor the smallest
  improvement that fits existing conventions; extra abstraction can increase the
  burden rather than reduce it.
- **Cost:** trace work done on real execution paths and its frequency. Remove
  demonstrably repeated work or excessive allocation where behavior is preserved.
  Base performance claims on evidence, and measure when the benefit is uncertain.
  Changes to concurrency, caching or lifetime management require checking order,
  invalidation, cancellation, resource limits and synchronization guarantees.

These aspects can be checked by one agent. If delegation is available and
authorized, independent readers may inspect them concurrently and return
suggestions; one editor consolidates and applies changes to avoid conflicting
patches. Do not require a particular agent product or a fixed number of agents.

## Apply and validate

Judge each suggestion against actual behavior and scope. Make an edit only when
its benefit outweighs migration and regression risk. Avoid adding dependencies,
rewriting unrelated modules or treating fewer lines as proof of a better design.
Leave uncertain ideas as suggestions. Preserve intentional safety checks unless
the replacement maintains the same invariant.

Run relevant existing checks after editing. Use a targeted regression or behavior
comparison when an observable contract could change; do not add tests that merely
assert the new implementation's shape. Review the final diff for unintended
changes and report any verification that could not be completed.

Summarize the concrete improvements, the scope and checks actually performed. If
the existing code is already appropriate, say so and leave it unchanged.
